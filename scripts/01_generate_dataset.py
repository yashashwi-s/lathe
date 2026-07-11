import os
import csv
from pathlib import Path

DATA_DIR = Path("data")

CATEGORIES = [
    ("01_prose", "Plain prose / paragraphs (no math)"),
    ("02_eq_simple", "Standalone equations, simple"),
    ("03_eq_hard", "Standalone equations, hard/dense"),
    ("04_paper_full", "Full real-world papers (with source)"),
    ("05_paper_small", "Full papers, small manual batch"),
    ("06_tables_simple", "Tables (simple)"),
    ("07_tables_complex", "Tables (complex: multirow/multicolumn, multi-page)"),
    ("08_algorithms", "Algorithms / pseudocode"),
    ("09_tikz_simple", "Simple TikZ diagrams"),
    ("10_tikz_complex", "Complex TikZ"),
    ("11_pgfplots", "PGFPlots (data/scientific plots)"),
    ("12_cv_simple", "Resumes/CVs, simple single-column"),
    ("13_cv_complex", "Resumes/CVs, complex multi-column"),
    ("14_posters", "Posters (large-format, dense figure+text)"),
    ("15_beamer", "Beamer slides / presentations"),
]

SAMPLES = {
    "01_prose": [
        ("easy.tex", "easy", r"""\documentclass{article}
\begin{document}
Recent advancements in large language models have demonstrated unprecedented capabilities across diverse natural language processing tasks. This rapid progress challenges traditional paradigms of linguistic analysis and demands robust evaluation frameworks to systematically assess model reasoning, factuality, and potential biases in zero-shot contexts.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\begin{document}
\section{Background}
The integration of transformer architectures has revolutionized sequential data modeling.
\subsection{Key Components}
\begin{itemize}
    \item \textbf{Self-Attention:} Enables the model to weigh the significance of different words within the input sequence.
    \item \textit{Positional Encoding:} Injects crucial sequence order information directly into the input embeddings.
\end{itemize}
These components act in synergy to capture long-range dependencies efficiently.
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{hyperref}
\begin{document}
\section{Methodology}\label{sec:methodology}
As discussed in Section~\ref{sec:methodology}, our approach leverages deep reinforcement learning\footnote{Specifically, Proximal Policy Optimization (PPO).} to align outputs with human preferences. 
\subsection{Data Processing}
The corpus is tokenized using \texttt{Byte-Pair Encoding} (BPE) with a vocabulary size of 50,257.
\begin{quote}
"Alignment remains one of the most critical open problems in modern artificial intelligence, bridging the gap between raw computational capability and safe, intended utility."
\end{quote}
\end{document}"""),
    ],
    "02_eq_simple": [
        ("easy.tex", "easy", r"""\documentclass{article}
\begin{document}
The relationship between mass and energy is defined as $E = mc^2$, where $c$ represents the speed of light in a vacuum.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\begin{document}
The Gaussian integral over the real line is remarkably elegant:
\begin{equation}
\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}
\end{equation}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\begin{document}
The Taylor series expansion of a real or complex-valued function $f(x)$ about the point $x=a$ is given by:
\begin{equation}
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x-a)^n
\end{equation}
\end{document}"""),
    ],
    "03_eq_hard": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}
