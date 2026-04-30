#!/usr/bin/env python3
"""
ZPL to PDF Converter
Renders ZPL labels locally using Pillow and python-barcode.

Usage:
    python3 zpl_to_pdf.py input.zpl output.pdf
    python3 zpl_to_pdf.py input.zpl output.pdf --dpi 203 --width 4 --height 6
    echo "^XA^FO50,50^ADN,36,20^FDHELLO^FS^XZ" | python3 zpl_to_pdf.py - output.pdf

Install dependencies:
    pip install Pillow python-barcode reportlab
"""

import sys
import io
import re
import argparse
from dataclasses import dataclass, field
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
import barcode as barcode_lib
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader


# --- Data model -----------------------------------------------------------

@dataclass
class DrawCmd:
    kind: str           # "text", "barcode", "box", "circle"
    x: int = 0
    y: int = 0
    # text
    text: str = ""
    font_h: int = 30
    font_w: int = 0
    reverse: bool = False
    # barcode
    bc_type: str = "code128"
    bc_height: int = 100
    bc_show_text: bool = True
    # box
    box_w: int = 0
    box_h: int = 0
    box_thick: int = 1
    box_fill: bool = False
    # circle
    circle_d: int = 0
    circle_thick: int = 1


@dataclass
class ZplLabel:
    width_dots: int = 812
    height_dots: int = 1218
    cmds: list = field(default_factory=list)


# --- Parser ---------------------------------------------------------------

def _i(s: str, default: int = 0) -> int:
    try:
        return int(s.strip())
    except Exception:
        return default


def _arg(args: list, idx: int, default: str = "") -> str:
    return args[idx].strip() if idx < len(args) else default


def parse_zpl(zpl: str, dpi: int = 203, label_w: float = 4.0, label_h: float = 6.0) -> list[ZplLabel]:
    labels = []

    for raw in re.split(r'\^XA', zpl, flags=re.IGNORECASE):
        body = re.split(r'\^XZ', raw, flags=re.IGNORECASE)[0]
        if not body.strip():
            continue

        label = ZplLabel(
            width_dots=int(label_w * dpi),
            height_dots=int(label_h * dpi),
        )

        cur_x, cur_y = 0, 0
        cur_font_h, cur_font_w = 30, 0
        cur_bc_h = 100
        cur_bc_show = True
        cur_bc_type = "code128"
        pending_bc = False
        reverse = False

        # ZPL commands are exactly 2 letters after ^; limit to {1,2} to avoid
        # capturing field data that starts with letters (e.g. ^FDHello)
        for token in re.findall(r'\^[A-Za-z]{1,2}[^\^]*', body):
            m = re.match(r'\^([A-Za-z]{1,2})(.*)', token, re.DOTALL)
            if not m:
                continue
            letters = m.group(1).upper()
            args_str = m.group(2).strip()
            args = [a.strip() for a in args_str.split(",")]

            if letters == "FO":
                cur_x = _i(_arg(args, 0))
                cur_y = _i(_arg(args, 1))
                pending_bc = False
                reverse = False

            elif letters == "CF":
                cur_font_h = _i(_arg(args, 1), 30)
                cur_font_w = _i(_arg(args, 2), 0)

            elif letters.startswith("A"):
                # ^A font,orientation,height,width  or  ^ADN,36,20
                parts = args_str.split(",")
                cur_font_h = _i(_arg(parts, 1 if len(letters) == 1 else 0, "30"), 30)
                cur_font_w = _i(_arg(parts, 2 if len(letters) == 1 else 1, "0"), 0)

            elif letters == "BY":
                # ^BY module_width,ratio,bar_height
                cur_bc_h = _i(_arg(args, 2), 100)

            elif letters.startswith("B"):
                bc_letter = letters[1] if len(letters) > 1 else "C"
                bc_map = {"C": "code128", "3": "code39", "E": "ean8", "A": "code39"}
                cur_bc_type = bc_map.get(bc_letter, "code128")
                h_arg = _arg(args, 1)
                if h_arg:
                    cur_bc_h = _i(h_arg, cur_bc_h)
                show_arg = _arg(args, 2).upper()
                cur_bc_show = show_arg != "N"
                pending_bc = True

            elif letters == "FD":
                data = args_str  # raw text after ^FD
                if pending_bc:
                    label.cmds.append(DrawCmd(
                        kind="barcode", x=cur_x, y=cur_y,
                        text=data, bc_type=cur_bc_type,
                        bc_height=cur_bc_h, bc_show_text=cur_bc_show,
                    ))
                    pending_bc = False
                else:
                    label.cmds.append(DrawCmd(
                        kind="text", x=cur_x, y=cur_y, text=data,
                        font_h=cur_font_h, font_w=cur_font_w, reverse=reverse,
                    ))

            elif letters == "FS":
                reverse = False

            elif letters == "FR":
                reverse = True

            elif letters == "GB":
                w = _i(_arg(args, 0), 10)
                h = _i(_arg(args, 1), 10)
                thick = _i(_arg(args, 2), 1)
                color = _arg(args, 3, "B")
                label.cmds.append(DrawCmd(
                    kind="box", x=cur_x, y=cur_y,
                    box_w=w, box_h=h, box_thick=thick,
                    box_fill=(thick >= min(w, h) or color.upper() == "B" and thick >= min(w, h)),
                ))

            elif letters == "GC":
                d = _i(_arg(args, 0), 50)
                thick = _i(_arg(args, 1), 1)
                label.cmds.append(DrawCmd(
                    kind="circle", x=cur_x, y=cur_y,
                    circle_d=d, circle_thick=thick,
                ))

            elif letters == "PW":
                label.width_dots = _i(_arg(args, 0), label.width_dots)

            elif letters == "LL":
                label.height_dots = _i(_arg(args, 0), label.height_dots)

        if label.cmds:
            labels.append(label)

    return labels


