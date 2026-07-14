#set page(
  paper: "us-letter",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.85em, spacing: 1.2em)

#show math.equation: set text(font: "New Computer Modern Math")

// Title block
#align(center)[
  #v(1.5em)
  #text(size: 14pt, weight: "bold")[Reply to \ Comment on "Multiparty quantum mutual information: An alternative definition"]
  #v(1em)
  #text(size: 11pt)[Asutosh Kumar]
  #v(0.3em)
  #text(size: 10pt, style: "italic")[asutoshk.phys\@gmail.com]
  #v(0.3em)
  #text(size: 10pt)[Department of Physics, Gaya College, Magadh University, Rampur, Gaya 823001, India]
  #v(1em)
]

// Abstract
#block(
  inset: (left: 2em, right: 2em),
  [
    #text(weight: "bold")[Abstract.]
    We reaffirm the claim of Lee _et al._ \[preceding Comment, Phys. Rev. A *108*, 066401 (2023)\] that the expression of quantum dual total correlation of a multipartite system in terms of quantum relative entropy as proposed in previous work \[A. Kumar, Phys. Rev. A *96*, 012332 (2017)\] is not correct. We provide alternate expression(s) of quantum dual total correlation in terms of quantum relative entropy. We, however, prescribe that in computing quantum dual total correlation one should use its expression in terms of von Neumann entropy.
  ]
)

#v(1.5em)

= Introduction

In Ref. @asu-qmi two different expressions of quantum dual total correlation were obtained: one in terms of von Neumann entropy and other in terms of quantum relative entropy. It was claimed that the two expressions are equivalent. In a comment @lee on Ref. @asu-qmi, Lee _et al._ have shown that the quantum dual total correlation of an $n$-partite quantum state cannot be represented as the quantum relative entropy between $(n - 1)$ copies of the quantum state and the product of $n$ different reduced quantum states for $n >= 3$. They arrived at this conclusion by considering explicitly the "support" condition of quantum relative entropy. Essentially, what Lee _et al._ have shown is that the following two expressions are not equal for $n >= 3$:

#v(0.5em)
$
I_n (rho) := sum_(k=1)^n S(rho_(overline(k))) - (n-1) S(rho),
$ <vn-ent>
#v(0.3em)

where $rho_(overline(k)) = op("tr")_k (rho)$ denotes the $(n-1)$-partite quantum state obtained by taking the partial trace on the $k^"th"$ party of $rho$, and

#v(0.5em)
$
J_n (rho) := S(rho^(times.circle (n-1)) || limits(times.circle)_(k=1)^n rho_(overline(k))),
$ <qr-ent1>
#v(0.3em)

where the quantum relative entropy is
$
S(tau || sigma) := cases(
  op("tr")(tau log tau) - op("tr")(tau log sigma) & "if" op("supp")(tau) subseteq op("supp")(sigma),
  infinity & "otherwise."
)
$

To justify their claim, authors provide two examples which imply that the above two expressions of $n$-partite quantum mutual information are not equivalent. $I_n (rho)$ in Eq. @vn-ent is non-negative and non-increasing under local CPTP maps @cerf, and therefore is a suitable monotonic measure of multi-partite correlations, while $J_n (rho)$ in Eq. @qr-ent1 is not.

= Reaffirming claim of Lee _et al._

The claim of Lee _et al._ is right. In this article we show analytically why the above two expressions are not equivalent. We begin with expression of $I_n (rho)$ [Eq. @vn-ent] and proceed to show that this is not equal to $J_n (rho)$ [Eq. @qr-ent1], as argued below.

