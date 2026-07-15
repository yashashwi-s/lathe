#let margin_x = sys.inputs.at("margin_x", default: "1.1in")
#let margin_y = sys.inputs.at("margin_y", default: "1.0in")
#let fontsize = eval(sys.inputs.at("fontsize", default: "11pt"))
#let leading = eval(sys.inputs.at("leading", default: "0.9em"))

#set page(
  paper: "us-letter",
  margin: (x: eval(margin_x), y: eval(margin_y)),
)
#set text(font: ("TeX Gyre Pagella", "Palatino"), size: fontsize)
#set par(justify: true, leading: leading, first-line-indent: 1.5em, spacing: 1.0em)
#show math.equation: set text(size: fontsize)
#set math.equation(numbering: "(1)")

#let S = math.italic("S")
#let tr = math.italic("tr")
#let supp = math.italic("supp")

// Title page
#align(center)[
  #v(0.3em)
  #text(size: 1.1em, weight: "bold")[Reply to \ Comment on "Multiparty quantum mutual information: An alternative definition"]

  #v(0.8em)
  Asutosh Kumar#super[1,\*]

  #v(0.5em)
  #super[1]#emph[Department of Physics, Gaya College, Magadh University, Rampur, Gaya 823001, India]
]

#v(0.5em)

#block[
  #set par(first-line-indent: 1.5em)
  We reaffirm the claim of Lee #emph[et al.] [preceding Comment, Phys. Rev. A *108*, 066401 (2023)] that the expression of quantum dual total correlation of a multipartite system in terms of quantum relative entropy as proposed in previous work [A. Kumar, Phys. Rev. A *96*, 012332 (2017)] is not correct. We provide alternate expression(s) of quantum dual total correlation in terms of quantum relative entropy. We, however, prescribe that in computing quantum dual total correlation one should use its expression in terms of von Neumann entropy.
]

#place(bottom + left, dx: 0.5in)[
  #line(length: 1in, stroke: 0.4pt) \
  #super[\*] asutoshk.phys\@gmail.com
]

#pagebreak()

= Introduction

In Ref. [1] two different expressions of quantum dual total correlation were obtained: one in terms of von Neumann entropy and other in terms of quantum relative entropy. It was claimed that the two expressions are equivalent. In a comment [2] on Ref. [1], Lee #emph[et al.] have shown that the quantum dual total correlation of an $n$-partite quantum state cannot be represented as the quantum relative entropy between $(n - 1)$ copies of the quantum state and the product of $n$ different reduced quantum states for $n >= 3$. They arrived at this conclusion by considering explicitly the "support" condition of quantum relative entropy. Essentially, what Lee #emph[et al.] have shown is that the following two expressions are not equal for $n >= 3$:

$ I_n (rho) := sum_(k=1)^n S(rho_(overline(k))) - (n-1) S(rho), $ <vn-ent>

where $rho_(overline(k)) = tr_k (rho)$ denotes the $(n-1)$-partite quantum state obtained by taking the partial trace on the $k^(t h)$ party of $rho$, and

$ J_n (rho) := S(rho^(⊗ (n-1)) || ⊗_(k=1)^n rho_(overline(k))), $ <qr-ent1>

where the quantum relative entropy is

$ S(tau || sigma) := cases(
  tr(tau log tau) - tr(tau log sigma) & "if " supp(tau) subset.eq supp(sigma),
  infinity & "otherwise."
) $

To justify their claim, authors provide two examples which imply that the above two expressions of $n$-partite quantum mutual information are not equivalent. $I_n (rho)$ in Eq. (1) is non-negative and non-increasing under local CPTP maps [3], and therefore is a suitable monotonic measure of multi-partite correlations, while $J_n (rho)$ in Eq. (2) is not.

= Reaffirming claim of Lee #emph[et al.]

