from pathlib import Path
root = Path(__file__).resolve().parents[1] / 'slides' / 'source-faithful'
files = {
'14-analytics-definition.tex': r'''\begin{abwframe}
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (40.625,-56.693) {\begin{minipage}[t][68.682bp][c]{878.75bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{44}{49.28}\selectfont\color{cBC0031}\bfseries\raggedright Analytics\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (193.2,-120.924) {\begin{minipage}[t][211.689bp][t]{579.6bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\ArialFont\fontsize{32}{35.84}\selectfont\color{c003366}\centering “The scientific process of transforming data into insight for making better decisions”\par}{\ArialFont\fontsize{12}{13.44}\selectfont\color{c003366}\itshape\vphantom{Ag}\par}{\ArialFont\fontsize{20}{22.4}\selectfont\color{c003366}\itshape\vphantom{Ag}\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (408,-312.482) {\href{https://www.informs.org/Explore/Operations-Research-Analytics}{\includegraphics[width=162bp,height=61.047bp]{assets/visuals/lecture-1/informs-analytics-definition-logo.png}}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (286,-388) {{\ArialFont\fontsize{9}{11}\selectfont\color{c7F7F7F}\href{https://www.informs.org/Explore/Operations-Research-Analytics}{Definition adapted from INFORMS.}}};
\ABWFooter{\insertframenumber}
\end{abwframe}
''',
'16-covid-descriptive.tex': r'''\begin{abwframe}
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (40.625,-56.693) {\begin{minipage}[t][68.682bp][c]{878.75bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{44}{49.28}\selectfont\color{cBC0031}\bfseries\raggedright Covid-19 example\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (394.951,-150.932) {\href{https://ourworldindata.org/coronavirus}{\includegraphics[width=515.963bp,height=364.209bp]{assets/visuals/lecture-1/covid-descriptive-analytics-case.png}}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (104.222,-237.339) {\begin{minipage}[t][87.314bp][t]{301.236bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{36}{40.32}\selectfont\color{c000000}\raggedright Descriptive Analytics\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (104,-343) {{\ArialFont\fontsize{9}{11}\selectfont\color{c7F7F7F}\href{https://ourworldindata.org/coronavirus}{Historical COVID-19 example; current data and source details: Our World in Data.}}};
\ABWFooter{\insertframenumber}
\end{abwframe}
''',
'18-covid-predictive.tex': r'''\begin{abwframe}
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (40.625,-56.693) {\begin{minipage}[t][68.682bp][c]{878.75bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{44}{49.28}\selectfont\color{cBC0031}\bfseries\raggedright Covid-19 example\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (610.939,-69.188) {\begin{minipage}[t][43.692bp][t]{301.236bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{36}{40.32}\selectfont\color{c000000}\raggedright Predictive Analytics\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (230.771,-125.375) {\href{https://epirisk.net/}{\includegraphics[width=680.39bp,height=357.205bp]{assets/visuals/lecture-1/covid-predictive-analytics-case.png}}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (80,-425) {{\ArialFont\fontsize{9}{11}\selectfont\color{c7F7F7F}\href{https://epirisk.net/}{Historical scenario visual: EpiRisk. Explore current assumptions and outputs online.}}};
\ABWFooter{\insertframenumber}
\end{abwframe}
''',
'36-dark-side.tex': r'''\begin{abwframe}
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (26.406,-82.893) {\begin{minipage}[t][73.709bp][c]{878.677bp}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}{\TimesNR\fontsize{44}{49.28}\selectfont\color{cBC0031}\bfseries\raggedright Dark side of Analytics…\par}\end{minipage}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (582.059,-48.873) {\href{https://weaponsofmathdestructionbook.com/}{\includegraphics[width=295.916bp,height=453.594bp]{assets/visuals/lecture-1/slide-37-dark-side-of-analytics-visual-01.png}}};
\node[anchor=north west,inner sep=0pt,outer sep=0pt] at (55,-438) {{\ArialFont\fontsize{9}{11}\selectfont\color{c7F7F7F}\href{https://weaponsofmathdestructionbook.com/}{Cover: Cathy O'Neil, \emph{Weapons of Math Destruction} (2016).}}};
\ABWFooter{\insertframenumber}
\end{abwframe}
'''
}
for name, content in files.items(): (root/name).write_text(content, encoding='utf-8')
print('Rebuilt', ', '.join(files))
