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

# Modelo Sigmoide

Um modelo 'populacional' muito conhecido pode ser empregado em diversas situações em que ocorre 'saturação', ou seja, estabilização no crescimento da população. Curvas com formato de "S" cumprem esse requisito, como o modelo abaixo. A função passa no ponto $(0, a/2)$ e sua saturação é em $a$ (a função cresce até o valor $a$).
\[f(x)= \dfrac{a}{1+e^{-bx}}.\]

Com $a=5$ e $b=0.8$, o gráfico fica assim:

<iframe src="https://www.desmos.com/calculator/k5hktyl3le?embed" width="500" height="500" style="border: 1px solid #ccc" frameborder=0></iframe>

<br><br><br>
Você pode utilizar o Octave [online](https://octave-online.net/) ou [offline](https://octave.org/download) para utilizar a função 
[sigmoide.m](https://github.com/j5r/home/blob/d0a173c071badf8da4eafd6a3210c38577665d90/arquivos/_diversos/sigmoide.m). Com ela, você pode passar alguns dados e verificar qual é o melhor valor para o parâmetro **b** para que a função fique melhor ajustada ao seus dados.
