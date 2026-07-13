% copy of the private class for lualatex-doc, lltxdoc.sty. 2017 version.
% see lualatex-doc.tex for copying conditions
% Manuel Pégourié-Gonnard

\ProvidesClass{luameshdoc}

\LoadClass[a4paper]{scrartcl}
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{metalogo, xspace, ifmtarg, xargs, fancyvrb}
\RequirePackage[french]{babel}
\RequirePackage{enumitem}
\RequirePackage{biblatex}
\RequirePackage{tcolorbox,tikz}
\RequirePackage[colorlinks=true,
linkcolor=darkred,
urlcolor=darkred,
citecolor=darkred
]{hyperref}
%\RequirePackage{bookmark}

\defaultfontfeatures{Ligatures=TeX, Scale=MatchLowercase}
% \setmainfont{Linux Libertine O}
%\setmainfont{Slabo 27px}
\RequirePackage{libertinus-otf}
\setsansfont{Kurier}
\setmonofont[Scale=MatchLowercase]{Monaco}

\newcommand*\simplelogo [1] {%
  \ifcsname #1\endcsname \else \badlogocommand \fi
  \lowercase{\expandafter\simple@logo\expandafter{%
      \csname #1\expandafter\endcsname\expandafter}}\expandafter{%
    \csname #1\endcsname}{#1}}
\newcommand*\simple@logo [3] {%
  \newcommand #1 {#2\xspace}%
  \pdfstringdefDisableCommands{\def#1{#3\space}}}

\providecommand \ConTeXt    {Con\TeX{}t}
\providecommand \pdfTeX     {pdf\TeX}
\providecommand \TeXLive    {\TeX\thinspace Live}
\providecommand \MiKTeX     {MiK\TeX}
\newcommand\matapli{\Verb+matapli+}
\simplelogo {TeX}
\simplelogo {LaTeX}
\simplelogo {LuaTeX}
\simplelogo {LuaLaTeX}
\simplelogo {XeTeX}
\simplelogo {XeLaTeX}
\simplelogo {ConTeXt}
\simplelogo {pdfTeX}
\simplelogo {MiKTeX}
\simplelogo {TeXLive}

\colorlet{code}{blue!80!black}
\fvset{formatcom=\color{code}}
\DefineShortVerb|
\catcode`\  10 % non-breakable space

\newcommand*\email  [1] {<\href{mailto:#1}{#1}>}
\newcommand*\ctan   [1]
{\href{http://mirror.ctan.org/#1}{\nolinkurl{#1}}}
\newcommand \file       {\nolinkurl}
\newcommand*\note   [1] {\noindent\textsf{\bfseries #1.}\quad\ignorespaces}
\newcommand \cmd        {\texttt}
\newcommand \code   [1] {\texorpdfstring {\texttt{\color{code}#1}} {#1}}
\newcommand*\cs     [1] {\code{\textbackslash #1}}

\newcommandx*\para [2][2] {%
  \@ifmtarg{#2}{\para@{#1}{#1}}{\para@{#1}{#2}}}
\newcommand \para@ [2] {%
  \par \medskip
  \hypertarget{para.#2}{}%
  \belowpdfbookmark{#1}{para.#2}%
  \noindent
  \label{para.#2}%
  \makebox [0pt][r] {%
    \textsf{\bfseries #1\quad}}%
  \ignorespaces
}
\newcommandx*\pararef [3][1, 3] {%
  \@ifmtarg{#3}{\para@ref{#1}{#2}{#2}}{\para@ref{#1}{#2}{#3}}}
\newcommand \para@ref [3] {%
  \hyperlink{para.#3}{#1{#2}}}
\newcommand*\parapageref [1] {%
  \autopagref{para.#1}}

\newcommand \pf {\textsf}
\newcommand \pk {\pararef[\pf]}

\newcommandx*\pkdesc [6][6] {%
  \para                             {#1}
  \pkditem {Engines}                {#3}
  \pkditem {Formats}                {#4}
  \pkditem {Authors}            [\\]{#2}
  \pkditem {CTAN location}      [\\]{#5}[\ctan]
  \pkditem {Development url}    [\\]{#6}[\url]
  \newline
}
\newcommandx*\pkditem [4][2,4] {\@ifnotmtarg{#3}{%
    #2\textsf{\bfseries #1:} #4{#3}.%
  }}


\newenvironment{myquote}{%
  \list{}{\leftmargin0pt \rightmargin1em}%
\item\relax
  \small
}{%
  \endlist
}


\definecolor{darkred}{rgb}{0.8,0.1,0.1}


\newcommand*\commande{\par\bigskip%
  \noindent\hspace{-30pt}%
  \SaveVerb[aftersave={%
    \UseVerb{Vitem}
  }%
  ]{Vitem}}

\newcommand*\textme[1]{\textcolor{black}{\rmfamily\textit{#1}}}
\newcommand*\meta[1]{% % meta
  \textme{\ensuremath{\langle}#1\ensuremath{\rangle}}}
\newcommand*\optstar{% % optional star
  \meta{\ensuremath{*}}\xspace}
\DefineShortVerb{\|}
\newcommand\R{\mathbf{R}}
\setlength{\fboxsep}{2pt}
\fvset{%
  codes={\catcode`\«\active \catcode`\×\active },
  defineactive={\makefancyog\makefancytimes},
  formatcom=\color{darkred},
  frame=single
}
% rendre «...» équivalent à \meta{...}
{\catcode`\«\active
  \newcommandx\makefancyog[0][addprefix=\global]{%
    \def«##1»{\meta{##1}}}}
% rendre × équivalent à \optstar
{\catcode`\×\active
  \newcommandx\makefancytimes[0][addprefix=\global]{%
    \def×{\optstar{}}}}


\tcbuselibrary{listings,breakable}

\definecolor{vert}{rgb}{0.1,0.4,0.1}
\definecolor{bleu}{rgb}{0.1,0.1,0.4}
\lstset{
  numberstyle=\footnotesize\color{vert},
  keywordstyle=\ttfamily\bfseries\color{blue},
  basicstyle=\ttfamily\footnotesize,
  commentstyle=\itshape\color{vert},
  stringstyle=\ttfamily,
  showstringspaces=false,
  language=[LaTeX]TeX,
  breaklines=true,
  breakindent=30pt,
  defaultdialect=[LaTeX]TeX,
  morekeywords={buildMeshBW,buildMeshBWinc,drawPointsMesh,buildVoronoiBW,buildVoronoiBWinc,
    drawPointsMeshinc, meshAddPointBW,
    meshAddPointBWinc,drawGmsh,drawGmshinc,gmshVoronoi,gmshVoronoiinc}% frame=tb
}

\lstdefinelanguage{lua}
{morekeywords={for,end,function,do,if,else,elseif,then,
    tex.print,tex.sprint,io.read,io.open,string.find,string.explode,require},
  morecomment=[l]{--},
  morecomment=[s]{--[[}{]]},
  morestring=[b]''
}

\newtcblisting{Exemple}{%
  arc=0pt,outer arc=0pt,
  colback=red!2!white,
  colframe=red!75!black,
  breakable,
  boxsep=0pt,left=5pt,right=5pt,top=5pt,bottom=5pt, bottomtitle =
  3pt, toptitle=3pt,
  boxrule=0pt,bottomrule=0.5pt,toprule=0.5pt, toprule at break =
  0pt, bottomrule at break = 0pt,
  listing options={breaklines},
}

\newtcblisting{commandshell}{colback=black,colupper=white,colframe=black,
  arc=0pt,
  listing only,boxsep=0pt,listing
  options={style=tcblatex,language=sh},
  every listing line={\textcolor{red}{\small\ttfamily\bfseries user \$> }}}

\newtcblisting{latexcode}{
  arc=0pt,outer arc=0pt,
  colback=red!2!white,
  colframe=red!75!black,
  breakable,
  boxsep=0pt,left=5pt,right=5pt,top=5pt,bottom=5pt, bottomtitle =
  3pt, toptitle=3pt,
  boxrule=0pt,bottomrule=0.5pt,toprule=0.5pt, toprule at break =
  0pt, bottomrule at break = 0pt,
  listing only,boxsep=0pt,listing
  options={breaklines}
}



\newenvironment{optionsenum}[1][]
{\begin{description}[font=\color{darkred}\ttfamily]}
  {\end{description}}

\newenvironment{warning}{%
  \setlength{\logowidth}{24pt}
  \tcbset{%
    arc=0pt,outer arc=0pt,colback=gray!10!white,colframe=gray!60!white,
    boxsep=0pt,left=5pt,right=5pt,top=5pt,bottom=5pt, bottomtitle = 3pt, toptitle=3pt,
    boxrule=0pt,bottomrule=0.5pt,toprule=0.5pt}
  \medskip
  \begin{tcolorbox}%
    \begin{wrapfigure}[2]{L}{17pt}%
      % \raisebox{-5pt}{
      \vspace*{-0.55cm}
      \bcinfo
      % }%
    \end{wrapfigure}
  }%
  {\end{tcolorbox}\medskip}

\lstset{moredelim=*[s][\color{red}\rmfamily\itshape]{<}{>}}
\lstset{moredelim=*[s][\color{blue}\rmfamily\itshape]{<<}{>>}}
