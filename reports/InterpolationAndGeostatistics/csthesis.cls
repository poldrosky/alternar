%%  $Id: csthesis.cls,v 1.2 2003/10/05 23:14:30 abuss Exp $
%%
%%    File : csthesis.cls    (LaTeX2e class file)
%%  Author : Antal Buss, Mauricio Heredia
%% Version : 0.1
%% 
%% This file contains a class definition, csthesis, for the LaTeX2e
%% system which defines the layout of theses which are submitted in
%% the Department of Computer Science at the University of Edinburgh.
%%
%% For information on this class, please refer to "texdoc csthesis"
%%
%% $Log: csthesis.cls,v $
%% Revision 1.2  2003/10/05 23:14:30  abuss
%% *** empty log message ***
%%
%%

\NeedsTeXFormat{LaTeX2e}[1994/12/01]
\ProvidesClass{csthesis}[1998/07/22 v0.1 Computer Science Thesis Class - PUJ]

%%
%% --- Initial Code ---
%%

\RequirePackage{ifthen}
\RequirePackage{vmargin}

\newcommand{\carrera}{INGENIERIA DE SISTEMAS Y COMPUTACION}
\newcommand{\titulo}{Ingeniero de Sistemas y Computaci\'on}
\newcommand{\carreramin}{Ingenier\'{\i}a de Sistemas y Computaci\'on}
\newcommand{\department}{FACULTAD DE INGENIERIA}
\newcommand{\university}{PONTIFICIA UNIVERSIDAD JAVERIANA}
\newcommand{\optar}{para optar el t\'{\i}tulo de}
\newcommand{\city}{SANTIAGO DE CALI}
\newcommand{\@chapteralignment}{\centering}
\newcommand{\draftmessage}{}
\newboolean{draftthesis}
\newboolean{usequotemarks}
\newboolean{usesinglespacing}
\newboolean{usedoublespacing}
\newboolean{usefullspacing}
\newboolean{usedeptreport}
\newboolean{useabbrevs}


%%
%%  --- Options ---
%%
%%  Current options: phd, mphil, msc, bsc, deptreport
%%                   draft
%%                   usequotes
%%                   singlespacing, doublespacing, fullspacing
%%                   centerchapter, leftchapter, rightchapter,
%%                   + all report.cls options
%%

% Modify by Mauricio Heredia R.
\DeclareOption{bsc}{\newcommand{\doctype}{Tesis de grado}}
\DeclareOption{ante}{\newcommand{\doctype}{Anteproyecto de grado}}

\newcommand{\degreetext} {\university\\ \department\\ \carrera}
\newcommand{\letrero} {\doctype~\optar\\ \titulo}
\newcommand{\letdirector} {Director}

\DeclareOption{centerchapter,centrechapter}
   {\renewcommand{\@chapteralignment}{\centering}}
\DeclareOption{leftchapter}
   {\renewcommand{\@chapteralignment}{\raggedright}}
\DeclareOption{rightchapter}
   {\renewcommand{\@chapteralignment}{\raggedleft}}

\DeclareOption{draft}{
   \setboolean{draftthesis}{true}
   \renewcommand{\draftmessage}{(Draft Copy)}}
\DeclareOption{usequotes}{\setboolean{usequotemarks}{true}}

\DeclareOption{abbrevs}{\setboolean{useabbrevs}{true}}

\DeclareOption{singlespacing}{\setboolean{usesinglespacing}{true}}
\DeclareOption{doublespacing}{\setboolean{usedoublespacing}{true}}
\DeclareOption{fullspacing}{\setboolean{usefullspacing}{true}}

\DeclareOption{deptreport}{\setboolean{usedeptreport}{true}}

\DeclareOption{parskip}{\AtEndOfClass{\input{parskip.clo}}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}

\ExecuteOptions{phd,centerchapter} % the default options
\ProcessOptions

%%
%% --- Class Loading (built ontop of report.cls) ---
%%

\LoadClass[letterpaper,12pt]{report}

%%
%% --- Main Code ---
%%

\newboolean{isspecialchapter}
\setboolean{isspecialchapter}{false}

%%
%% Hack to make minitoc work with csthesis. We declare a new chapter
%% variable called starchapter to be used by \addcontentsline when we
%% add contents lines for List of Figures/Tables. If we don't, then
%% minitoc treats the LOF/LOT sections as chapters of the thesis.
%%

\@ifundefined{chapter}{}{\let\l@starchapter\l@chapter}

%%
%% This bit will set up the header format for the thesis.
%% This currently uses a "headings" style showing the pagenumber
%% and chapter number/title. (in slanted text)
%%

\renewcommand{\chaptermark}[1]{\markboth{#1}{#1}}
\newcommand{\chapternoheader}{
  \ifthenelse{\boolean{isspecialchapter}}
    {}
    {\chaptername\ \thechapter\ \ ---\ }
}

\newcommand{\headfootstyle}{\normalsize}  % font size of headers and footers

\renewcommand{\ps@headings}{
  \renewcommand{\@oddfoot}{}
  \renewcommand{\@evenfoot}{}
  \renewcommand{\@evenhead}{\headfootstyle\thepage\hfil\sl\chapternoheader%
                            \leftmark\ \draftmessage}
  \renewcommand{\@oddhead}{\hskip -0.35em {\sl\headfootstyle\chapternoheader%
                           \rightmark\ \draftmessage}\hfil\thepage}
}

\renewcommand{\ps@plain}{
  \renewcommand{\@oddfoot}{\hfil\headfootstyle\thepage\hfil}
  \renewcommand{\@evenfoot}{\hfil\headfootstyle\thepage\hfil}
  \renewcommand{\@evenhead}{}
  \renewcommand{\@oddhead}{}
}

%%
%% And now setup that headings style as default
%%

\newcommand{\@textpagenumbering}{arabic}
\newcommand{\@preamblepagenumbering}{roman}
\newcommand{\@textpagestyle}{plain}
\newcommand{\@preamblepagestyle}{plain}


\pagestyle{\@preamblepagestyle}

\setcounter{secnumdepth}{6}

%%
%% Set up the default names for the various chapter headings
%%

\renewcommand{\contentsname}{CONTENIDO}
\renewcommand{\listfigurename}{LISTA DE FIGURAS}
\renewcommand{\listtablename}{LISTA DE CUADROS}
\newcommand{\listanexoname}{LISTA DE ANEXOS}
\renewcommand{\bibname}{Bibliograf'ia}
\renewcommand{\indexname}{Indicie}
\renewcommand{\abstractname}{Resumen}

%%
%% Some sundry commands which are generally useful...
%%

\ifthenelse{\boolean{useabbrevs}}
 {\RequirePackage{xspace}
  \newcommand{\NB}{N.B.\@\xspace}
  \newcommand{\eg}{e.g.\@\xspace}
  \newcommand{\Eg}{E.g.\@\xspace}
  \newcommand{\ie}{i.e.\@\xspace}
  \newcommand{\Ie}{I.e.\@\xspace}
  \newcommand{\etc}{etc.\@\xspace}
  \newcommand{\etal}{{\em et al}.\@\xspace}
  \newcommand{\etseq}{{\em et seq}.\@\xspace}
  \newcommand{\precis}{pr\'ecis\xspace}
  \newcommand{\Precis}{Pr\'ecis\xspace}
  \newcommand{\role}{r\^ole\xspace}
  \newcommand{\Role}{R\^ole\xspace}
  \newcommand{\naive}{na\"\i ve\xspace}
  \newcommand{\Naive}{Na\"\i ve\xspace}
  \newcommand{\tm}{\raisebox{1ex}{\tiny TM}\xspace}
  \newcommand{\cpright}{\raisebox{1ex}{\tiny\copyright}\xspace}
  \newcommand{\degrees}{\raisebox{1.2ex}{\tiny\ensuremath{\circ}}\xspace}}
 {}

%%
%% Set up the double spacing and provide commands to alter the
%% spacing for the subsequent text. By default, 1.5 spacing will be
%% used. This can be modified through the singlespacing, doublespacing
%% or draft class options.
%%

\ifthenelse{\boolean{usefullspacing}}
   {\newcommand{\doublespace}{\setlength{\baselineskip}{28.8pt}}
    \newcommand{\oneandahalfspace}{\setlength{\baselineskip}{21.6pt}}}
   {\newcommand{\doublespace}{\setlength{\baselineskip}{24pt}}
    \newcommand{\oneandahalfspace}{\setlength{\baselineskip}{18pt}}}
\newcommand{\singlespace}{\setlength{\baselineskip}{14.4pt}}

\ifthenelse{\boolean{draftthesis}}
   {\AtBeginDocument{\singlespace}\SetPrinterDraft}{
   \ifthenelse{\boolean{usesinglespacing}}
      {\AtBeginDocument{\singlespace}}{
      \ifthenelse{\boolean{usedoublespacing}}
         {\AtBeginDocument{\doublespace}}
         {\AtBeginDocument{\oneandahalfspace}}
   }
}

%%
%% When printing twosided, then the title page must be followed by
%% a blank page so that the thesis begins on the right-hand page. 
%% Also we must ensure that the thesis ends on a lef-hand page. We
%% do the latter by issuing a \cleardoublepage at the end of document.
%%

\newcommand{\cscleardoublepage}%
  {\vfill\pagebreak\thispagestyle{empty}\cleardoublepage}
\AtEndDocument{\cscleardoublepage}

%%
%% A couple of commands for figures/captions
%%

\newcommand{\thesiscaption}[3][]{
   \ifthenelse{\equal{#1}{}}
     {\parbox{5in}{\caption{{\em #2\/}}\label{#3}}}
     {\parbox{5in}{\caption[#1]{{\em #2\/}}\label{#3}}}
}

%%
%% Quotations are supposed to be in single-space, so we will
%% explicitly redefine the quotation env. to support this.
%% And introduce a citetext env. which can add an attribution.
%%

\renewenvironment{quotation}
   {\begin{quote}\singlespace
    \ifthenelse{\boolean{usequotemarks}}{``}{}\sl}
   {\ifthenelse{\boolean{usequotemarks}}{\rm''}{}\end{quote}}

\newcommand{\citationname}{}
\newenvironment{citetext}[1]
   {\renewcommand{\citationname}{#1}\begin{quote}\singlespace
    \ifthenelse{\boolean{usequotemarks}}{``}{}\sl}
   {\ifthenelse{\boolean{usequotemarks}}{\rm''}{}
    \hspace*{\fill}\nolinebreak[1]\hspace*{\fill}
    \rm (\citationname)\end{quote}}

%%
%% Let's have a dedication page so I can thank my mummy.
%%

\newcommand{\dedication}[1]
   {\titlepage\null\vspace{2.5in}
   \begin{flushleft}\raggedleft #1\end{flushleft}
%    \begin{center}#1\end{center}
    \par\vfil\null\endtitlepage\cscleardoublepage}


%%
%% Para las paginas con los anexos
%% 

\newenvironment{anexo}[2]
   {%\cscleardoublepage
    \ifthenelse{\equal {#1}{1}}{\addcontentsline{toc}{chapter}{ANEXOS}}{}
%ojo aqui
    \addcontentsline{loa}{section}{#2}
    \newpage
%    \null\vspace{2.5in}
 %   \par\vfil\null
    \begin{center}{\bf #2}\end{center}
%    \par\cscleardoublepage
%    {\Large #2} \vspace{0.7cm} \newline
    }
%    {\par\vfil\null} 



%%
%% Now let's redefine the abstract env. so that the title is 
%% comparable to other chapter headings. Also have abstract
%% start at top of page instead of floating in the middle
%%

\renewenvironment{abstract}
   {\cscleardoublepage\null\vspace{1cm}
    \begin{center}
       \bfseries \LARGE\abstractname
    \end{center}}
   {\par\vfil\null\cscleardoublepage}


%\renewenvironment{abstract}
%   {\titlepage\null\vspace{1cm}
%    \begin{center}
%       \bfseries \LARGE\abstractname
%    \end{center}}
%   {\par\vfil\null\endtitlepage}

%%
%% Based upon the above abstract env., provide wrappers for
%% an acknowledgements and declation env.
%%

\newenvironment{acknowledgements}
   {\renewcommand{\abstractname}{Agradecimientos}\begin{abstract}}
   {\end{abstract}\renewcommand{\abstractname}{Abstract}}   

\newenvironment{declaration}
   {\renewcommand{\abstractname}{Declaraci\'on}\begin{abstract}}
   {\end{abstract}\renewcommand{\abstractname}{Abstract}}   


\newcommand{\nullpage}[1]
   {\titlepage\null\vspace{2.5in}
 \begin{flushleft}#1\end{flushleft}
    \par\vfil\null\endtitlepage\cscleardoublepage}%\raggedright}



\newcommand{\art}
{  \titlepage\null\vspace{2.5in}
   \begin{flushleft}
   \raggedleft
   ARTICULO 23 de la Resoluci\'on No 13 del 6 de Julio de 1946\\
   del Reglamento de la Pontificia Universidad Javeriana.\\
   \vspace{0.2in}
   ``La Universidad no se hace responsable por los conceptos emitidos\\
   por sus alumnos en sus trabajos de Tesis. S\'olo velar\'a porque no se \\
   publique nada contrario al dogma y a la moral Cat\'olica y porque las\\
   Tesis no contengan ataques o pol\'emicas puramente personales;\\
   antes bien, se vea en ellas el anhelo de buscar la Verdad y la Justicia''\\
   \end{flushleft}\par\vfil\null\endtitlepage\cscleardoublepage
}



%%
%% Now we can redefine the chapter headings, with the flexibility
%% to choose whether we want the headings to be left, right or
%% centre justified. N.B. Most of this code is replicated from
%% the utthesis.sty style: version 1.0, (c) 1994 Dinesh Das
%%

\newcommand{\specialchapter}[1]{
   \chapter*{#1\@mkboth{\MakeUppercase#1}{\MakeUppercase#1}}
   \chaptermark{#1}
   \setboolean{isspecialchapter}{true}


}

\renewcommand{\chapter}{\clearpage
%   \thispagestyle{plain}   Se lo colca como comentario para que no sea obligatorio que los capitulos esten numerados
%   \setboolean{isspecialchapter}{false}
   \global\@topnum\z@
   \@afterindentfalse
   \secdef\@chapter\@schapter
   }

%%%
%%% Command from report.cls, (c) LaTeX3 Project.
%%%


\def\@chapter[#1]#2{\ifnum \c@secnumdepth >\m@ne
%                     Aumenta el numero
                      \refstepcounter{chapter}%
                      \typeout{\@chapapp\space\thechapter.}%
                      \addcontentsline{toc}{chapter}%
                             {\protect\numberline{\thechapter}#1}%
% deleted by mhr 
%                             {\@chapapp\ \protect\numberline{\thechapter}#1}%
                    \else
                      \addcontentsline{toc}{chapter}{\@chapapp\ #1}
                    \fi
                    \ifnum\value{chapter}=1\pagestyle{\@textpagestyle}\fi%
                    \chaptermark{#1}%
                    \addtocontents{lof}{\protect\addvspace{10\p@}}%
                    \addtocontents{lot}{\protect\addvspace{10\p@}}%
                    \addtocontents{loa}{\protect\addvspace{10\p@}}%
                    \@makechapterhead{#2}%
                    \@afterheading
                    }
%%%
%%% Command from report.cls, (c) LaTeX3 Project.
%%%

\def\@makechapterhead#1{%
 \vspace*{0cm} % Modifica la margen de los capitulos
  {\parindent \z@ \@chapteralignment \reset@font
    \ifnum \c@secnumdepth >\m@ne
%% modify by mhr
%      \normalsize\bfseries \@chapapp{} \thechapter%%%%%% Cambia el tamaño de los capitulos
      \normalsize\bfseries \thechapter%%%%%% Cambia el tamaño de los capitulos
% deleted by mhr
%      \par
%      \vskip 20\p@
    \fi
    \normalsize ~ \bfseries #1\par%%%%%% Cambia el tamaño de los capitulos
    \nobreak
    \vskip 40\p@
  }}
\def\@makeschapterhead#1{%
  \vspace*{0cm}% Modifica la margen de los capitulos especiales
  {\parindent \z@ \@chapteralignment
    \reset@font
    \normalsize\bfseries  #1\par%%%%%% No tocar, puede dañar las imagenes
    \nobreak
    \vskip 40\p@
  }}


%\newcommand{\setbibliographyheader}{
%   \chaptermark{\bibname}
%   \setboolean{isspecialchapter}{true}
%}

%%
%% Updated thebibliography environment. 
%% Modified from report.cls v1.3q (c) LaTeX3 Project.
%% Now includes entry in contents page & supports title rejustifying
%%

\renewenvironment{thebibliography}[1]
     {\specialchapter{\bibname}
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy\clubpenalty4000\widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}


\newenvironment{posiblebibliografia}[1]
     {\list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}}%
%      \sloppy\clubpenalty4000\widowpenalty4000%
%      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}


%%
%% Updated listoftables environment. 
%% Modified from report.cls v1.3q (c) LaTeX3 Project.
%% Now includes entry in contents page & supports title rejustifying
%%

\renewcommand\listoftables{%
    \chapter*{\listtablename
      \@mkboth{%
          \MakeUppercase\listtablename}{\MakeUppercase\listtablename}}%
%    \addcontentsline{toc}{starchapter}{\listtablename} 
    \@starttoc{lot}%
    }

%%
%% Updated listoffigures environment. 
%% Modified from report.cls v1.3q (c) LaTeX3 Project.
%% Now includes entry in contents page & supports title rejustifying
%%

\renewcommand\listoffigures{%
    \chapter*{\listfigurename
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}}%
%    \addcontentsline{toc}{starchapter}{\listfigurename}
    \@starttoc{lof}%
    }


%%
%% listofanexos environment. 
%% Created by mhr.
%% Now includes entry in contents page & supports title rejustifying
%%

\newcommand\listofanexos{%
    \chapter*{\listanexoname
      \@mkboth{%
          \MakeUppercase\listanexoname}{\MakeUppercase\listanexoname}}%
%     \addcontentsline{toc}{starchapter}{\listanexoname} 
    \@starttoc{loa}%
    }





\renewcommand\tableofcontents{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\contentsname
	\@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    \if@restonecol\twocolumn\fi
    }
\renewcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
    \endgroup
  \fi}
\renewcommand*\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
 
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}

\renewcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{2em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}

\renewcommand*\l@subsection[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}


%\renewcommand*\l@section{\@undottedtocline{1}{1.5em}{2.3em}}
%\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\renewcommand*\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\renewcommand*\l@paragraph{\@dottedtocline{4}{10em}{5em}}
\renewcommand*\l@subparagraph{\@dottedtocline{5}{12em}{6em}}

%%
%% Redefine the appendix command to ensure that it does a pagebreak
%% (sorts problem of Appendix appearing in header of last page before
%% the first apppendix).
%%

\renewcommand{\appendix}{\vfill\pagebreak
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \renewcommand\@chapapp{\appendixname}%
  \renewcommand\chaptername{\appendixname}%
  \renewcommand\thechapter{\@Alph\c@chapter}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Cambio el tamaño se secciones y subsecciones de Large y large a normal size %%%%%%%

\renewcommand\section{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\normalsize\bfseries}}
%\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
%                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
%                                     {1.5ex \@plus .2ex}%
%                                    {\normalfont\normalsize\bfseries}}

\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                      {-1em}%
                                     {\normalfont\normalsize\bfseries}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    {-1em}%
                                    {\normalfont\normalsize\bfseries}}
\renewcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {3.25ex \@plus1ex \@minus .2ex}%
                                       {-1em}%
                                      {\normalfont\normalsize\bfseries}}

%%
%% EOF: csthesis.cls
%%




