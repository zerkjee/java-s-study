package etapa1_logica;

import java.util.Scanner;

public class Tabuada {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Digite um número: ");
        int numero = sc.nextInt();

        for (int i = 1; i <= 10; i++) {
            int resultado = 0;
            resultado = numero * i;
            System.out.println(numero + "X" + i + " = " + resultado);
            // numero x i = resultado

        }

    }
}