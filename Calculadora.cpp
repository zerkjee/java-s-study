#include <cstdio>
    int main(){
double a, b;
int opcao;
printf("1 - Adição\n");
printf("2 - Subtração\n");
printf("3 - Multiplicação\n");
printf("4 - Divisão\n");
printf("5 - Potencia\n");
printf("6 - Seno\n");
printf("7 - Cosseno\n");
printf("0 - Sair\n");
scanf("%d", &opcao);
printf("Digite o Primeiro número: ");
scanf("%lf", &a);
printf("Digite o Segundo número: ");
scanf("%lf", &b);
if (opcao == 1 ){
    printf("O Resultado;%2lf\n", a + b);

}




}