The system of linear equations can be represented as:
\begin{align}
3x + 2y - z &= 1 \\
2x - 2y + 4z &= -2 \\
-x + \frac{1}{2}y - z &= 0
\end{align}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}
Applying the Cauchy-Schwarz inequality yields:
\begin{align*}
\left( \sum_{k=1}^n a_k b_k \right)^2 &\leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right) \\
&= \| \mathbf{a} \|^2 \| \mathbf{b} \|^2
\end{align*}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}
The inverse of the partitioned block matrix is defined using the Schur complement:
\[
\begin{pmatrix}
A & B \\
C & D
\end{pmatrix}^{-1}
=
\begin{pmatrix}
A^{-1} + A^{-1}B(D - CA^{-1}B)^{-1}CA^{-1} & -A^{-1}B(D - CA^{-1}B)^{-1} \\
-(D - CA^{-1}B)^{-1}CA^{-1} & (D - CA^{-1}B)^{-1}
\end{pmatrix}
\]
\end{document}"""),
    ],
    "04_paper_full": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{amsmath}
\title{Quantum Entanglement in Bipartite Systems}
\author{Dr. Alice \and Dr. Bob}
\begin{document}
\maketitle
\begin{abstract}
We explore the fundamental properties of quantum entanglement in simplified bipartite systems, focusing on Bell state inequalities and information-theoretic interpretations.
\end{abstract}
\section{Introduction}
Quantum entanglement describes a physical phenomenon where pairs or groups of particles interact in ways such that the quantum state of each particle cannot be described independently.
\section{Theoretical Framework}
Let $\mathcal{H}_A$ and $\mathcal{H}_B$ be Hilbert spaces. The composite system is $\mathcal{H}_A \otimes \mathcal{H}_B$.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{amsmath, graphicx}
\begin{document}
\section{Experimental Results}
Our measurements indicate a clear violation of the CHSH inequality, as demonstrated in the primary experimental apparatus.
\begin{figure}[h]
\centering
\rule{4cm}{3cm}
\caption{Schematic representation of the spontaneous parametric down-conversion setup.}
\end{figure}
The correlation coefficient $S = 2.82 \pm 0.03$ heavily favors the quantum mechanical predictions over local hidden variable theories.
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{amsmath, graphicx, hyperref}
\begin{document}
\section{Introduction}
The resolution of the black hole information paradox remains a profound challenge in theoretical physics \cite{hawking1976}. Recent developments in AdS/CFT correspondence suggest unitary evolution is preserved.
\section{Holographic Entanglement Entropy}
The Ryu-Takayanagi formula relates the entanglement entropy $S_A$ to the area of a minimal surface $\gamma_A$:
\begin{equation}
S_A = \frac{\text{Area}(\gamma_A)}{4G_N}
\end{equation}
\begin{thebibliography}{9}
\bibitem{hawking1976}
Hawking, S. W. (1976). Breakdown of predictability in gravitational collapse. \textit{Physical Review D}, 14(10), 2460.
\end{thebibliography}
\end{document}"""),
    ],
    "05_paper_small": [
        ("easy.tex", "easy", r"""\documentclass{article}
\begin{document}
\section{Discussion and Conclusion}
The empirical data strongly corroborates our initial hypothesis regarding thermal conductivity at cryogenic temperatures. Future work will extend this analysis to high-temperature superconducting cuprates.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\begin{document}
\section{Limitations of the Study}
\subsection{Sample Size Constraints}
While the effect size was statistically significant ($p < 0.01$), the limited cohort size ($N=45$) restricts the generalizability of our findings across diverse demographic populations.
\subsection{Measurement Artifacts}
Signal attenuation in the fiber optic relay introduced minor, albeit non-negligible, baseline drift during the prolonged observation windows.
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\begin{document}
\twocolumn
\section{Optimization Topologies}
In this section, we transition to a two-column layout to efficiently present the dual nature of the gradient descent pathways. 
The right column typically contains supplementary derivations, while the left focuses on the primary narrative trajectory of the optimization landscape constraints.
\end{document}"""),
    ],
    "06_tables_simple": [
        ("easy.tex", "easy", r"""\documentclass{article}
\begin{document}
\begin{tabular}{|c|c|c|}
\hline
Dataset & Accuracy (\%) & Latency (ms) \\
\hline
MNIST & 99.2 & 12 \\
CIFAR-10 & 95.8 & 45 \\
ImageNet & 88.4 & 120 \\
\hline
\end{tabular}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\begin{document}
\begin{tabular}{l c r}
\textbf{Hyperparameter} & \textbf{Value} & \textbf{Impact} \\
Learning Rate & $3 \times 10^{-4}$ & High \\
Batch Size & 256 & Moderate \\
Weight Decay & $0.01$ & Low \\
\end{tabular}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\begin{document}
\begin{table}[h]
\centering
\begin{tabular}{ccc}
\textbf{Model Architecture} & \textbf{Parameters (M)} & \textbf{Throughput (seq/s)} \\
Transformer-Base & 110 & 2450 \\
Transformer-Large & 340 & 890 \\
\end{tabular}
\caption{Inference performance metrics across model scales.}
\end{table}
\end{document}"""),
    ],
    "07_tables_complex": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{multirow}
