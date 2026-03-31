package etapa1_logica;
import java.util.Scanner;
public class notas {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Digite a primeiro nota: ");
        float nota = sc.nextFloat();
        System.out.println("Digite a segundo nota: ");
        float nota2 = sc.nextFloat();
        System.out.println("Digite a terceiro nota: ");
        float nota3 = sc.nextFloat();
        System.out.println("Digite a quarta nota: ");
        float nota4 = sc.nextFloat();

        float media = (nota + nota2 + nota3 + nota4) / 4;
        if (media < 5) {
            System.out.print("Você foi reprovado com " + media + "de media");
        }
        else if(media < 7) {
            System.out.println("Você ficou de recuperação com " + media + "de media");
        }
        else {
            System.out.println("Você foi aprovado com " + media + "de media");
        }

    }
}
