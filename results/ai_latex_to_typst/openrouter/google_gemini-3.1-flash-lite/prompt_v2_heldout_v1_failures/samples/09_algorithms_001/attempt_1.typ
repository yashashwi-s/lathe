#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 1]
  #v(0.5em)
  Source-backed Image2Struct algorithm sample
])

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  caption: [Source-backed algorithmic procedure],
  block[
    #set par(leading: 1em)
    For $t$ in $\{-1, ..., -T^{traceback}\}$: // Initialization of $\delta_t^{turned\_on}$ and $\delta_t^{turned\_off}$
    #h(2em) $\delta_t^{turned\_on} <- 0$
    #h(2em) $\delta_t^{turned\_off} <- 0$
    #h(2em) If $S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1$: // Replace by $S_{u,t}^{OFF} - S_{t-1}^{OFF} = 1$ if STOP is not defined.
    #h(4em) $\delta_t^{turned\_off} <- 1$
    #h(2em) Else If $S_{u,t}^{START} - S_{t-1}^{START} = 1$: // Replace by $S_{u,t}^{OFF} - S_{t-1}^{OFF} = -1$ if START is not defined.
    #h(4em) $\delta_t^{turned\_on} <- 1$

    For $t$ in $\{-1, ..., -T^{traceback}\}$: // Initialization of $\delta_t^{stable}$, $\delta_t^{entered\_up}$ and $\delta_t^{entered\_down}$
    #h(2em) $\delta_t^{stable} <- 0$
    #h(2em) $\delta_t^{entered\_up} <- 0$
    #h(2em) $\delta_t^{entered\_down} <- 0$
    #h(2em) If $S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1$:
    #h(4em) $\delta_t^{stable} <- 1$
    #h(2em) Else If $S_{u,t}^{ON\_UP} - S_{t-1}^{ON\_UP} = 1$:
    #h(4em) $\delta_t^{entered\_up} <- 1$
    #h(2em) Else If $S_{u,t}^{ON\_UP} - S_{t-1}^{ON\_UP} = 1$:
    #h(4em) $\delta_t^{entered\_down} <- 1$

    For $t$ in $\{-1, ..., -T^{traceback}\}$: // Initialization of $\delta_t^{stable}$, $\delta_t^{entered\_up}$ and $\delta_t^{entered\_down}$
    #h(2em) $\delta_t^{stable} <- 0$
    #h(2em)