\begin{document}
\begin{tabular}{|c|c|c|}
\hline
\multirow{2}{*}{Phase} & \multicolumn{2}{c|}{Duration (hours)} \\
 & Expected & Actual \\
\hline
Setup & 2.0 & 2.5 \\
Execution & 12.0 & 11.5 \\
Analysis & 4.0 & 5.0 \\
\hline
\end{tabular}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{booktabs}
\begin{document}
\begin{tabular}{llrr}
\toprule
Family & Species & Mass (kg) & Lifespan (yrs) \\
\midrule
Felidae & Panthera leo & 190.0 & 14 \\
Canidae & Canis lupus & 40.0 & 8 \\
Ursidae & Ursus arctos & 300.0 & 25 \\
\bottomrule
\end{tabular}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{multirow}
\usepackage{booktabs}
\begin{document}
\begin{tabular}{llrr}
\toprule
\multicolumn{2}{c}{Taxonomy} & \multicolumn{2}{c}{Metrics} \\
\cmidrule(r){1-2} \cmidrule(l){3-4}
Class & Order & Avg. Weight (g) & Avg. Length (cm) \\
\midrule
\multirow{2}{*}{Aves}      & Passeriformes & 45.2 & 15.4 \\
                           & Strigiformes  & 1200.5 & 45.0 \\
Mammalia                   & Rodentia      & 25.4 & 10.2 \\
\bottomrule
\end{tabular}
\end{document}"""),
    ],
    "08_algorithms": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{algorithm}
\usepackage{algpseudocode}
\begin{document}
\begin{algorithm}
\caption{Simple Variable Assignment}
\begin{algorithmic}
\State $counter \gets 0$
\State $total \gets \sum_{i=1}^{10} i$
\end{algorithmic}
\end{algorithm}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{algorithm}
\usepackage{algpseudocode}
\begin{document}
\begin{algorithm}
\caption{Binary Search Validation}
\begin{algorithmic}
\If{$target = array[mid]$}
    \State \textbf{return} $mid$
\ElsIf{$target < array[mid]$}
    \State $high \gets mid - 1$
\Else
    \State $low \gets mid + 1$
\EndIf
\end{algorithmic}
\end{algorithm}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{algorithm}
\usepackage{algpseudocode}
\begin{document}
\begin{algorithm}
\caption{Euclidean Algorithm for GCD}\label{alg:gcd}
\begin{algorithmic}[1]
\Require $a, b \geq 0$ and not both zero
\Ensure $gcd = \text{greatest common divisor of } a, b$
\State $x \gets a$
\State $y \gets b$
\While{$y \neq 0$}
    \State $r \gets x \bmod y$
    \State $x \gets y$
    \State $y \gets r$
\EndWhile
\State \textbf{return} $x$
\end{algorithmic}
\end{algorithm}
\end{document}"""),
    ],
    "09_tikz_simple": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
\draw[thick, blue] (0,0) -- (3,2);
\draw[thick, red] (0,2) -- (3,0);
\end{tikzpicture}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
\draw[fill=blue!20] (0,0) rectangle (4,2);
\draw[fill=red!20] (2,1) circle (0.8);
\node at (2,1) {\textbf{Center}};
\end{tikzpicture}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=1.5, thick]
\draw[->] (-1,0) -- (3,0) node[right] {$x$-axis};
\draw[->] (0,-1) -- (0,3) node[above] {$y$-axis};
\draw[domain=0:2.5, smooth, variable=\x, red] plot ({\x}, {\x*\x/2}) node[right] {$f(x) = \frac{x^2}{2}$};
\end{tikzpicture}
\end{document}"""),
    ],
    "10_tikz_complex": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{decorations.pathmorphing, arrows.meta}
\begin{document}
\begin{tikzpicture}[decoration={coil,aspect=0.3,segment length=2mm,amplitude=2mm}]
\draw [decorate, -{Stealth[length=3mm]}] (0,0) -- (4,0);
\node[above] at (2, 0.3) {Spring Force};
\end{tikzpicture}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{positioning}
\begin{document}
\begin{tikzpicture}[node distance=2cm, auto, every node/.style={draw, rectangle, fill=blue!10, minimum height=1cm, text centered}]
\node (A) {Input Data};
\node (B) [right=of A] {Feature Extraction};
\node (C) [right=of B] {Classification};
\draw[->, thick] (A) -- (B);
\draw[->, thick] (B) -- (C);
\end{tikzpicture}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
\foreach \i in {1,...,5} {
    \foreach \j in {1,...,\i} {
        \node[draw, circle, inner sep=2pt, fill=black] at (\j - \i/2, -\i*0.8) {};
    }
}
\node[above] at (0, -0.5) {Pascal's Triangle Structure};
\end{tikzpicture}
\end{document}"""),
    ],
    "11_pgfplots": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{axis}[grid=major, width=8cm, height=6cm]