#v(0.5em)
$
I_n (rho) &= sum_(k=1)^n S(rho_(overline(k))) - (n-1) S(rho) \
&= sum_(k=1)^n (S(rho_k) + S(rho_(overline(k))) - S(rho)) - (sum_(k=1)^n S(rho_k) - S(rho)) \
&= sum_(k=1)^n S(rho || rho_k times.circle rho_(overline(k))) - S(rho || limits(times.circle)_(k=1)^n rho_k) &#h(3em) & "(3)" \
&= S(rho^(times.circle n) || limits(times.circle)_(k=1)^n (rho_k times.circle rho_(overline(k)))) - S(rho || limits(times.circle)_(k=1)^n rho_k) &#h(3em) & "(4)" \
&attach(=, t: ?) #text(fill: blue)[$S(rho times.circle rho^(times.circle (n-1)) || (limits(times.circle)_(k=1)^n rho_k) times.circle (limits(times.circle)_(k=1)^n rho_(overline(k)))) - S(rho || limits(times.circle)_(k=1)^n rho_k)$] &#h(3em) & "(5)" \
&= S(rho || limits(times.circle)_(k=1)^n rho_k) + S(rho^(times.circle (n-1)) || limits(times.circle)_(k=1)^n rho_(overline(k))) - S(rho || limits(times.circle)_(k=1)^n rho_k) \
&= S(rho^(times.circle (n-1)) || limits(times.circle)_(k=1)^n rho_(overline(k))) = J_n (rho), &#h(3em) & "(6)"
$
#v(0.3em)

where quantum relative entropy in Eq. (3) and Eq. (4) is properly matched to satisfy the "support" condition in the sense that
$
S(rho || limits(times.circle)_(k=1)^n rho_k) &equiv S(rho_(12 dots n) || limits(times.circle)_(k=1)^n rho_k) \
S(rho || rho_k times.circle rho_(overline(k))) &equiv S(rho_(k overline(k)) || rho_k times.circle rho_(overline(k))) \
S(rho^(times.circle n) || limits(times.circle)_(k=1)^n (rho_k times.circle rho_(overline(k)))) &equiv S(rho_(12 dots n) times.circle rho_(23 dots n 1) times.circle dots times.circle rho_(n 1 dots (n-1)) || limits(times.circle)_(k=1)^n (rho_k times.circle rho_(overline(k)))),
$

where $overline(1) = 23 dots n$, $overline(2) = 34 dots n 1$ and $overline(k) = (k+1) dots n 1 dots (k-1)$. Eq. (3) and Eq. (4) are alternate expressions equivalent to Eq. @vn-ent in terms of quantum relative entropy. We, however, prescribe to use Eq. @vn-ent in computing quantum dual total correlation. Eq. (5) is not correct for two reasons: (i) noncommutativity of tensor product, and (ii) "matching" issue of subsystems. Therefore, we cannot arrive at Eq. (6).

= Second Rebuttal

Let us reconsider Eq. @qr-ent1 for $n=3$ explicitly.
$
J_3 (rho) &= S(rho^(times.circle 2) || limits(times.circle)_(k=1)^3 rho_(overline(k))) \
&= S(rho_(123) times.circle rho_(123) || rho_(23) times.circle rho_(31) times.circle rho_(12)). #h(3em) "(7)"
$

Here we see that the subsystems in the first and the second arguments of the quantum relative entropy are not properly matched. However, the subsystems in the above expression could be matched up if we adopt the following conventions: (i) interpret the first argument in the usual way, with the subsystems in their standard order and (ii) interpret the tensor product in the second argument with the values of $k$ running from $n$ to $1$. That is, for $n=3$, if we define
$
tilde(J)_3 (rho) &:= S(rho^(times.circle 2) || limits(times.circle)_(k=3)^1 rho_(overline(k))) \
&= S(rho_(123) times.circle rho_(123) || rho_(12) times.circle rho_(31) times.circle rho_(23)), #h(3em) "(8)"
$

then we see that the subsystems are properly matched. Now, let us adopt the following notations:
$
rho_(123)^(times.circle 2) &= rho_(123) times.circle rho_(123) equiv rho_(A_1 A_2 A_3) times.circle rho_(B_1 B_2 B_3) equiv rho_(123) times.circle rho_(456), #h(3em) "(9)" \
limits(times.circle)_(k=3)^1 rho_(overline(k)) &= rho_(12) times.circle rho_(31) times.circle rho_(23) equiv rho_(A_1 A_2) times.circle rho_(A_3 B_1) times.circle rho_(B_2 B_3) equiv rho_(12) times.circle rho_(34) times.circle rho_(56). #h(3em) "(10)"
$

