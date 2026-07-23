#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Introduction
<introduction>
In Ref. [asu-qmi] two different expressions of quantum dual total
correlation were obtained: one in terms of von Neumann entropy and other
in terms of quantum relative entropy. It was claimed that the two
expressions are equivalent. In a comment [lee] on Ref. [asu-qmi], Lee
#emph[et al.] have shown that the quantum dual total correlation of an
$n$-partite quantum state cannot be represented as the quantum relative
entropy between $\(n - 1\)$ copies of the quantum state and the product
of $n$ different reduced quantum states for $n gt.eq 3$. They arrived at
this conclusion by considering explicitly the "support" condition of
quantum relative entropy. Essentially, what Lee #emph[et al.] have shown
is that the following two expressions are not equal for $n gt.eq 3$:

$ I_n\(rho\):= sum_(k = 1)^n S\(rho_(overline(k))\)-\(n - 1\)S\(rho\)\, $<vn-ent>
where $rho_(overline(k)) = t r_k\(rho\)$ denotes the $\(n - 1\)$-partite
quantum state obtained by taking the partial trace on the $k^(t h)$
party of $rho$, and

$ J_n\(rho\):= S\(rho^(times.circle\(n - 1\))\|\|times.circle_(k = 1)^n rho_(overline(k))\)\, $<qr-ent1>
where the quantum relative entropy is
$ S\(tau\|\|sigma\):= cases(delim: "{", t r\(tau log tau\)- t r\(tau log sigma\) & upright("if ") s u p p\(tau\)subset.eq s u p p\(sigma\), oo & upright("otherwise.")) $

To justify their claim, authors provide two examples which imply that
the above two expressions of $n$-partite quantum mutual information are
not equivalent. $I_n\(rho\)$ in Eq. (@vn-ent) is non-negative and
non-increasing under local CPTP maps [cerf], and therefore is a suitable
monotonic measure of multi-partite correlations, while $J_n\(rho\)$ in
Eq. (@qr-ent1) is not.

= Reaffirming claim of Lee #emph[et al.]
<reaffirming-claim-of-lee-et-al.>
The claim of Lee #emph[et al.] is right. In this article we show
analytically why the above two expressions are not equivalent. We begin
with expression of $I_n\(rho\)$ \[Eq. (@vn-ent)\] and proceed to show
that this is not equal to $J_n\(rho\)$ \[Eq. (@qr-ent1)\], as argued
below.

$ I_n\(rho\) & = & sum_(k = 1)^n S\(rho_(overline(k))\)-\(n - 1\)S\(rho\)\
 & = & sum_(k = 1)^n #scale(x: 120%, y: 120%)[\(] S\(rho_k\)+ S\(rho_(overline(k))\)- S\(rho\)#scale(x: 120%, y: 120%)[\)] - #scale(x: 120%, y: 120%)[\(] sum_(k = 1)^n S\(rho_k\)- S\(rho\)#scale(x: 120%, y: 120%)[\)]\
 & = & sum_(k = 1)^n S\(rho\|\|rho_k times.circle rho_(overline(k))\)- S\(rho\|\|times.circle_(k = 1)^n rho_k\)\
 & = & S #scale(x: 120%, y: 120%)[\(] rho^(times.circle n)\|\|times.circle_(k = 1)^n\(rho_k times.circle rho_(overline(k))\)#scale(x: 120%, y: 120%)[\)] - S\(rho\|\|times.circle_(k = 1)^n rho_k\)\
 & =^(?) & S #scale(x: 120%, y: 120%)[\(] rho times.circle rho^(times.circle\(n - 1\))\|\|\(times.circle_(k = 1)^n med rho_k\)times.circle\(times.circle_(k = 1)^n med rho_(overline(k))\)#scale(x: 120%, y: 120%)[\)] - S\(rho\|\|times.circle_(k = 1)^n rho_k\)\
 & = & S\(rho\|\|times.circle_(k = 1)^n rho_k\)+ S\(rho^(times.circle\(n - 1\))\|\|times.circle_(k = 1)^n rho_(overline(k))\)- S\(rho\|\|times.circle_(k = 1)^n rho_k\)\
 & = & S\(rho^(times.circle\(n - 1\))\|\|times.circle_(k = 1)^n rho_(overline(k))\)= J_n\(rho\)\, $<qmi1>
where quantum relative entropy in Eq. (@qmi1) and Eq. ([qmi2]) is
properly matched to satisfy the "support" condition in the sense that
$ S\(rho\|\|times.circle_(k = 1)^n rho_k\) & equiv & S\(rho_(12 dots.h.c n)\|\|times.circle_(k = 1)^n rho_k\)\
S\(rho\|\|rho_k times.circle rho_(overline(k))\) & equiv & S\(rho_(k overline(k))\|\|rho_k times.circle rho_(overline(k))\)\
S #scale(x: 120%, y: 120%)[\(] rho^(times.circle n)\|\|times.circle_(k = 1)^n\(rho_k times.circle rho_(overline(k))\)#scale(x: 120%, y: 120%)[\)] & equiv & S #scale(x: 120%, y: 120%)[\(] rho_(12 dots.h.c n) times.circle rho_(23 dots.h.c n 1) times.circle dots.h.c times.circle rho_(n 1 dots.h.c\(n - 1\))\|\|times.circle_(k = 1)^n\(rho_k times.circle rho_(overline(k))\)#scale(x: 120%, y: 120%)[\)]\, $
where $overline(1) = 23 dots.h.c n$, $overline(2) = 34 dots.h.c n 1$ and
$overline(k) =\(k + 1\)dots.h.c n 1 dots.h.c\(k - 1\)$. Eq. (@qmi1) and
Eq. ([qmi2]) are alternate expressions equivalent to Eq. (@vn-ent) in
terms of quantum relative entropy. We, however, prescribe to use Eq.
(@vn-ent) in computing quantum dual total correlation. Eq. ([problem]) is
not correct for two reasons: (i) noncommutativity of tensor product, and
(ii) "matching" issue of subsystems. Therefore, we cannot arrive at Eq.
([qmi3]).

