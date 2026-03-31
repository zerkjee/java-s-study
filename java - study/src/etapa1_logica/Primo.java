package etapa1_logica;
import java.util.Scanner;
public class Primo {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Digite um número: ");
        int numero = sc.nextInt();

        int divisores = 0;

        for (int i = 1; i <= numero; i++) {
            if (numero % i == 0)
                    divisores++;

        }

        if (divisores == 2) {
            System.out.println("Número primo");
        } else {
            System.out.println("Não é primo");
        }

    }
}