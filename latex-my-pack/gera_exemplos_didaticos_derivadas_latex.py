from random import randint,choice
from os import system
system("cls")


def poly2latex(coeffs, order='descend'):
    # Handle order aliases
    if order in ['descend', 'd']:
        indices = range(len(coeffs))
    elif order in ['ascend', 'a']:
        indices = range(len(coeffs)-1, -1, -1)
    else:
        raise ValueError("order must be 'descend', 'd', 'ascend', or 'a'")

    terms = []
    n = len(coeffs)
    for idx in indices:
        coef = coeffs[idx]
        # Determine power based on order
        if order in ['descend', 'd']:
            power = n - idx - 1
        else:
            power = idx

        if coef == 0:
            continue

        # Sign
        if not terms:
            sign = '- ' if coef < 0 else ''
        else:
            sign = ' - ' if coef < 0 else ' + '

        abs_coef = abs(coef)
        # Coefficient string
        if abs_coef == 1 and power != 0:
            coef_str = ''
        else:
            coef_str = str(abs_coef)

        # Power string
        if power == 0:
            term = f"{sign}{coef_str}"
        elif power == 1:
            term = f"{sign}{coef_str}x"
        else:
            term = f"{sign}{coef_str}x^{{{power}}}"

        terms.append(term)

    # Join and clean up leading sign/space
    result = ''.join(terms)
    return result.lstrip(' +')


def generate_polynomial(degree, coef_min=-5, coef_max=5):
    # Ensure the leading coefficient is not zero
    while True:
        coeffs = [randint(coef_min, coef_max) for _ in range(degree + 1)]
        if coeffs[0] != 0:
            break

    return coeffs


def derivative_poly(coeffs, order='descend'):
    # Calculate the derivative of the polynomial considering the order
    n = len(coeffs)
    if order in ['descend', 'd']:  # ok
        # Standard: highest degree first
        return [coef * (n - idx - 1) for idx, coef in enumerate(coeffs[:-1])]
    elif order in ['ascend', 'a']:  # !! errado
        # Lowest degree first
        deriv = [coef * idx for idx, coef in enumerate(coeffs)]
        return deriv[1:]
    else:
        raise ValueError("order must be 'descend', 'd', 'ascend', or 'a'")





s = """\\documentclass[12pt,a4paper]{article}\n\\usepackage{preambuloaula}\n
\\title{Exercícios resolvidos: derivadas}\n\\begin{document}\n\\maketitle\n\\tableofcontents\n
\\section{Exercícios resolvidos de derivadas de polinômios}\n
Exercícios resolvidos de derivadas de polinômios (uso da regra da multiplicação por constante, regra da soma, regra da constante e regra do tombo/potência):
\n\\jboxx{\\[
    f(x) = k\\cdot x^n \\qquad \\Longrightarrow \\qquad f'(x) = k\\cdot n \\cdot x^{n-1}
\\]}\n
\\begin{abcd}\n"""


for i in range(20):
    # Generate a random polynomial of degree 4
    poly = generate_polynomial(randint(2, 8))
    poly_str = poly2latex(poly)
    deriv_str = poly2latex(derivative_poly(poly))
    s += f"\\item $f(x)={poly_str}$\n\n \\textbf{{Solução:}}\n \\["
    s += f"f'(x) = {deriv_str}.\n\\]\n"
s += "\\end{abcd}"


def given_exponential(exp_poly, order='descend', base='e', constant=1,ommit_constant=False):
    """Converts a polynomial to an exponential function string."""
    if constant == 1:
        return f"{base}^{{{poly2latex(exp_poly, order)}}}"
    elif constant == -1:
        return f"- {base}^{{{poly2latex(exp_poly, order)}}}"
    else:
        if ommit_constant:
            return f"{base}^{{{poly2latex(exp_poly, order)}}}"
        return f"{constant} \\cdot {base}^{{{poly2latex(exp_poly, order)}}}"


def derivative_poly_exponential(exp_poly, order='descend', base='e', constant=1):
    """Calculates the derivative_poly of an exponential function."""
    s = ""
    if constant == 1:
        s += ""
    elif constant == -1:
        s += f"- "
    else:
        s += f"{constant} \\cdot "

    poly_str = poly2latex(exp_poly, order)
    deriv_str = poly2latex(derivative_poly(exp_poly, order), order)
    if base == 'e':
        s += f"({deriv_str}) \\cdot  e^{{{poly_str}}}"
    else:
        s+= f"({deriv_str}) \\cdot {base}^{{{poly_str}}} \\cdot \\ln({base})"
    return s