= Second Rebuttal
<second-rebuttal>
Let us reconsider Eq. (@qr-ent1) for $n = 3$ explicitly.
$ J_3\(rho\) & = & S\(rho^(times.circle 2)\|\|times.circle_(k = 1)^3 rho_(overline(k))\)\
 & = & S\(rho_123 times.circle rho_123\|\|rho_23 times.circle rho_31 times.circle rho_12\). $<match1>
Here we see that the subsystems in the first and the second arguments of
the quantum relative entropy are not properly matched. However, the
subsystems in the above expression could be matched up if we adopt the
following conventions: (i) interpret the first argument in the usual
way, with the subsystems in their standard order and (ii) interpret the
tensor product in the second argument with the values of $k$ running
from $n$ to $1$. That is, for $n = 3$, if we define
$ tilde(J)_3\(rho\) & := & S\(rho^(times.circle 2)\|\|times.circle_(k = 3)^1 rho_(overline(k))\)\
 & = & S\(rho_123 times.circle rho_123\|\|rho_12 times.circle rho_31 times.circle rho_23\)\, $<match2>
then we see that the subsystems are properly matched. Now, let us adopt
the following notations:
$ rho_123^(times.circle 2) & = & rho_123 times.circle rho_123 equiv rho_(A_1 A_2 A_3) times.circle rho_(B_1 B_2 B_3) equiv rho_123 times.circle rho_456\,\
times.circle_(k = 3)^1 rho_(overline(k)) & = & rho_12 times.circle rho_31 times.circle rho_23 equiv rho_(A_1 A_2) times.circle rho_(A_3 B_1) times.circle rho_(B_2 B_3) equiv rho_12 times.circle rho_34 times.circle rho_56 . $<notation1>
Then, using notations in Eqs. (@notation1, [notation2]), one might
attempt to show that Eq. (@match2) is equivalent to
$I_3\(rho\)= sum_(k = 1)^3 S\(rho_(overline(k))\)- 2 S\(rho\)$ as argued
below.
$ tilde(J)_3\(rho\) & := & S\(rho^(times.circle 2)\|\|times.circle_(k = 3)^1 rho_(overline(k))\)\
 & = & S\(rho_123 times.circle rho_123\|\|rho_12 times.circle rho_31 times.circle rho_23\)\
 & equiv & S\(rho_123 times.circle rho_456\|\|rho_12 times.circle rho_34 times.circle rho_56\)\
 & = & - t r\(rho_123 times.circle rho_456 log\(rho_12 times.circle rho_34 times.circle rho_56\)\)+ t r\(rho_123 times.circle rho_456 log\(rho_123 times.circle rho_456\)\)\
 & = & - t r\(rho_123 times.circle rho_456 log\(rho_12 times.circle I_34 times.circle I_56\)\)- t r\(rho_123 times.circle rho_456 log\(I_12 times.circle rho_34 times.circle I_56\)\)\
 & - & t r\(rho_123 times.circle rho_456 log\(I_12 times.circle I_34 times.circle rho_56\)\)+ t r\(rho_123 times.circle rho_456 log\(rho_123 times.circle I_456\)\)+ t r\(rho_123 times.circle rho_456 log\(I_123 times.circle rho_456\)\)\
 & = & - t r_12\(rho_12 log rho_12\)- t r_34\(rho_3 times.circle rho_4 log rho_34\) - t r_56\(rho_56 log rho_56\)+ t r_123\(rho_123 log rho_123\)+ t r_456\(rho_456 log rho_456\)\
 & =^(?) & S\(rho_12\)+ S\(rho_34\) + S\(rho_56\)- S\(rho_123\)- S\(rho_456\)\
 & equiv & S\(rho_12\)+ S\(rho_31\)+ S\(rho_23\)- 2 S\(rho_123\)= I_3\(rho\). $<qmi4>
But this is not correct because the second term in Eq. (@qmi4) cannot be
obtained from the previous equation.

Thus, even if we define quantum dual total correlation of a multipartite
system in terms of quantum relative entropy alternatively as
$ tilde(J)_n\(rho\):= S\(rho_(12 dots.h.c n)^(times.circle\(n - 1\))\|\|times.circle_(k = n)^1 rho_(overline(k))\)\, $<qr-ent2>
and use the notations as discussed above, Eq. (@qr-ent2) is not
equivalent to Eq. (@vn-ent).

#block[
AK is very thankful to Jaehak Lee, Gibeom Noh, Changsuk Noh and Jiyong
Park for pointing out the subtle mistake in Ref. [asu-qmi.]

]
#block[
99 A. Kumar, #emph[Multiparty quantum mutual information: An alternative
definition],
#link("https://doi.org/10.1103/PhysRevA.96.012332")[Phys. Rev. A #strong[96], 012332 (2017)].

J. Lee, G. Noh, C. Noh and J. Park, #emph[Comment on "Multiparty quantum
mutual information: An alternative definition"],
#link("https://doi.org/10.1103/PhysRevA.108.066401")[Phys. Rev. A #strong[108(6)], 066401 (2023)].

N. J. Cerf, S. Massar, and S. Schneider, #emph[Multipartite classical
and quantum secrecy monotones],
#link("https://doi.org/10.1103/PhysRevA.66.042309")[Phys. Rev. A #strong[66], 042309 (2002)].

]
