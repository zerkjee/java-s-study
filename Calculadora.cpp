#include <cstdio>

double exponencial(double x) {
    double resultado = 1.0;
    double termo = 1.0;
    int N = 20;
    for (int i = 1; i <= N; i++) {
        termo = termo * (x / i);
        resultado += termo;
    }
    return resultado;
}

double log(double x) {
    double resultado = 0.0;
    double y = x - 1.0;
    double termo = y;
    int N = 20;

    for (int i = 1; i <= N; i++) {
        if (i > 1) termo *= y;
        if (i % 2 == 0)
            resultado -= termo / i;
        else
            resultado += termo / i;
    }

    return resultado;
}

double pow(double a, double b) {
    return exponencial(b * log(a));
}

int main() {
    double a, b;
    int opcao;

    printf("1 - Adição\n");
    printf("2 - Subtração\n");
    printf("3 - Multiplicação\n");
    printf("4 - Divisão\n");
    printf("5 - Potência\n");
    printf("6 - Seno\n");
    printf("7 - Cosseno\n");
    printf("0 - Sair\n");
    scanf("%d", &opcao);

    printf("Digite o Primeiro número: ");
    scanf("%lf", &a);
    printf("Digite o Segundo número: ");
    scanf("%lf", &b);

    if (opcao == 1)
        printf("O resultado da sua Adição é: %.2lf\n", a + b);

    if (opcao == 2)
        printf("O resultado da sua Subtração é: %.2lf\n", a - b);

    if (opcao == 3)
        printf("O resultado da sua Multiplicação é: %.2lf\n", a * b);

    if (opcao == 4) {
        if (b != 0)
            printf("O resultado da sua Divisão é: %.2lf\n", a / b);
        else
            printf("Erro: divisão por zero!\n");
    }

    if (opcao == 5)
        printf("O resultado da sua Potência é: %.5lf\n", pow(a, b));

    return 0;
}
