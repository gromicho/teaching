\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{abwlecture}[2026/09/01 Analytics for a Better World lecture slides]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass[aspectratio=169]{beamer}

\RequirePackage{fontspec}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,calc}
\RequirePackage{graphicx}
\RequirePackage{ragged2e}
\RequirePackage{hyperref}
\RequirePackage{xparse}
\RequirePackage{etoolbox}

\geometry{paperwidth=960bp,paperheight=540bp}
\setlength{\paperwidth}{960bp}
\setlength{\paperheight}{540bp}
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=0pt,text margin right=0pt}

\definecolor{ABWRed}{HTML}{BC0031}
\definecolor{ABWGray}{HTML}{7F7F7F}
\definecolor{ABWLinkBlue}{HTML}{0070C0}
\definecolor{ABWSoftGray}{HTML}{F1F1F1}
\definecolor{ABWOrange}{HTML}{E98300}
% Compatibility palette for accurately reconstructed legacy frames. New
% native components should prefer the semantic ABW colors above.
\definecolor{c000000}{HTML}{000000}
\definecolor{c002060}{HTML}{002060}
\definecolor{c003366}{HTML}{003366}
\definecolor{c0070C0}{HTML}{0070C0}
\definecolor{c00B050}{HTML}{00B050}
\definecolor{c00B0F0}{HTML}{00B0F0}
\definecolor{c101073}{HTML}{101073}
\definecolor{c141215}{HTML}{141215}
\definecolor{c171619}{HTML}{171619}
\definecolor{c1F1D21}{HTML}{1F1D21}
\definecolor{c257835}{HTML}{257835}
\definecolor{c4D4C4D}{HTML}{4D4C4D}
\definecolor{c595959}{HTML}{595959}
\definecolor{c7030A0}{HTML}{7030A0}
\definecolor{c751B68}{HTML}{751B68}
\definecolor{c7F7F7F}{HTML}{7F7F7F}
\definecolor{c87C0B5}{HTML}{87C0B5}
\definecolor{c898989}{HTML}{898989}
\definecolor{c92D050}{HTML}{92D050}
\definecolor{cA5CFC7}{HTML}{A5CFC7}
\definecolor{cBC0031}{HTML}{BC0031}
\definecolor{cBEB511}{HTML}{BEB511}
\definecolor{cBF7400}{HTML}{BF7400}
\definecolor{cBFBFBF}{HTML}{BFBFBF}
\definecolor{cC00000}{HTML}{C00000}
\definecolor{cC0504D}{HTML}{C0504D}
\definecolor{cD2CFD5}{HTML}{D2CFD5}
\definecolor{cDC0039}{HTML}{DC0039}
\definecolor{cE5D94F}{HTML}{E5D94F}
\definecolor{cF2F2F2}{HTML}{F2F2F2}
\definecolor{cFF0000}{HTML}{FF0000}
\definecolor{cFFC000}{HTML}{FFC000}
\definecolor{cFFFF00}{HTML}{FFFF00}
\definecolor{cFFFFFF}{HTML}{FFFFFF}
\hypersetup{colorlinks=true,urlcolor=ABWLinkBlue}

\IfFontExistsTF{Times New Roman}
  {\newfontfamily\TimesNR{Times New Roman}}
  {\newfontfamily\TimesNR{TeX Gyre Termes}}
\IfFontExistsTF{Calibri}
  {\newfontfamily\CalibriFont{Calibri}}
  {\newfontfamily\CalibriFont{Times New Roman}}
\IfFontExistsTF{Arial}
  {\newfontfamily\ArialFont{Arial}}
  {\newfontfamily\ArialFont{Times New Roman}}
\let\HelveticaFont\ArialFont