s += """
\\section{Exercícios resolvidos de derivadas de funções exponenciais}\n
Exercícios resolvidos de derivadas de funções exponenciais (uso da regra da multiplicação por constante, regra da soma, regra da constante e regra do tombo/potência, e regra da exponencial):
\n\\jboxx{\\[
    \\begin{aligned}
    f(x) &= k\\cdot a^{f(x)} \\qquad \\Longrightarrow \\qquad f'(x) = k\\cdot f'(x) \\cdot a^{f(x)}
    \\cdot \\ln(a) \\\\[12pt]\n &\\text{(em que $\\ln(a)=\\log_e(a),\;\;e=2,71828...$)}
    \\end{aligned}
\\]}\n
Caso a base seja $e$, a expressão fica mais simples:
\n\\jboxx{\\[
    f(x) = k\\cdot e^{f(x)} \\qquad \\Longrightarrow \\qquad f'(x) = k\\cdot f'(x) \\cdot e^{f(x)}
\\]}\n
\\begin{abcd}\n"""

for _ in range(20):
    poly = generate_polynomial(randint(2, 4),-10,10)
    constant = randint(-10, 10)
    while constant == 0:
        constant = randint(-10, 10)
    choice_base = choice(['e', randint(2, 10)])
    exp = given_exponential(poly, order='descend', base=choice_base, constant=constant)
    deriv_exp = derivative_poly_exponential(poly, order='descend', base=choice_base, constant=constant)
    s += f"\\item $f(x)={exp}$\n\n\\textbf{{Solução:}}"
    s += f"\n\\[\nf'(x)={deriv_exp}\n\\]\n"
s+= "\\end{abcd}\n\n"



def given_poly_prod_exp(poly, exp_poly, order='descend', base='e', constant=1,ommit_constant=False):
    """Converts a polynomial and an exponential to a product string."""
    poly_str = poly2latex(poly, order)
    exp_str = given_exponential(exp_poly, order, base, constant)
    if constant == 1:
        return f"({poly_str}) \\cdot {exp_str}"
    elif constant == -1:
        return f"- ({poly_str}) \\cdot {exp_str}"
    else:
        return f"{constant} \\cdot ({poly_str}) \\cdot {exp_str}"


def derivative_poly_prod_exp(poly, exp_poly, order='descend', base='e', constant=1):
    """Calculates the derivative_poly of a product of a polynomial and an exponential."""
    poly_str = poly2latex(poly, order)
    exp_str = given_exponential(exp_poly, order, base, constant=1)
    deriv_poly_str = poly2latex(derivative_poly(poly,order), order)
    deriv_exp_str = derivative_poly_exponential(exp_poly, order, base, constant=1)

    if constant == 1:
        return f"({deriv_poly_str}) \\cdot {exp_str} + ({poly_str}) \\cdot {deriv_exp_str}"
    elif constant == -1:
        return f"- ({deriv_poly_str}) \\cdot {exp_str} - ({poly_str}) \\cdot {deriv_exp_str}"
    else:
        return f"{constant} \\cdot \\Big( ({deriv_poly_str}) \\cdot {exp_str} + ({poly_str}) \\cdot {deriv_exp_str} \\Big)"


s += """
\\section{Exercícios resolvidos de derivadas do \\underline{produto} de polinomiais e exponenciais}\n
Exercícios resolvidos de derivadas de funções exponenciais: regra do produto!
\n\\jboxx{\\[
    f(x) = u(x)\\cdot v(x) \\qquad \\Longrightarrow \\qquad f'(x) = u'(x)\\cdot v(x) + u(x)\\cdot v'(x)
\\]}\n
\\begin{abcd}\n"""

for _ in range(20):
    poly = generate_polynomial(randint(1, 3), -10, 10)
    exp_poly = generate_polynomial(randint(1, 2), -10, 10)
    constant = randint(-10, 10)
    while constant == 0:
        constant = randint(-10, 10)
    choice_base = choice(['e', randint(2, 10)])
    prod_exp = given_poly_prod_exp(poly, exp_poly, order='descend', base=choice_base, constant=1)
    deriv_prod_exp = derivative_poly_prod_exp(poly, exp_poly, order='descend', base=choice_base, constant=1)
    s += f"\\item $ f(x)={constant} \\cdot {prod_exp} $\n\n\\textbf{{Solução:}}\n"
    s += f"\\[\nf'(x)={constant} \\cdot\\Big[{deriv_prod_exp}\\Big]\n\\]\n\n"
s += "\\end{abcd}\n\n"

s += "\n\\end{document}"
with open(r"D:\MYDATA\DESKTOP\AULAS-2025\gera_ex.tex", "wb") as f:
    f.write(s.encode('utf-8'))
print('Tudo ok')
