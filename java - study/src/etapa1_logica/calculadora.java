package etapa1_logica;
import java.util.Scanner;

public class calculadora {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("Digite o primeiro número: ");
        double n1 = sc.nextDouble();

        System.out.println("Digite o segundo número: ");
        double n2 = sc.nextDouble();

        System.out.println("Digite a operação (+,-,*,/):");
        String op = sc.next();

        double resultado;


        if(op.equals("+")) {
            resultado = n1 + n2;
        } else if(op.equals("-")) {
            resultado = n1 - n2;
        } else if(op.equals("*")) {
            resultado = n1 * n2;
        } else if(op.equals("/")) {
            resultado = n1 / n2;
        } else {
            System.out.println("Operação invalida");
        return;
        }
        System.out.println("Resultado: " + resultado);
    }
}
