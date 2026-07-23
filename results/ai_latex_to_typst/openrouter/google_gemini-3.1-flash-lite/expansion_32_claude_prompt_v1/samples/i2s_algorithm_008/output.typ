#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "linux libertine")

#align(center)[
  #text(size: 1.44em, weight: "bold")[Algorithm Sample 8] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #v(1em)
]

= Procedure
The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#block(stroke: (top: 0.5pt, bottom: 0.5pt), inset: (y: 0.5em))[
  #align(center)[*Algorithm: Delta Particle Filter*]
  #v(0.5em)
  #set enum(numbering: "1.")
  #enum(
    [Input: data $y_{1:T}$, level $l in NN$, particle number $N in NN$ and parameter $theta in Theta$.],
    [Initialize: For $i in {1, dots, N}$, independently generate $overline(W)_(Delta_l:1)^(i,l)$ from $cal(N)(0, Delta_l)$. For $(i,k) in {1, dots, N} times {1, dots, Delta_(l-1)^(-1)}$ set
    $
    overline(W)_(k Delta_(l-1))^(i,l-1) = overline(W)_(2k Delta_l)^(i,l) + overline(W)_((2k-1) Delta_l)^(i,l).
    $
    Set $t=1$, $hat(tilde(p))^N(y_{1:0})=1$ for convention and go to step 3.],
    [Iterate: For $i in {1, dots, N}$ compute
    $
    tilde(u)_t^i = frac(max{kappa_(t,l)(overline(w)_(Delta_l:t)^(i,l)), kappa_(t,l-1)(overline(w)_(Delta_(l-1):t)^(i,l-1))}, sum_(j=1)^N max{kappa_(t,l)(overline(w)_(Delta_l:t)^(j,l)), kappa_(t,l-1)(overline(w)_(Delta_(l-1):t)^(j,l-1))}).
    $
    Set $hat(p)^N(y_{1:t}) = hat(p)^N(y_{1:t-1}) dot 1/N sum_(i=1)^N max{kappa_(t,l)(overline(w)_(Delta_l:t)^(i,l)), kappa_(t,l-1)(overline(w)_(Delta_(l-1):t)^(i,l-1))}$.
    Then sample $(overline(w)_(Delta_l:t)^(1:N,l), overline(w)_(Delta_(l-1):t)^(1:N,l-1))$ with replacement from
    $(overline(w)_(Delta_l:t)^(1:N,l), overline(w)_(Delta_(l-1):t)^(1:N,l-1))$
    using probabilities
    $tilde(u)_t^(1:N)$. For $i in {1, dots, N}$, independently generate $overline(W)_(t+Delta_l:t+1)^i$ from $cal(N)(0, Delta_l)$. For $(i,k) in {1, dots, N} times {1, dots, Delta_(l-1)^(-1)}$ set
    $
    overline(W)_(t+k Delta_(l-1))^(i,l-1) = overline(W)_(t+2k Delta_l)^(i,l) + overline(W)_(t+(2k-1) Delta_l)^(i,l).
    $
    Set $t=t+1$ and if $t=T$ go to step 4, otherwise restart step 3.],
    [Grand Selection: For $i in {1, dots, N}$ compute
    $
    tilde(u)_T^i = frac(max{kappa_(T,l)(overline(w)_(Delta_l:T)^(i,l)), kappa_(T,l-1)(overline(w)_(Delta_(l-1):T)^(i,l-1))}, sum_(j=1)^N max{kappa_(T,l)(overline(w)_(Delta_l:T)^(j,l)), kappa_(T,l-1)(overline(w)_(Delta_(l-1):T)^(j,l-1))}).
    $
    Set $hat(p)^N(y_{1:T}) = hat(p)^N(y_{1:T-1}) dot 1/N sum_(i=1)^N max{kappa_(T,l)(overline(w)_(Delta_l:T)^(i,l)), kappa_(T,l-1)(overline(w)_(Delta_(l-1):T)^(i,l-1))}$.
    Sample one $(overline(w)_(Delta_l:T)^l, overline(w)_(Delta_(l-1):T)^(l-1))$ from $(overline(w)_(Delta_l:T)^(1:N,l), overline(w)_(Delta_(l-1):T)^(1:N,l-1))$ using $tilde(u)_T^(1:N)$ and go to step 5.],
    [Output: trajectories $(overline(w)_(Delta_l:T)^l, overline(w)_(Delta_(l-1):T)^(l-1))$ and normalizing constant estimate $hat(tilde(p))^N(y_{1:T})$.]
  )
]