The claim of Lee #emph[et al.] is right. In this article we show analytically why the above two expressions are not equivalent. We begin with expression of $I_n (rho)$ [Eq. (1)] and proceed to show that this is not equal to $J_n (rho)$ [Eq. (2)], as argued below.

$ I_n (rho) &= sum_(k=1)^n S(rho_(overline(k))) - (n-1) S(rho) \
&= sum_(k=1)^n (S(rho_k) + S(rho_(overline(k))) - S(rho)) - (sum_(k=1)^n S(rho_k) - S(rho)) \
&= sum_(k=1)^n S(rho || rho_k ⊗ rho_(overline(k))) - S(rho || ⊗_(k=1)^n rho_k) \
&= S(rho^(⊗ n) || ⊗_(k=1)^n (rho_k ⊗ rho_(overline(k)))) - S(rho || ⊗_(k=1)^n rho_k) \
&scripts(=)^? #text(fill: blue)[$S(rho ⊗ rho^(⊗ (n-1)) || (⊗_(k=1)^n thin rho_k) ⊗ (⊗_(k=1)^n thin rho_(overline(k))))$] - S(rho || ⊗_(k=1)^n rho_k) \
&= S(rho || ⊗_(k=1)^n rho_k) + S(rho^(⊗ (n-1)) || ⊗_(k=1)^n rho_(overline(k))) - S(rho || ⊗_(k=1)^n rho_k) \
&= S(rho^(⊗ (n-1)) || ⊗_(k=1)^n rho_(overline(k))) = J_n (rho), $

where quantum relative entropy in Eq. (3) and Eq. (4) is properly matched to satisfy the "support" condition in the sense that

$ S(rho || ⊗_(k=1)^n rho_k) &equiv S(rho_(1 2 dots.c n) || ⊗_(k=1)^n rho_k) \
S(rho || rho_k ⊗ rho_(overline(k))) &equiv S(rho_(k overline(k)) || rho_k ⊗ rho_(overline(k))) \
S(rho^(⊗ n) || ⊗_(k=1)^n (rho_k ⊗ rho_(overline(k)))) &equiv S(rho_(1 2 dots.c n) ⊗ rho_(2 3 dots.c n 1) ⊗ dots.c ⊗ rho_(n 1 dots.c (n-1)) || ⊗_(k=1)^n (rho_k ⊗ rho_(overline(k)))), $

where $overline(1) = 2 3 dots.c n$, $overline(2) = 3 4 dots.c n 1$ and $overline(k) = (k+1) dots.c n 1 dots.c (k-1)$. Eq. (3) and Eq. (4) are alternate expressions equivalent to Eq. (1) in terms of quantum relative entropy. We, however, prescribe to use Eq. (1) in computing quantum dual total correlation. Eq. (5) is not correct for two reasons: (i) noncommutativity of tensor product, and (ii) "matching" issue of subsystems. Therefore, we cannot arrive at Eq. (8).

= Second Rebuttal

Let us reconsider Eq. (2) for $n=3$ explicitly.

$ J_3 (rho) &= S(rho^(⊗ 2) || ⊗_(k=1)^3 rho_(overline(k))) \
&= S(rho_(123) ⊗ rho_(123) || rho_(23) ⊗ rho_(31) ⊗ rho_(12)). $

Here we see that the subsystems in the first and the second arguments of the quantum relative entropy are not properly matched. However, the subsystems in the above expression could be matched up if we adopt the following conventions: (i) interpret the first argument in the usual way, with the subsystems in their standard order and (ii) interpret the tensor product in the second argument with the values of $k$ running from $n$ to $1$. That is, for $n=3$, if we define

$ tilde(J)_3 (rho) &:= S(rho^(⊗ 2) || ⊗_(k=3)^1 rho_(overline(k))) \
&= S(rho_(123) ⊗ rho_(123) || rho_(12) ⊗ rho_(31) ⊗ rho_(23)), $

then we see that the subsystems are properly matched. Now, let us adopt the following notations:

