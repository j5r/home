%                                      By Junior R Ribeiro; junho 03, 2025
%
% Esta funcao tem o objetivo de calcular o parametro 'b' do modelo
% "sigmoide" abaixo, baseando-se nos dados coletados 'x' e 'y'.
%        f(x) =         a
%                ----------------
%                 1 + e^( -bx )
% A curva sigmoide acima eh uma curva com formato de "S", que, em x=0 passa
% em y=a/2 e que, a medida em que x cresce, a curva vai crescendo e se
% aproximando de 'a'.
%
% Para utilizar esta funcao, o parametro 'a' deve ser informado (valor de
% saturacao), bem como os dados 'x' e 'y'. A funcao calculara o parametro
% 'b' para o modelo e gerarah dois graficos em pdf contendo informacoes do
% modelo e o erro quadratico associado.
%
% A implementacao segue o metodo matematico dos minimos quadrados, que
% resulta em resolver a seguinte equacao:
%
% SOMA(i) x(i) * y(i) * ( e^(-b*x(i)) + e^(-2*b*x(i)) ) =
%
%         = a * SOMA(i) x(i) * e^(-b*x(i))
%
%  em que x(i) e y(i) sao os dados conhecidos.
%
%  [melhor_b] = sigmoide(a, x, y, numero_tentativas*)
%        *numero_tentativas eh opcional. Se nao for informado, farei
%         numero_tentativas = 1000.
%

function [melhor_b] = sigmoide(a, x, y, numero_tentativas)
if nargin < 4
    numero_tentativas = 1000;
end
MAX = numero_tentativas;
assert(numel(x)==numel(y),...
    sprintf('x e y devem ter o mesmo numero de elementos!\nnumel(x)=%d, numel(y)=%d.',...
    numel(x),numel(y)));
%% configs
tolerancia_do_erro = 1e-8;
erros_b = zeros(MAX,2);
erro_anterior = inf;
tentativa = 0;
b = 1e-1; % valor inicial para b.
%%
while tentativa < MAX
    tentativa = tentativa + 1;
    
    %% lhs e rhs (membro esquerdo=lhs, membro direito=rhs)
    %
    % preciso aproximar a igualdade o maximo possivel, modificando b
    %
    % sum(x.*y.*(exp(-b*x)+exp(-2*b*x))) = A*sum(x.*exp(-b*x))
    %
    lhs = sum(x .* y .*  (exp(-b*x) + exp(-2*b*x))   );
    rhs = a * sum(x .* exp(-b*x));
    
    erro = (rhs-lhs)^2; % erro quadratico que desejo minimizar
    erros_b(tentativa,:) = [erro, b]; % armazenando os valores do erro e de b
    
    if erro < tolerancia_do_erro
        fprintf('O erro foi bem pequeno, menor que %.6f.\n',tolerancia_do_erro);
        fprintf('a = %.6f,   b = %.6f.\n',a,b); % se o erro for bem pequeno
        break
    end
    if erro_anterior < erro
        % se o erro aumentou, diminua b
        b = b*0.8;
    else
        % se o erro diminuiu, aumente b
        b = b*1.2;
    end
    erro_anterior = erro;
end

[~,indice] = min(erros_b(:,1));
melhor_b = erros_b(indice,2);
plot(erros_b(:,2),erros_b(:,1),'b*',melhor_b,erros_b(indice,1),'*r');
xlabel('valor de b');
ylabel('valor do erro^2');
title({sprintf('O valor de [b] com menor erro quadratico eh b=%.6f',melhor_b),''});
saveas(1,'erro.pdf')

figure
plot(x,y,'*');
hold on
dom = linspace(min(x),max(x),300);
im = a./(1+exp(-melhor_b*dom));
plot(dom,im,'-');
legend('Dados','Modelo ajustado','Location','southeast')
titulo = sprintf('O modelo ajustado eh: $f(x)=\\frac{%.f}{1+e^{-%.6f x}}$',a,melhor_b);
xlabel('x');
ylabel('f(x)'); grid;
t =title(titulo,'Interpreter','latex');
set(t,'fontsize',18);
hold off
saveas(2,'modelo.pdf')
end