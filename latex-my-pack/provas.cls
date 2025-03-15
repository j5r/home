% Classe LaTeX de exemplo - provas.cls
%
%
% \title{Prova de Cálculo 1. \hfill 25 de Novembro de 2024.}
% \questao[2,5pt]
% \alternativa
% \vfx (assinalar verdadeiro / falso / X)
%
%

\ProvidesClass{provas}[2024/11/28 Classe de exemplo personalizada]
\LoadClass[12pt,a4paper]{article}

\setlength{\parskip}{4pt}
\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}

\makeatletter
\newcommand{\provastitulo}{\@title}
\makeatother

\newcommand{\senaovazio}[1]{
	\ifx #1\empty
	\else
		\noindent[#1]\;\;(\ignorespaces
	\fi
}

\newlength{\indentalternativa}
\setlength{\indentalternativa}{1cm}
\newlength{\indentvfx}
\setlength{\indentvfx}{1cm}

\newcounter{jrquestao}\setcounter{jrquestao}{0}
\newcommand{\questao}[1][]{
	\setcounter{jralternativa}{0}\stepcounter{jrquestao}\par\noindent\senaovazio{#1}Q.\thejrquestao)\;\;
}

\newcommand{\vfx}{\newline\hspace*{\indentvfx}(\;\;\;\;\;)\;\;}

\newcounter{jralternativa}\setcounter{jralternativa}{0}
\newcommand{\alternativa}{
	\stepcounter{jralternativa}\newline\hspace*{\indentalternativa}(\texttt{\alph{jralternativa}})\;\;
}




\AtBeginDocument{
	\begin{center}
		{\provastitulo}\par
		\fbox{\fbox{
				\begin{minipage}{.85\linewidth}\centering
					\;\\[8pt]
					Nome: \rule{10cm}{1pt}\quad Nota:\;\rule{1.5cm}{1pt}\\
					\;
				\end{minipage}
			}}
	\end{center}
}


\endinput
