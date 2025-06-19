<style>
    h1{color: #f38; border: 5px solid #fac; text-align:center; padding:8px; border-radius:10px;}
    h2{color:#3a8; font-weight:bold; background-color:#afe;border-radius:5px;padding:8px;}
    h3{color:blue; border-bottom:8px solid #aac;}
    h4{color:#c5c; font-style:italic; border-bottom:2px solid #caa;}
    //ul{color:red;}
</style>
<script>
MathJax = {
tex: {
inlineMath: [['$','$']],
displayMath: [['$$','$$'],['\[','\]']]
},/*
svg: {
fontCache: 'global'
}*/
};
</script>
<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>


# Fazendo música com matemática

Aqueles que já estudaram alguma coisa sobre música sabem que as notas musicais são ondas sonoras que vibram em frequências específicas. A título de informação, a nota mais utilizada para afinação de instrumentos é A4 (`"LÁ 4"`), cuja frequência é de 440Hz. A próxima nota `"LÁ"`  é A5 (`"LÁ 5"`), cuja frequência é de 880Hz, e assim por diante, sempre dobrando a frequência para obter A6, A7, etc.

Na música ocidental, cada **_oitava_** é dividida em 12 partes [1]. Não! **A música não tem 7 notas, mas sim, 12 notas!** Acontece que as 12 notas têm 7 nomes, com algumas variações de nomes. Na tabela abaixo, podes verificar isto com mais detalhes.


|       Nº        |   1   |   2    |   3    |   4    |   5    |   6    |   7    |   8    |   9    |   10   |   11   |   12   |  13   |
| :-------------: | :---: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :---: |
| Frequência (Hz) |  440  | 466.16 | 493.88 | 523.25 | 554.37 | 587.33 | 622.25 | 659.26 | 698.46 | 739.99 | 783.99 | 830.61 |  880  |
|      Sigla      |   A   |   A#   |   B    |   C    |   C#   |   D    |   D#   |   E    |   F    |   F#   |   G    |   G#   |   A   |
|      Nome       |  LÁ   |  LÁ#   |   SI   |   DÓ   |  DÓ#   |   RÉ   |  RÉ#   |   MI   |   FÁ   |  FÁ#   |  SOL   |  SOL#  |  LÁ   |
|        -        |   -   |   -    |   -    |   -    |   -    |   -    |   -    |   -    |   -    |   -    |   -    |   -    |   -   |
|   Outra sigla   |   -   |   Bb   |   Cb   |   B#   |   Db   |   -    |   Eb   |   Fb   |   E#   |   Gb   |   -    |   Ab   |   -   |
|   Outro nome    |   -   |  SIb   |  DÓb   |  SI#   |  RÉb   |   -    |  MIb   |  FÁb   |  MI#   |  SOLb  |   -    |  LÁb   |   -   |


[1] Oitava é o nome que se dá a um conjunto de notas em sequência, em que a primeira e a última nota são iguais em nome e diferentes em frequência, como as notas A4 e A5: são duas notas `"LÁ"`, mas com frequências 440Hz e 880Hz respectivamente.

Podemos criar uma função exponencial que gera essas frequências:
\[
F(x) = 440\cdot 2^{x/12}.
\]
Assim, $ F(0) $ nos dá a frequência 440Hz da nota A4, e $ F(12) $ nos dá a frequência 880Hz da nota A5, e cada um dos outros valores inteiros de $ x $ nos dá a frequência das outras notas, conforme a tabela acima. Como exemplo, $ F(9) \approx 698.46 $ que corresponde à nota F5.

Para criar uma nota musical, precisamos de uma onda com a frequência que desejamos. Para criá-la, recorreremos às funções periódicas, e mais especificamente, vamos utilizar uma função trigonométrica como seno ou cosseno.