\newcommand{\ABWCrestPath}{assets/template/uva-crest.png}
\newcommand{\ABWFooterText}{Analytics for a Better World, Lecture 1}
\providecommand{\ABWSharedRoot}{.}
\NewDocumentCommand{\ABWSharedAsset}{m}{\ABWSharedRoot/assets/#1}
\NewDocumentCommand{\ABWSetSharedRoot}{m}{%
  \renewcommand{\ABWSharedRoot}{#1}%
  \ABWSetCrestPath{#1/assets/template/uva-crest.png}%
}
\NewDocumentCommand{\ABWSetCrestPath}{m}{\renewcommand{\ABWCrestPath}{#1}}
\NewDocumentCommand{\ABWSetFooterText}{m}{\renewcommand{\ABWFooterText}{#1}}

\newcommand{\ABWLogo}{%
  \begin{tikzpicture}[x=1bp,y=1bp,baseline=(current bounding box.north)]
    \path[use as bounding box] (0,0) rectangle (265.039,-69.864);
    \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (12,-13)
      {\includegraphics[width=28bp,height=30bp]{\ABWCrestPath}};
    \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (48,-11)
      {{\TimesNR\fontsize{15.5}{17}\selectfont\textsc{University of Amsterdam}}};
    \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (48,-31)
      {{\TimesNR\fontsize{15}{17}\selectfont Amsterdam Business School}};
  \end{tikzpicture}%
}

\NewDocumentCommand{\ABWTitle}{m}{%
  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (40.625,-55.791)
    {\begin{minipage}[t][69.584bp][c]{878.75bp}
       \setlength{\parindent}{0pt}\setlength{\parskip}{0pt}%
       {\TimesNR\fontsize{44}{49.28}\selectfont\color{ABWRed}\bfseries\raggedright #1\par}
     \end{minipage}};%
}

\NewDocumentCommand{\ABWFooter}{m}{%
  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (56.693,-499.702)
    {\begin{minipage}[t][11.952bp][c]{324bp}
       \setlength{\parindent}{0pt}\setlength{\parskip}{0pt}%
       {\TimesNR\fontsize{10}{11.2}\selectfont\color{ABWGray}\raggedright \ABWFooterText\par}
     \end{minipage}};%
  \ifstrempty{#1}{}{%
    \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (880.898,-499.702)
      {\begin{minipage}[t][11.952bp][c]{22.409bp}
         \setlength{\parindent}{0pt}\setlength{\parskip}{0pt}%
         {\TimesNR\fontsize{10}{11.2}\selectfont\color{ABWGray}\bfseries\raggedleft #1\par}
       \end{minipage}};%
  }%
}

% One consistent source/credit line for any frame that uses artwork.
\NewDocumentCommand{\ABWArtCredit}{m}{%
  \node[anchor=south west,inner sep=0pt,outer sep=0pt,text width=760bp]
    at (56.693,-487)
    {{\TimesNR\fontsize{9}{10.5}\selectfont\color{ABWGray}\raggedright #1\par}};%
}

% Base frame: owns the slide canvas and recurring UvA/ABS mark.
\NewDocumentEnvironment{abwframe}{O{} +b}{%
  \ifstrempty{#1}{\begin{frame}[plain]}{\begin{frame}[plain,#1]}%
  \begin{tikzpicture}[remember picture,overlay,x=1bp,y=1bp]
  \begin{scope}[shift={(current page.north west)}]
  \fill[white] (0,0) rectangle (960,-540);
  % Isolate slide-specific clipping and transforms.
  \begin{scope}
  #2
  \end{scope}
  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (4.819,-4.819)
    {\ABWLogo};
  \end{scope}
  \end{tikzpicture}
  \end{frame}
}{}

% Regular lecture content with shared title and footer geometry.
\NewDocumentEnvironment{abwstandardframe}{O{} m m +b}{%
  \begin{abwframe}[#1]
  \ABWTitle{#2}
  \ABWFooter{#3}
  #4
  \end{abwframe}
}{}

% Portrait layout. Geometry may be overridden for a portrait's prepared crop.
\pgfkeys{
  /abw/person/.is family,
  /abw/person,
  portrait x/.store in=\ABWPortraitX,
  portrait y/.store in=\ABWPortraitY,
  portrait width/.store in=\ABWPortraitWidth,
  portrait height/.store in=\ABWPortraitHeight,
  portrait x=583.148,
  portrait y=5.125,
  portrait width=376.852,
  portrait height=534.875
}
\NewDocumentEnvironment{abwpersonframe}{O{} m m m +b}{%
  \begingroup
  \pgfkeys{/abw/person,#1}
  \begin{abwframe}
  \node[anchor=north west,inner sep=0pt,outer sep=0pt]
    at (\ABWPortraitX,-\ABWPortraitY)
    {\includegraphics[width=\ABWPortraitWidth bp,height=\ABWPortraitHeight bp]{#3}};
  \ABWTitle{#2}
  \ABWFooter{#4}
  #5
  \end{abwframe}
  \endgroup
}{}

% Readable content helpers for person slides.
\pgfkeys{
  /abw/person text/.is family,
  /abw/person text,
  content x/.store in=\ABWPersonTextX,
  content y/.store in=\ABWPersonTextY,
  content width/.store in=\ABWPersonTextWidth,
  content height/.store in=\ABWPersonTextHeight,
  font size/.store in=\ABWPersonTextSize,
  line height/.store in=\ABWPersonTextLeading,
  content x=45,
  content y=145,
  content width=475,
  content height=345,
  font size=24,
  line height=26.88
}
\NewDocumentCommand{\ABWPersonText}{O{} +m}{%
  \begingroup
  \pgfkeys{/abw/person text,#1}
  \node[anchor=north west,inner sep=0pt,outer sep=0pt]
    at (\ABWPersonTextX,-\ABWPersonTextY)
    {\begin{minipage}[t][\ABWPersonTextHeight bp][t]{\ABWPersonTextWidth bp}
       \setlength{\parindent}{0pt}\setlength{\parskip}{0pt}%
       \TimesNR\fontsize{\ABWPersonTextSize}{\ABWPersonTextLeading}\selectfont\color{black}\raggedright
       #2
     \end{minipage}};%
  \endgroup
}
\NewDocumentCommand{\ABWPersonBullet}{m}{%
  \par\noindent\hangindent=22bp\hangafter=1%
  \makebox[22bp][l]{\char"2022}#1\par\vspace{7bp}%
}
\NewDocumentCommand{\ABWPlacedGraphic}{m m m m m}{%
  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (#1,-#2)
    {\includegraphics[width=#3bp,height=#4bp]{#5}};%
}
\NewDocumentCommand{\ABWPlacedLabel}{O{16} m m m m}{%
  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (#2,-#3)
    {\begin{minipage}[t]{#4bp}\TimesNR\fontsize{#1}{#1}\selectfont\raggedright #5\par\end{minipage}};%
}

% Semantic aliases make the intent of new slides visible in the source.
\NewDocumentEnvironment{abwquestionframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}
\NewDocumentEnvironment{abwanswerframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}
\NewDocumentEnvironment{abwfigureframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}

% Instructional structures are drawn as native objects in the source.
\NewDocumentEnvironment{abwlearningframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}
\NewDocumentEnvironment{abwrecapframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}

% Artwork frames always reserve and populate the standard attribution line.
\NewDocumentEnvironment{abwartframe}{O{} m m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #5
  \ABWArtCredit{#4}
  \end{abwstandardframe}
}{}

% Reusable native learning components; no flattened PowerPoint graphics.
\NewDocumentCommand{\ABWLearningCard}{m m m m m +m}{%
  \draw[rounded corners=8bp,fill=ABWSoftGray,draw=none]
    (#2,-#3) rectangle ++(#4,-#5);
  \fill[ABWRed] ($(#2,-#3)+(29,-31)$) circle[radius=18bp];
  \node[anchor=center,inner sep=0pt] at ($(#2,-#3)+(29,-31)$)
    {{\TimesNR\fontsize{18}{20}\selectfont\bfseries\color{white}#1}};
  \node[anchor=north west,inner sep=0pt,text width=\dimexpr#4bp-78bp\relax]
    at ($(#2,-#3)+(62,-16)$) {#6};%
}
\NewDocumentCommand{\ABWCardText}{m +m}{%
  {\TimesNR\fontsize{23}{26}\selectfont\bfseries #1\par}\vspace{4bp}%
  {\TimesNR\fontsize{18}{21}\selectfont #2\par}%
}
\NewDocumentCommand{\ABWJourneyStep}{m m m m}{%
  \fill[white,draw=ABWRed,line width=2bp] (#2,-235) circle[radius=31bp];
  \node[anchor=center,inner sep=0pt] at (#2,-235)
    {{\TimesNR\fontsize{23}{25}\selectfont\bfseries\color{ABWRed}#1}};
  \node[anchor=north,text width=190bp,align=center,inner sep=0pt]
    at (#2,-292) {{\TimesNR\fontsize{22}{24}\selectfont\bfseries #3}};
  \node[anchor=north,text width=190bp,align=center,inner sep=0pt]
    at (#2,-328) {{\TimesNR\fontsize{16}{19}\selectfont #4}};%
}
\NewDocumentCommand{\ABWRecapBar}{m m m}{%
  \draw[rounded corners=7bp,fill=ABWSoftGray,draw=none]
    (55,-#1) rectangle (905,-{#1+62});
  \fill[ABWRed] (87,-{#1+31}) circle[radius=16bp];
  \node[anchor=center,inner sep=0pt] at (87,-{#1+31})
    {{\TimesNR\fontsize{16}{18}\selectfont\bfseries\color{white}#2}};
  \node[anchor=west,text width=775bp,inner sep=0pt] at (122,-{#1+31})
    {{\TimesNR\fontsize{23}{26}\selectfont #3}};%
}
\NewDocumentEnvironment{abwtableframe}{O{} m m +b}{%
  \begin{abwstandardframe}[#1]{#2}{#3}
  #4
  \end{abwstandardframe}
}{}

% Section dividers use a larger centered heading while retaining deck chrome.
\NewDocumentEnvironment{abwsectionframe}{O{} m m +b}{%
  \begin{abwframe}[#1]
  \ABWFooter{#3}
  \node[anchor=center,inner sep=0pt,text width=820bp,align=center] at (480,-275)
    {{\TimesNR\fontsize{48}{54}\selectfont\bfseries\color{ABWRed}#2}};
  #4
  \end{abwframe}
}{}

% Title frames leave the right side available to the slide-specific artwork.
\NewDocumentEnvironment{abwtitleframe}{O{} m m m +b}{%
  \begin{abwframe}[#1]
  \node[anchor=north west,inner sep=0pt,text width=397.375bp] at (40.625,-186.227)
    {{\TimesNR\fontsize{44}{49.28}\selectfont\color{ABWRed}\bfseries\raggedright #2\par}};
  \node[anchor=north west,inner sep=0pt,text width=397.375bp] at (40.625,-150.371)
    {{\TimesNR\fontsize{22}{24.64}\selectfont\raggedright #3\par}};
  \node[anchor=north west,inner sep=0pt,text width=297.055bp] at (40.625,-457.518)
    {{\TimesNR\fontsize{18}{20.16}\selectfont\raggedright #4\par}};
  #5
  \end{abwframe}
}{}

