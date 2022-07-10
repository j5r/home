#include <stdio.h>
#include "hypotesistest.c"
#include <conio.h>

int main()
{
    printf("\nHYPOTESIS TEST FOR THE AVERAGE/MEAN OF A POPULATION\n\n\n");
    int N;
    printf("Type the sample size (integer number).\n\t");
    scanf("%d", &N);
    printf("\n");
    if (N <= 30)
    {
        printf("\n\n\t>> Your sample is too small to proceed the test. I am sorry.");
        getch();
        return 1;
    }

    double hypotesis_media;
    printf("What is the hypotesis mean (the hypotesis value)? (real number).\n\t");
    scanf("%lf", &hypotesis_media);
    printf("\n");

    double observed_media;
    printf("What is the sample mean (the observed value)? (real number).\n\t");
    scanf("%lf", &observed_media);
    printf("\n");

    double desvio_p = -1;
    while (desvio_p <= 0)
    {
        printf("What is the sample standard deviation? (positive real number)\n\t");
        scanf("%lf", &desvio_p);
        printf("\n");
        if (desvio_p <= 0)
        {
            printf("Positive value, please!\n\n");
        }
    }

    double indice_signif = -1;
    while (indice_signif <= 0 || indice_signif >= 1)
    {
        printf("What is the significancy index? (a real number in (0, 1)).\n\t");
        scanf("%lf", &indice_signif);
        printf("\n");
        if (indice_signif <= 0 || indice_signif >= 1)
        {
            printf("A value in (0, 1), please!\n\n");
        }
    }

    int kind;
    printf("What kind of test do you want to perform?\n");
    printf("\tLeft-side  -> type '1'\n");
    printf("\tRight-side -> type '3'\n");
    printf("\tBilateral  -> type '5'\n\t");
    scanf("%d", &kind);
    printf("\n");
    printf("=======================================================");

    if (kind == 1)
    {
        l_hyp_mean_test(N, hypotesis_media, observed_media, desvio_p, indice_signif);
    }
    if (kind == 3)
    {
        r_hyp_mean_test(N, hypotesis_media, observed_media, desvio_p, indice_signif);
    }
    if (kind == 5)
    {
        b_hyp_mean_test(N, hypotesis_media, observed_media, desvio_p, indice_signif);
    }
    printf("=======================================================");
    getch();
    return 0;
}