$ rho_(123)^(⊗ 2) &= rho_(123) ⊗ rho_(123) equiv rho_(A_1 A_2 A_3) ⊗ rho_(B_1 B_2 B_3) equiv rho_(123) ⊗ rho_(456), \
⊗_(k=3)^1 rho_(overline(k)) &= rho_(12) ⊗ rho_(31) ⊗ rho_(23) equiv rho_(A_1 A_2) ⊗ rho_(A_3 B_1) ⊗ rho_(B_2 B_3) equiv rho_(12) ⊗ rho_(34) ⊗ rho_(56). $

Then, using notations in Eqs. (11, 12), one might attempt to show that Eq. (10) is equivalent to $I_3 (rho) = sum_(k=1)^3 S(rho_(overline(k))) - 2 S(rho)$ as argued below.

$ tilde(J)_3 (rho) &:= S(rho^(⊗ 2) || ⊗_(k=3)^1 rho_(overline(k))) \
&= S(rho_(123) ⊗ rho_(123) || rho_(12) ⊗ rho_(31) ⊗ rho_(23)) \
&equiv S(rho_(123) ⊗ rho_(456) || rho_(12) ⊗ rho_(34) ⊗ rho_(56)) \
&= -tr(rho_(123) ⊗ rho_(456) log(rho_(12) ⊗ rho_(34) ⊗ rho_(56))) + tr(rho_(123) ⊗ rho_(456) log(rho_(123) ⊗ rho_(456))) \
&= -tr(rho_(123) ⊗ rho_(456) log(rho_(12) ⊗ I_(34) ⊗ I_(56))) - tr(rho_(123) ⊗ rho_(456) log(I_(12) ⊗ rho_(34) ⊗ I_(56))) \
&- tr(rho_(123) ⊗ rho_(456) log(I_(12) ⊗ I_(34) ⊗ rho_(56))) + tr(rho_(123) ⊗ rho_(456) log(rho_(123) ⊗ I_(456))) + tr(rho_(123) ⊗ rho_(456) log(I_(123) ⊗ rho_(456))) \
&= -tr_(12)(rho_(12) log rho_(12)) #text(fill: blue)[$- tr_(34)(rho_3 ⊗ rho_4 log rho_(34))$] - tr_(56)(rho_(56) log rho_(56)) + tr_(123)(rho_(123) log rho_(123)) + tr_(456)(rho_(456) log rho_(456)) \
&scripts(=)^? S(rho_(12)) + #text(fill: blue)[$S(rho_(34))$] + S(rho_(56)) - S(rho_(123)) - S(rho_(456)) \
&equiv S(rho_(12)) + S(rho_(31)) + S(rho_(23)) - 2 S(rho_(123)) = I_3 (rho). $

But this is not correct because the second term in Eq. (13) cannot be obtained from the previous equation.

Thus, even if we define quantum dual total correlation of a multipartite system in terms of quantum relative entropy alternatively as

$ tilde(J)_n (rho) := S(rho_(1 2 dots.c n)^(⊗ (n-1)) || ⊗_(k=n)^1 rho_(overline(k))), $

and use the notations as discussed above, Eq. (14) is not equivalent to Eq. (1).

#v(1em)
#align(center)[*Acknowledgments*]

AK is very thankful to Jaehak Lee, Gibeom Noh, Changsuk Noh and Jiyong Park for pointing out the subtle mistake in Ref. [1].

#v(1em)

[1] A. Kumar, #emph[Multiparty quantum mutual information: An alternative definition], Phys. Rev. A *96*, 012332 (2017).

[2] J. Lee, G. Noh, C. Noh and J. Park, #emph[Comment on "Multiparty quantum mutual information: An alternative definition"], Phys. Rev. A *108(6)*, 066401 (2023).

[3] N. J. Cerf, S. Massar, and S. Schneider, #emph[Multipartite classical and quantum secrecy monotones], Phys. Rev. A *66*, 042309 (2002).