# --- Renderer -------------------------------------------------------------

_FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
]


def _font(size: int):
    for path in _FONT_PATHS:
        try:
            return ImageFont.truetype(path, max(size, 8))
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def _render_barcode(text: str, bc_type: str, height: int) -> Optional[Image.Image]:
    try:
        cls = barcode_lib.get_barcode_class(bc_type)
        buf = io.BytesIO()
        cls(text, writer=ImageWriter()).write(buf, options={
            "module_height": max(height / 10, 5),
            "quiet_zone": 2,
            "font_size": 10,
            "text_distance": 3,
            "dpi": 203,
            "write_text": True,
        })
        buf.seek(0)
        return Image.open(buf).convert("RGBA")
    except Exception as e:
        print(f"  Warning: barcode '{text}' ({bc_type}): {e}", file=sys.stderr)
        return None


def render_label(label: ZplLabel) -> Image.Image:
    img = Image.new("RGB", (label.width_dots, label.height_dots), "white")
    draw = ImageDraw.Draw(img)

    for c in label.cmds:
        if c.kind == "text" and c.text:
            font = _font(c.font_h)
            if c.reverse:
                bbox = draw.textbbox((c.x, c.y), c.text, font=font)
                draw.rectangle(bbox, fill="black")
                draw.text((c.x, c.y), c.text, fill="white", font=font)
            else:
                draw.text((c.x, c.y), c.text, fill="black", font=font)

        elif c.kind == "barcode" and c.text:
            bc_img = _render_barcode(c.text, c.bc_type, c.bc_height)
            if bc_img:
                img.paste(bc_img, (c.x, c.y), bc_img)

        elif c.kind == "box":
            x2, y2 = c.x + c.box_w, c.y + c.box_h
            if c.box_thick >= min(c.box_w, c.box_h):
                draw.rectangle([c.x, c.y, x2, y2], fill="black")
            else:
                draw.rectangle([c.x, c.y, x2, y2], outline="black", width=c.box_thick)

        elif c.kind == "circle":
            x2, y2 = c.x + c.circle_d, c.y + c.circle_d
            draw.ellipse([c.x, c.y, x2, y2], outline="black", width=c.circle_thick)

    return img


# --- PDF writer -----------------------------------------------------------

def images_to_pdf(images: list[Image.Image], output_path: str, dpi: int = 203):
    if not images:
        raise ValueError("No images to write.")
    c = pdf_canvas.Canvas(output_path)
    for img in images:
        w_px, h_px = img.size
        pdf_w = w_px * 72 / dpi
        pdf_h = h_px * 72 / dpi
        c.setPageSize((pdf_w, pdf_h))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        c.drawImage(ImageReader(buf), 0, 0, width=pdf_w, height=pdf_h)
        c.showPage()
    c.save()


# --- Entry point ----------------------------------------------------------

def convert(input_path: str, output_path: str, dpi: int, width: float, height: float):
    zpl_content = sys.stdin.read() if input_path == "-" else open(input_path, encoding="utf-8").read()

    labels = parse_zpl(zpl_content, dpi=dpi, label_w=width, label_h=height)
    if not labels:
        print("Warning: No valid ZPL labels found in input.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(labels)} label(s). Rendering...")
    images = []
    for i, label in enumerate(labels, 1):
        print(f"  Label {i}/{len(labels)}...", end=" ", flush=True)
        images.append(render_label(label))
        print("done")

    print(f"Saving PDF: {output_path}")
    images_to_pdf(images, output_path, dpi=dpi)
    print("Done.")


def main():
    p = argparse.ArgumentParser(
        description="Convert ZPL label files to PDF (offline, no external API).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("input", help="ZPL file path, or '-' for stdin")
    p.add_argument("output", help="Output PDF path")
    p.add_argument("--dpi", type=int, default=203,
                   help="Printer DPI (203 or 300). Default: 203")
    p.add_argument("--width", type=float, default=4.0,
                   help="Label width in inches. Default: 4.0")
    p.add_argument("--height", type=float, default=6.0,
                   help="Label height in inches. Default: 6.0")
    args = p.parse_args()
    try:
        convert(args.input, args.output, args.dpi, args.width, args.height)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
