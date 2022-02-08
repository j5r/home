# Sedumi - Matlab - Instalação
1. [YALMIP](https://yalmip.github.io/tutorial/installation)
2. [SeDuMi](https://github.com/sqlp/sedumi)

# Como implementar LMIs no matlab com LMItoolbox

## Sequência da declaração

1.  `setlmis([])`, para iniciar uma nova implementação;
2.  `lmivar(...)`, para declarar uma nova variável;
3.  `newlmi()`, para declarar uma nova inequação;
4.  `lmiterm(...)`, para declarar os blocos dentro das matrizes da inequação;
5.  `getlmis()`, para capturar todo o conjunto de lmis declaradas;
6.  `decnbr(...)` para obter o número total de variáveis;
7.  Solvers
    - `feasp(...)`, para factibilidade;
    - `mincx(...)`, para solução;
8.  `dec2mat(...)`, para recuperar a solução.

## Explicando melhor...

- `[P_index, last_var, IDmatrix] = lmivar(T, [D, t])`, em que `[D, t]` é uma matriz **Nx2** em que a estrutura da variável desejada contém **N** blocos-diagonais (veja o exemplo abaixo para ficar mais claro).

  - **T** é o tipo de matriz

    - `T == 1` simétrica: matriz bloco-diagonal
      - **D** indica a dimensão do bloco-diagonal (blocos quadrados)
        - `D == 5` bloco **5x5**, etc.
      - **t** indica o tipo do bloco-diagonal
        - `t == 1` bloco cheio simétrico
        - `t == 0` bloco identidade
        - `t ==-1` bloco de zeros
        - Exemplo
          ```matlab
          lmivar(1, [2,  1;  % 1o bloco diagonal: bloco 2x2 do tipo  1:simétrico
                     3, -1;  % 2o bloco diagonal: bloco 3x3 do tipo -1:zeros
                     4,  0]) % 3o bloco diagonal: bloco 4x4 do tipo  0:identidade
          % corresponde à matriz
           P = [a b
                b c
                    0 0 0
                    0 0 0
                    0 0 0
                          d
                            d
                              d
                                d]
          ```
    - `T == 2` matriz cheia, `[D, t]` é uma matriz **1x2**. A variável criada será uma matriz retangular **Dxt**.

    - `T == 3` outras estruturas, `[D, t]` na verdade é qualquer matriz de qualquer tamanho.
        - Se você quer declarar entradas iguais na matriz, apenas entre com IDs repetidos nas posições desejadas.
        - Se você quer declarar entradas distintas (variáveis distintas), entre com IDs distintos nas posições desejadas.
        - Se você quer declarar algumas entradas iguais às de outras variáveis previamente declaradas, utilize o mesmo ID nas posições desejadas. Veja `IDmatrix` abaixo no item **retorno** da função.
        - Os zeros permanecerão zeros (_hard zeroes_).
      ```matlab
      structure = [ 0  11  11  11   0  12
                       13  14  14   0   2   3
                        0  11  15  16   1  10]
      [P_index, n, matrix] = lmivar(3, structure);
      ```

  - O retorno é `[P_index, last_var, IDmatrix]` em que 
    - **P_index** é um número inteiro, índice da variável LMI criada; cada chamada de `lmivar(...)` incrementa este contador.
    - **last_var** é o índice da última variável escalar criada; 
    - **IDmatrix** é uma matriz representando a estrutura declarada. Cada entrada de `IDmatrix` tem o ID da variável escalar correspondente.

Modelo da Inequação:

```matlab
[ . . . ]            [ . . . ]
[ . . . ]   <   M' * [ . . . ] * M
[ . . . ]            [ . . . ]

+A          <  -A
```

- `lmiterm([A, B, C, D], P, Q, F)`. Declare apenas os blocos ou acima ou abaixo da diagonal (e também a diagonal).
  - `A` é o índice da LMI (**newlmi**). Se estiver à esquerda da inequação, **A** deve ser positivo, do contrário, negativo.
  - `[B, C]` indica qual bloco (i, j) da LMI. Exemplo: se for o segundo bloco da diagonal, então `B == 2 == C`. Se `B == 0 == C`, então o termo é um fator externo, como **M** indicado no modelo acima.
  - `D` é
    - o índice de uma das variáveis criadas **P_index** (**lmivar**) **X**; P e Q serão obrigatórios.
    - o negativo do índice de uma das variáveis criadas, se a variável for usada transposta **X'**; P e Q serão obrigatórios.
    - zero, caso o bloco declarado não contenha nenhuma variável.
  - `P, Q` são fatores matriciais ou escalares que pré e pós-multiplicam o termo declarado. Exemplo: **P.X.Q**.
  - `F` é um parâmetro opcional, igual a **'s'**, indicando o caso em que o bloco aparece repetido transposto (simétrico). <br> Exemplo: **P.X.Q + Q'.X'.P'**.

- `LMI_SYS = getlmis()` captura o conjunto de LMIs declaradas para então resolvê-las.
- `decnbr(LMI_SYS)` retorna o número de variáveis do sistema.

## Exemplo completo

```matlab
A = [  0,    1,    0;
       0,    0,    1;
    -0.5, -0.4, -0.3];

B = [0,0,1]';
C = [1,1,0];

setlmis([]);

[P_index, n, matrix] = lmivar(1,[3,1]);
System = newlmi();


% LMI: [[A' * P * A - P + I < 0]]

lmiterm([ System, 1, 1, P_index], A', A)
lmiterm([ System, 1, 1, P_index], -1, 1)
lmiterm([ System, 1, 1,       0], eye(3))
lmiterm([-System, 2, 2, P_index],  1, 1)

LMIS = getlmis();

decnbr(LMIS)

cost = [1, 0, 0, 0, 0, 0];

% SOLVERS
%[t_min, x_opt] = feasp(LMIS); % t_min < 0 significa factibilidade
[cost_opt, x_opt] = mincx(LMIS, cost);

P = dec2mat(LMIS, x_opt, P_index);
```
