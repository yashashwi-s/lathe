#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Equation Sample 4]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(0.5em)

$
  lr(||f||)_(1_mu) + lr(||g||)_(1_mu)
  &= integral_(x in cal(D)) |f(x)| + |g(x)| dif mu(x) \

  &= + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) >= 0, g(x) >= 0,$)) f(x) + g(x) dif mu(x)
  - integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) < 0, g(x) < 0,$)) f(x) + g(x) dif mu(x) \

  & quad + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) >= 0, g(x) < 0,$)) f(x) - g(x) dif mu(x)
  + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) < 0, g(x) >= 0,$)) g(x) - f(x) dif mu(x) \

  &= + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) >= 0, g(x) >= 0,$)) max(f(x), g(x)) + min(f(x), g(x)) dif mu(x) \

  & quad - integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) < 0, g(x) < 0,$)) max(f(x), g(x)) + min(f(x), g(x)) dif mu(x) \

  & quad + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) >= 0, g(x) < 0,$)) max(f(x), g(x)) - min(f(x), g(x)) dif mu(x) \

  & quad + integral_(#stack(dir: ttb, $x in cal(D)$, $f(x) < 0, g(x) >= 0,$)) max(f(x), g(x)) - min(f(x), g(x)) dif mu(x). \
$
