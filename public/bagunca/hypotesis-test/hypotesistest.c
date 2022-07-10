#include <conio.h>
#include <math.h>

double dens_gauss(double t)
{
    return exp(-0.5 * t * t) / 2.506628274631;
}

double prob_gauss(double t)
{
    if (t <= -4.5)
        return 0;
    if (t >= 4.5)
        return 1;
    register double h = 1e-6, s = -4.5, soma = 0.0, d;
    while (s < t)
    {
        s += h;
        d = dens_gauss(s);
        soma += d * h;
    }

    return soma;
}

double inv_gauss(double prob)
{
    register double a = -4.5, b = 4.5, x = 0, tol = 1e-4;
    while (b - a > tol)
    {
        x = 0.5 * (a + b);
        if (prob_gauss(x) - prob > 0)
        {
            b = x;
        }
        else
        {
            a = x;
        }
    }
    return x;
}

double normcdf(double a, double media, double desvio_p)
{
    return prob_gauss((a - media) / desvio_p);
}
double invnorm(double prob, double media, double desvio_p)
{
    return inv_gauss(prob) * desvio_p + media;
}

double normcdf_le_a(double a, double media, double desvio_p)
{
    return prob_gauss((a - media) / desvio_p);
}
double normcdf_ge_a(double a, double media, double desvio_p)
{
    return 1 - prob_gauss((a - media) / desvio_p);
}
double normcdf_between_a_b(double a, double b, double media, double desvio_p)
{
    return normcdf_le_a(b, media, desvio_p) - normcdf_le_a(a, media, desvio_p);
}

void l_hyp_mean_test(int N, double h0_media, double observed_media, double desvio_p, double ind_signif)
{
    if (N < 30)
    {
        printf("Your sample is too small to use Normal model.\n");
        getch();
        return;
    }
    printf("\nLEFT-SIDE Hypotesis test. The sample size is :: %d:\n\n", N);
    printf("\tH_0: The mean of the population is :: %.4lf.\n", h0_media);
    printf("\tH_a: The mean of the population is smaller than :: %.4lf.\n\n", h0_media);
    printf(":: The observed mean is ..............:: %.4lf\n", observed_media);
    printf(":: The sample standard deviation is ..:: %.4lf\n", desvio_p);
    printf(":: The significancy index is .........:: %.4lf\n\n", ind_signif);

    double p_value;
    p_value = normcdf_le_a(observed_media, h0_media, desvio_p);
    printf("The P-Value is :: %.4lf%%\n\n", 100 * p_value);

    if (p_value > ind_signif)
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test confirms H_0. (P-value is greater than significancy index)\n\nTHE END.\n", 100 * ind_signif);
    }
    else
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test rejects H_0. (P-value is smaller than significancy index)\n\tThe H_a is then assumed to be true.\n\nTHE END.\n", 100 * ind_signif);
    }
    getch();
}

void r_hyp_mean_test(int N, double h0_media, double observed_media, double desvio_p, double ind_signif)
{
    if (N < 30)
    {
        printf("Your sample is too small to use Normal model.\n");
        getch();
        return;
    }

    printf("\nRIGHT-SIDE Hypotesis test. The sample size is :: %d:\n\n", N);
    printf("\tH_0: The mean of the population is :: %.4lf.\n", h0_media);
    printf("\tH_a: The mean of the population is greater than :: %.4lf.\n\n", h0_media);
    printf(":: The observed mean is ..............:: %8.4lf\n", observed_media);
    printf(":: The sample standard deviation is ..:: %8.4lf\n", desvio_p);
    printf(":: The significancy index is .........:: %8.4lf\n\n", ind_signif);

    double p_value;
    p_value = normcdf_ge_a(observed_media, h0_media, desvio_p);
    printf("The P-Value is :: %.4lf%%\n\n", 100 * p_value);

    if (p_value > ind_signif)
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test confirms H_0. (P-value is greater than significancy index)\n\nTHE END.\n", 100 * ind_signif);
    }
    else
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test rejects H_0. (P-value is smaller than significancy index)\n\tThe H_a is then assumed to be true.\n\nTHE END.\n", 100 * ind_signif);
    }
    getch();
}

void b_hyp_mean_test(int N, double h0_media, double observed_media, double desvio_p, double ind_signif)
{
    if (N < 30)
    {
        printf("Your sample is too small to use Normal model.\n");
        getch();
        return;
    }
    printf("\nBILATERAL Hypotesis test. The sample size is :: %d:\n\n", N);
    printf("\tH_0: The mean of the population is :: %.4lf.\n", h0_media);
    printf("\tH_a: The mean of the population is not :: %.4lf.\n\n", h0_media);
    printf(":: The observed mean is ..............:: %8.4lf\n", observed_media);
    printf(":: The sample standard deviation is ..:: %8.4lf\n", desvio_p);
    printf(":: The significancy index is .........:: %8.4lf\n\n", ind_signif);

    double p_value;
    if (observed_media > h0_media)
    {
        p_value = 2 * normcdf_ge_a(observed_media, h0_media, desvio_p);
    }
    else
    {
        p_value = 2 * normcdf_le_a(observed_media, h0_media, desvio_p);
    }
    printf("The P-Value is :: %.4lf%%\n\n", 100 * p_value);
    if (p_value > ind_signif)
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test confirms H_0. (P-value is greater than significancy index)\n\nTHE END.\n", 100 * ind_signif);
    }
    else
    {
        printf("RESULT\n\n\t>> Under significancy index of %.2lf%%, the test rejects H_0. (P-value is smaller than significancy index)\n\tThe H_a is then assumed to be true.\n\nTHE END.\n", 100 * ind_signif);
    }
    getch();
}