Then, using notations in Eqs. (9, 10), one might attempt to show that Eq. (8) is equivalent to $I_3 (rho) = sum_(k=1)^3 S(rho_(overline(k))) - 2 S(rho)$ as argued below.
$
tilde(J)_3 (rho) &:= S(rho^(times.circle 2) || limits(times.circle)_(k=3)^1 rho_(overline(k))) \
&= S(rho_(123) times.circle rho_(123) || rho_(12) times.circle rho_(31) times.circle rho_(23)) \
&equiv S(rho_(123) times.circle rho_(456) || rho_(12) times.circle rho_(34) times.circle rho_(56)) \
&= - op("tr")(rho_(123) times.circle rho_(456) log(rho_(12) times.circle rho_(34) times.circle rho_(56))) + op("tr")(rho_(123) times.circle rho_(456) log(rho_(123) times.circle rho_(456))) \
&= - op("tr")(rho_(123) times.circle rho_(456) log(rho_(12) times.circle I_(34) times.circle I_(56))) - op("tr")(rho_(123) times.circle rho_(456) log(I_(12) times.circle rho_(34) times.circle I_(56))) \
&quad - op("tr")(rho_(123) times.circle rho_(456) log(I_(12) times.circle I_(34) times.circle rho_(56))) + op("tr")(rho_(123) times.circle rho_(456) log(rho_(123) times.circle I_(456))) + op("tr")(rho_(123) times.circle rho_(456) log(I_(123) times.circle rho_(456))) \
&= - op("tr")_(12)(rho_(12) log rho_(12)) #text(fill: blue)[$- op("tr")_(34)(rho_3 times.circle rho_4 log rho_(34))$] - op("tr")_(56)(rho_(56) log rho_(56)) + op("tr")_(123)(rho_(123) log rho_(123)) + op("tr")_(456)(rho_(456) log rho_(456)) \
&attach(=, t: ?) S(rho_(12)) + #text(fill: blue)[$S(rho_(34))$] + S(rho_(56)) - S(rho_(123)) - S(rho_(456)) #h(3em) "(11)" \
&equiv S(rho_(12)) + S(rho_(31)) + S(rho_(23)) - 2 S(rho_(123)) = I_3 (rho).
$

But this is not correct because the second term in Eq. (11) cannot be obtained from the previous equation.

Thus, even if we define quantum dual total correlation of a multipartite system in terms of quantum relative entropy alternatively as
$
tilde(J)_n (rho) := S(rho_(12 dots n)^(times.circle (n-1)) || limits(times.circle)_(k=n)^1 rho_(overline(k))),
$ <qr-ent2>

and use the notations as discussed above, Eq. @qr-ent2 is not equivalent to Eq. @vn-ent.

#v(1em)
*Acknowledgments.* AK is very thankful to Jaehak Lee, Gibeom Noh, Changsuk Noh and Jiyong Park for pointing out the subtle mistake in Ref. @asu-qmi.

#v(1em)

#bibliography("refs.bib", style: "numerical", title: "References")

// Since we can't use an actual .bib file, we'll render the references manually
#show bibliography: none

*References*

#v(0.5em)
#set par(hanging-indent: 2em)

\[1\] A. Kumar, _Multiparty quantum mutual information: An alternative definition_, #link("https://doi.org/10.1103/PhysRevA.96.012332")[Phys. Rev. A *96*, 012332 (2017)]. <asu-qmi>

\[2\] J. Lee, G. Noh, C. Noh and J. Park, _Comment on "Multiparty quantum mutual information: An alternative definition"_, #link("https://doi.org/10.1103/PhysRevA.108.066401")[Phys. Rev. A *108*(6), 066401 (2023)]. <lee>

\[3\] N. J. Cerf, S. Massar, and S. Schneider, _Multipartite classical and quantum secrecy monotones_, #link("https://doi.org/10.1103/PhysRevA.66.042309")[Phys. Rev. A *66*, 042309 (2002)]. <cerf>
