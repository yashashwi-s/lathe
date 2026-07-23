#set page(
  paper: "us-letter",
  margin: (x: 72.27pt, y: 72.27pt),
)
#set text(font: "Palatino", size: 11pt)
#set par(leading: 1.3em, justify: true)

#let otimes = sym.times.circle
#let bigotimes = sym.times.circle.big

#align(center, [
  #text(size: 14pt, weight: "bold")[Reply to \
  Comment on ``Multiparty quantum mutual information: An
  alternative definition'']
  
  #v(1em)
  Asutosh Kumar
  
  #text(size: 10pt)[Department of Physics, Gaya College, Magadh University, Rampur, Gaya 823001, India]
])

#v(2em)

#block(inset: (x: 2em))[
  *Abstract:* We reaffirm the claim of Lee _et al._ [preceding Comment, Phys. Rev. A *108*, 066401 (2023)] that the expression of quantum dual total correlation of a multipartite system in terms of quantum relative entropy as proposed in previous work [A. Kumar, Phys. Rev. A *96*, 012332 (2017)] is not correct. We provide alternate expression(s) of quantum dual total correlation in terms of quantum relative entropy. We, however, prescribe that in computing quantum dual total correlation one should use its expression in terms of von Neumann entropy.
]

#v(1em)

= Introduction
In Ref. [1] two different expressions of quantum dual total correlation were obtained: one in terms of von Neumann entropy and other in terms of quantum relative entropy. It was claimed that the two expressions are equivalent.
In a comment [2] on Ref. [1], Lee _et al._ have shown that the quantum dual total correlation of an $n$-partite quantum state cannot be represented as the quantum relative entropy between $(n - 1)$ copies of the quantum state and the product of $n$ different reduced quantum states for $n >= 3$.
They arrived at this conclusion by considering explicitly the ``support'' condition of quantum relative entropy. 
Essentially, what Lee _et al._ have shown is that the following two expressions are not equal for $n >= 3$:

$ I_n(rho) := sum^n_{k=1} S(rho_overline(k)) - (n-1) S(rho), $ <vn-ent>

where $rho_overline(k) = "tr"_k (rho)$ denotes the $(n-1)$-partite quantum state obtained by taking the partial trace on the $k^"th"$ party of $rho$, and 

$ J_n(rho) := S(rho^(otimes (n-1)) || bigotimes^n_{k=1} rho_overline(k)), $ <qr-ent1>

where the quantum relative entropy is 
$ S(tau || sigma) := cases(
   "tr" (tau log tau) - "tr" (tau log sigma) "if" supp(tau) subset.eq supp(sigma),
   infinity "otherwise." 
) $

To justify their claim, authors provide two examples which imply that the above two expressions of $n$-partite quantum mutual information are not equivalent. 
$I_n(rho)$ in @vn-ent is non-negative and non-increasing under local CPTP maps [3], and therefore is a suitable monotonic measure of multi-partite correlations, while $J_n(rho)$ in @qr-ent1 is not. 

= Reaffirming claim of Lee _et al._
The claim of Lee _et al._ is right. 
In this article we show analytically why the above two expressions are not equivalent. We begin with expression of $I_n(rho)$ [@vn-ent] and proceed to show that this is not equal to $J_n(rho)$ [@qr-ent1], as argued below.

$ I_n(rho) &= sum^n_{k=1} S(rho_overline(k)) - (n-1) S(rho) \
&= sum^n_{k=1} (S(rho_k) + S(rho_overline(k)) - S(rho)) - (sum^n_{k=1} S(rho_k) - S(rho)) \
&= sum^n_{k=1} S(rho || rho_k otimes rho_overline(k)) - S(rho || bigotimes^n_{k=1} rho_k) <qmi1> \
&= S (rho^(otimes n) || bigotimes^n_{k=1} (rho_k otimes rho_overline(k))) - S(rho || bigotimes^n_{k=1} rho_k) <qmi2> \
&overset(?)= #text(fill: blue)[$S (rho otimes rho^(otimes (n-1)) || (bigotimes^n_{k=1} rho_k) otimes (bigotimes^n_{k=1} rho_overline(k)))$] - S(rho || bigotimes^n_{k=1} rho_k) <problem> \
&= S(rho || bigotimes^n_{k=1} rho_k) + S(rho^(otimes (n-1)) || bigotimes^n_{k=1} rho_overline(k)) - S(rho || bigotimes^n_{k=1} rho_k) \
&= S(rho^(otimes (n-1)) || bigotimes^n_{k=1} rho_overline(k)) = J_n(rho), <qmi3> $

where quantum relative entropy in @qmi1 and @qmi2 is properly matched to satisfy the ``support'' condition. Eq. @qmi1 and @qmi2 are alternate expressions equivalent to @vn-ent in terms of quantum relative entropy. We, however, prescribe to use @vn-ent in computing quantum dual total correlation.
Eq. @problem is not correct for two reasons: (i) noncommutativity of tensor product, and (ii) ``matching'' issue of subsystems. Therefore, we cannot arrive at @qmi3. 

