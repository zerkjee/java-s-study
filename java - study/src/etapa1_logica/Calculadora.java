package etapa1_logica;

import java.util.Scanner;

public class Calculadora {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Digite o primeiro número: ");
        double n1 = sc.nextDouble();

        System.out.print("Digite o segundo número: ");
        double n2 = sc.nextDouble();

        System.out.print("Escolha a operação (+, -, *, /): ");
        String op = sc.next(); // lê apenas 1 palavra/símbolo

        double resultado = 0;

        if (op.equals("+")) {
            resultado = n1 + n2;

        } else if (op.equals("-")) {
            resultado = n1 - n2;

        } else if (op.equals("*")) {
            resultado = n1 * n2;

        } else if (op.equals("/")) {
            if (n2 == 0) {
                System.out.println("Erro: divisão por zero!");
                return;
            }
            resultado = n1 / n2;

        } else {
            System.out.println("Operação inválida!");
            return;
        }

        System.out.println("Resultado: " + resultado);
    }
}