\addplot[domain=-5:5, samples=50, color=blue, thick] {sin(deg(x))};
\end{axis}
\end{tikzpicture}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
    xlabel={Time (s)},
    ylabel={Voltage (V)},
    legend pos=north west
]
\addplot[color=red, mark=square*] coordinates {
    (0,0) (1,2.1) (2,3.5) (3,4.2) (4,4.8)
};
\addlegendentry{Experimental}
\end{axis}
\end{tikzpicture}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
    view={60}{30},
    xlabel=$x$, ylabel=$y$, zlabel=$z$,
    colormap/viridis,
    grid=major
]
\addplot3[surf, domain=-2:2, domain y=-2:2, samples=20] 
    {exp(-x^2-y^2)};
\end{axis}
\end{tikzpicture}
\end{document}"""),
    ],
    "12_cv_simple": [
        ("easy.tex", "easy", r"""\documentclass{article}
\begin{document}
\begin{center}
{\LARGE \textbf{Eleanor Rigby}} \\
\vspace{2mm}
eleanor.rigby@abbeyroad.com | (555) 123-4567 | London, UK
\end{center}
\vspace{5mm}
\noindent Dedicated community organizer and architectural observer with 10 years of experience in localized demographic studies.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\begin{document}
\section*{Alexander Hamilton}
ahamilton@treasury.gov | New York, NY
\hrule
\vspace{3mm}
\subsection*{Education}
\textbf{King's College (Columbia University)} \hfill 1774 - 1776 \\
Studies in Mathematics and Law
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\begin{document}
\begin{center}
\LARGE \textbf{Marie Curie} \\
\normalsize mcurie@sorbonne.fr | Paris, France
\end{center}
\section*{Professional Experience}
\textbf{University of Paris} \hfill 1906 - 1934 \\
\textit{Professor of General Physics}
\begin{itemize}
    \item First woman to become a professor at the University of Paris.
    \item Directed the Radium Institute, conducting pioneering research on radioactivity.
\end{itemize}
\end{document}"""),
    ],
    "13_cv_complex": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage[margin=1in]{geometry}
\begin{document}
\noindent\begin{minipage}{0.6\textwidth}
{\Large \textbf{Dr. Alan Turing}} \\
Theoretical Computer Scientist
\end{minipage}
\begin{minipage}{0.4\textwidth}
\raggedleft
Bletchley Park, UK \\
aturing@enigma.gov
\end{minipage}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage[margin=1in]{geometry}
\begin{document}
\noindent\begin{minipage}{0.5\textwidth}
\textbf{Ada Lovelace} \\
Analytical Engine Programmer
\end{minipage}%
\begin{minipage}{0.5\textwidth}
\raggedleft
ada@babbage.co.uk \\
London, UK
\end{minipage}
\vspace{5mm}
\hrule
\vspace{2mm}
\textbf{Skills:} Algorithm Design, Bernoulli Numbers, Visionary Computation
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage{tabularx}
\usepackage{geometry}
\geometry{margin=1in}
\begin{document}
\noindent
\begin{tabularx}{\textwidth}{@{}X r@{}}
{\LARGE \textbf{Grace Hopper}} & ghopper@navy.mil \\
Rear Admiral, US Navy & Arlington, VA \\
\end{tabularx}
\vspace{3mm}
\hrule
\vspace{3mm}
\noindent
\begin{tabularx}{\textwidth}{@{}l X@{}}
\textbf{1952} & Invented the first operational compiler (A-0 System). \\
\textbf{1959} & Served as technical consultant on the CODASYL committee, leading to the creation of COBOL. \\
\end{tabularx}
\end{document}"""),
    ],
    "14_posters": [
        ("easy.tex", "easy", r"""\documentclass{article}
\usepackage[a0paper, margin=4cm]{geometry}
\begin{document}
\Huge
\begin{center}
\textbf{Analysis of Deep Ocean Currents}
\end{center}
\vspace{2cm}
\Large
A preliminary study on the effects of salinity variations in the Marianas Trench.
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{article}
\usepackage[a0paper, margin=4cm]{geometry}
\begin{document}
\Huge
\begin{center}
\textbf{CRISPR-Cas9 Gene Editing Efficacy} \\
\vspace{1cm}
\Large Dr. Jane Smith, Dr. John Doe \\
\normalsize Institute for Biological Research
\end{center}
\vspace{4cm}
\section*{Abstract}
We demonstrate a 98\% cleavage efficiency in target sequences using our modified gRNA vectors.
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{article}
\usepackage[a0paper, margin=4cm]{geometry}
\usepackage{multicol}
\begin{document}
\begin{center}
\Huge \textbf{Advancements in Solid-State Battery Technologies} \\
\Large Energy Research Laboratory
\end{center}
\vspace{2cm}
\Large
\begin{multicols}{3}
\section*{Introduction}
Solid-state electrolytes offer significant safety advantages over volatile liquid counterparts.
\section*{Methodology}
We synthesized a lithium-lanthanum-zirconium-oxide (LLZO) ceramic membrane.
\section*{Results}
Ionic conductivity reached $10^{-3}$ S/cm at room temperature.
\end{multicols}
\end{document}"""),
    ],
    "15_beamer": [
        ("easy.tex", "easy", r"""\documentclass{beamer}
\begin{document}
\begin{frame}
\frametitle{Project Kickoff}
Welcome to the initial presentation for the Q3 development cycle. We will outline milestones and deliverables.
\end{frame}
\end{document}"""),
        ("medium.tex", "medium", r"""\documentclass{beamer}
\begin{document}
\begin{frame}
\frametitle{Strategic Objectives}
\begin{itemize}
\item Increase operational efficiency by 15\%.
\item Deploy the new microservices architecture to production.
\item Expand our user testing cohort across European markets.
\end{itemize}
\end{frame}
\end{document}"""),
        ("hard.tex", "hard", r"""\documentclass{beamer}
\title{Quarterly Financial Review}
\author{CFO Office}
\begin{document}
\begin{frame}
\titlepage
\end{frame}
\begin{frame}
\frametitle{Revenue Breakdown}
\begin{block}{Q2 Highlights}
Software licensing revenue grew by 22\% year-over-year, largely driven by enterprise renewals.
\end{block}
\begin{alertblock}{Risk Factors}
Hardware supply chain disruptions present a continuous challenge through Q3.
\end{alertblock}
\end{frame}
\end{document}"""),
    ],
}

def main():
    DATA_DIR.mkdir(exist_ok=True)
    manifest = []
    
    for cat_dir, cat_name in CATEGORIES:
        d = DATA_DIR / cat_dir
        d.mkdir(exist_ok=True)
        
        samples = SAMPLES.get(cat_dir, [])
        for fname, difficulty, content in samples:
            fpath = d / fname
            fpath.write_text(content)
            
            manifest.append({
                "category": cat_dir,
                "category_name": cat_name,
                "filename": fname,
                "difficulty": difficulty,
                "path": str(fpath)
            })
            
    with open("data/manifest.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "category_name", "filename", "difficulty", "path"])
        writer.writeheader()
        writer.writerows(manifest)
        
    print(f"Generated {len(manifest)} samples across {len(CATEGORIES)} categories.")

if __name__ == "__main__":
    main()