= Second Rebuttal
Let us reconsider @qr-ent1 for $n=3$ explicitly.
$ J_3(rho) &= S(rho^(otimes 2) || bigotimes^3_{k=1} rho_overline(k)) \
&= S(rho_123 otimes rho_123 || rho_23 otimes rho_31 otimes rho_12). <match1> $

Here we see that the subsystems in the first and the second arguments of the quantum relative entropy are not properly matched. 
However, the subsystems in the above expression could be matched up if we adopt the following conventions: (i) interpret the first argument in the usual way, with the subsystems in their standard order and (ii) interpret the tensor product in the second argument with the values of $k$ running from $n$ to $1$. That is, for $n=3$, if we define 
$ tilde(J)_3(rho) &:= S(rho^(otimes 2) || bigotimes^1_{k=3} rho_overline(k)) \
&= S(rho_123 otimes rho_123 || rho_12 otimes rho_31 otimes rho_23), <match2> $

then we see that the subsystems are properly matched. Now, let us adopt the following notations:
$ rho_123^(otimes 2) &= rho_123 otimes rho_123 equiv rho_(A_1 A_2 A_3) otimes rho_(B_1 B_2 B_3) equiv rho_123 otimes rho_456, <notation1> \
bigotimes^1_{k=3} rho_overline(k) &= rho_12 otimes rho_31 otimes rho_23 equiv rho_(A_1 A_2) otimes rho_(A_3 B_1) otimes rho_(B_2 B_3) equiv rho_12 otimes rho_34 otimes rho_56. <notation2> $

Then, using notations in @notation1, @notation2, one might attempt to show that @match2 is equivalent to $I_3(rho) = sum^3_{k=1} S(rho_overline(k)) - 2 S(rho)$ as argued below.
$ tilde(J)_3(rho) &:= S(rho^(otimes 2) || bigotimes^1_{k=3} rho_overline(k)) \
&= S(rho_123 otimes rho_123 || rho_12 otimes rho_31 otimes rho_23) \
&equiv S(rho_123 otimes rho_456 || rho_12 otimes rho_34 otimes rho_56) \
&= - "tr" (rho_123 otimes rho_456 log (rho_12 otimes rho_34 otimes rho_56)) + "tr" (rho_123 otimes rho_456 log (rho_123 otimes rho_456)) \
&= - "tr" (rho_123 otimes rho_456 log (rho_12 otimes I_34 otimes I_56)) - "tr" (rho_123 otimes rho_456 log (I_12 otimes rho_34 otimes I_56)) \
&- "tr" (rho_123 otimes rho_456 log (I_12 otimes I_34 otimes rho_56)) + "tr" (rho_123 otimes rho_456 log (rho_123 otimes I_456)) + "tr" (rho_123 otimes rho_456 log (I_123 otimes rho_456)) \
&= - "tr"_12 (rho_12 log rho_12) #text(fill: blue)[$- "tr"_34 (rho_3 otimes rho_4 log rho_34)$] - "tr"_56 (rho_56 log rho_56) + "tr"_123 (rho_123 log rho_123) + "tr"_456 (rho_456 log rho_456) \
&overset(?)= S(rho_12) + #text(fill: blue)[$S(rho_34)$] + S(rho_56) - S(rho_123) - S(rho_456) <qmi4> \
&equiv S(rho_12) + S(rho_31) + S(rho_23) - 2 S(rho_123) = I_3 (rho). $

But this is not correct because the second term in @qmi4 cannot be obtained from the previous equation.

Thus, even if we define quantum dual total correlation of a multipartite system in terms of quantum relative entropy alternatively as
$ tilde(J)_n(rho) := S(rho_12...n^(otimes (n-1)) || bigotimes^1_{k=n} rho_overline(k)), <qr-ent2> $

and use the notations as discussed above, @qr-ent2 is not equivalent to @vn-ent.

#v(1em)

#block[
  *Acknowledgments*
  AK is very thankful to Jaehak Lee, Gibeom Noh, Changsuk Noh and Jiyong Park for pointing out the subtle mistake in Ref. [1]. 
]

#v(1em)

[1] A. Kumar, _Multiparty quantum mutual information: An alternative definition_, Phys. Rev. A *96*, 012332 (2017).

[2] J. Lee, G. Noh, C. Noh and J. Park, _Comment on ``Multiparty quantum mutual information: An alternative definition''_, Phys. Rev. A *108(6)*, 066401 (2023).

[3] N. J. Cerf, S. Massar, and S. Schneider, _Multipartite classical and quantum secrecy monotones_, Phys. Rev. A *66*, 042309 (2002).
