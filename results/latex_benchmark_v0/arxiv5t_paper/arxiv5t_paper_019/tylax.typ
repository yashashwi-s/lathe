#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

  /* \newboolean */ /* \setboolean */

 /* \pagestyle */empty

 /* \title */Reply to \  Comment on ``Multiparty quantum mutual information: An alternative definition''

 /* \author */Asutosh Kumar /* \email */asutoshk.phys[gmail.com]

 /* \affiliation */Department of Physics, Gaya College, Magadh University, Rampur, Gaya 823001, India

#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We reaffirm the claim of Lee __ preceding Comment, Phys. Rev. A **, 066401 (2023) that the expression of quantum dual total correlation of a multipartite system in terms of quantum relative entropy as proposed in previous work A. Kumar, Phys. Rev. A **, 012332 (2017) is not correct. We provide alternate expression(s) of quantum dual total correlation in terms of quantum relative entropy. We, however, prescribe that in computing quantum dual total correlation one should use its expression in terms of von Neumann entropy.
]

 /* \maketitle */
== Introduction
 In Ref. #cite(<asu-qmi>) two different expressions of quantum dual total correlation were obtained: one in terms of von Neumann entropy and other in terms of quantum relative entropy. It was claimed that the two expressions are equivalent. In a comment #cite(<lee>) on Ref. #cite(<asu-qmi>), Lee __ have shown that the quantum dual total correlation of an $n $-partite quantum state cannot be represented as the quantum relative entropy between $(n - 1)$ copies of the quantum state and the product of $n $ different reduced quantum states for $n >= 3 $. They arrived at this conclusion by considering explicitly the ``support'' condition of quantum relative entropy.  Essentially, what Lee __ have shown is that the following two expressions are not equal for $n >= 3 $:

 $  I_(n)(rho) : = sum^(n)_(k = 1) S(rho_(overline(k))) -(n - 1) S(rho),  $ <vn-ent>
 where $rho_(overline(k)) = t r_(k)(rho)$ denotes the $(n - 1)$-partite quantum state obtained by taking the partial trace on the $k^(t h)$ party of $rho $, and

 $  J_(n)(rho) : = S(rho^(times.circle(n - 1)) | | times.circle^(n)_(k = 1) rho_(overline(k))),  $ <qr-ent1>
 where the quantum relative entropy is
$  S(tau | | sigma) : = cases(t r(tau log tau) - t r(tau log sigma) & "if" s u p p(tau) subset.eq s u p p(sigma), infinity& "otherwise.")  $

 To justify their claim, authors provide two examples which imply that the above two expressions of $n $-partite quantum mutual information are not equivalent.
$I_(n)(rho)$ in Eq. (@vn-ent) is non-negative and non-increasing under local CPTP maps #cite(<cerf>), and therefore is a suitable monotonic measure of multi-partite correlations, while $J_(n)(rho)$ in Eq. (@qr-ent1) is not.

== Reaffirming claim of Lee \it et al.
 The claim of Lee __ is right.  In this article we show analytically why the above two expressions are not equivalent. We begin with expression of $I_(n)(rho)$ Eq. (@vn-ent) and proceed to show that this is not equal to $J_(n)(rho)$ Eq. (@qr-ent1), as argued below.

 $  I_(n)(rho) & = & sum^(n)_(k = 1) S(rho_(overline(k))) -(n - 1) S(rho) nonumber \
& = & sum^(n)_(k = 1) S(rho_(k)) + S(rho_(overline(k))) - S(rho) - sum^(n)_(k = 1) S(rho_(k)) - S(rho) nonumber \ & = & sum^(n)_(k = 1) S(rho | | rho_(k) times.circle rho_(overline(k))) - S(rho | | times.circle^(n)_(k = 1) rho_(k)) \ & = & S rho^(times.circle n) | | times.circle^(n)_(k = 1)(rho_(k) times.circle rho_(overline(k))) - S(rho | | times.circle^(n)_(k = 1) rho_(k)) \ & limits(=)^(?) & /* \color{blue} -> blue */S rho times.circle rho^(times.circle(n - 1)) | |(times.circle^(n)_(k = 1)space.nobreak rho_(k)) times.circle(times.circle^(n)_(k = 1)space.nobreak rho_(overline(k))) - S(rho | | times.circle^(n)_(k = 1) rho_(k)) \ & = & S(rho | | times.circle^(n)_(k = 1) rho_(k)) + S(rho^(times.circle(n - 1)) | | times.circle^(n)_(k = 1) rho_(overline(k))) - S(rho | | times.circle^(n)_(k = 1) rho_(k)) nonumber \ & = & S(rho^(times.circle(n - 1)) | | times.circle^(n)_(k = 1) rho_(overline(k))) = J_(n)(rho),  $ <qmi3>
 where
quantum relative entropy in Eq. ([qmi1]) and Eq. ([qmi2]) is properly matched to satisfy the ``support'' condition in the sense that  $  S(rho | | times.circle^(n)_(k = 1) rho_(k)) & equiv & S(rho_(1 2 ... n) | | times.circle^(n)_(k = 1) rho_(k)) nonumber \ S(rho | | rho_(k) times.circle rho_(overline(k))) & equiv & S(rho_(k overline(k)) | | rho_(k) times.circle rho_(overline(k))) nonumber \ S rho^(times.circle n) | | times.circle^(n)_(k = 1)(rho_(k) times.circle rho_(overline(k))) & equiv & S rho_(1 2 ... n) times.circle rho_(2 3 ... n 1) times.circle ... times.circle rho_(n 1 ...(n - 1)) | | times.circle^(n)_(k = 1)(rho_(k) times.circle rho_(overline(k))), nonumber  $
 where $overline(1) = 2 3 ... n $, $overline(2) = 3 4 ... n 1 $ and $overline(k) =(k + 1) ... n 1 ...(k - 1)$. Eq. ([qmi1]) and Eq. ([qmi2]) are alternate expressions equivalent to Eq. (@vn-ent) in terms of quantum relative entropy. We, however, prescribe to use Eq. (@vn-ent) in computing quantum dual total correlation.
Eq. ([problem]) is not correct for two reasons: (i) noncommutativity of tensor product, and (ii) ``matching'' issue of subsystems. Therefore, we cannot arrive at Eq. (@qmi3).

== Second Rebuttal
 Let us reconsider Eq. (@qr-ent1) for $n = 3 $ explicitly. $  J_(3)(rho) & = & S(rho^(times.circle 2) | | times.circle^(3)_(k = 1) rho_(overline(k))) nonumber \ & = & S(rho_(1 2 3) times.circle rho_(1 2 3) | | rho_(2 3) times.circle rho_(3 1) times.circle rho_(1 2)).  $ <match1>
 Here we see that the subsystems in the first and the second arguments of the quantum relative entropy are not properly matched.
However, the subsystems in the above expression could be matched up if we adopt the following conventions: (i) interpret the first argument in the usual way, with the subsystems in their standard order and (ii) interpret the tensor product in the second argument with the values of $k $ running from $n $ to $1 $. That is, for $n = 3 $, if we define  $  tilde(J)_(3)(rho) & : = & S(rho^(times.circle 2) | | times.circle^(1)_(k = 3) rho_(overline(k))) nonumber \ & = & S(rho_(1 2 3) times.circle rho_(1 2 3) | | rho_(1 2) times.circle rho_(3 1) times.circle rho_(2 3)),  $ <match2>
 then we see that the subsystems are properly matched. Now, let us adopt the following notations: $  rho_(1 2 3)^(times.circle 2) & = & rho_(1 2 3) times.circle rho_(1 2 3) equiv rho_(A_(1)A_(2)A_(3)) times.circle rho_(B_(1)B_(2)B_(3)) equiv rho_(1 2 3) times.circle rho_(4 5 6), \
times.circle^(1)_(k = 3) rho_(overline(k)) & = & rho_(1 2) times.circle rho_(3 1) times.circle rho_(2 3) equiv rho_(A_(1)A_(2)) times.circle rho_(A_(3)B_(1)) times.circle rho_(B_(2)B_(3)) equiv rho_(1 2) times.circle rho_(3 4) times.circle rho_(5 6).  $ <notation2>
 Then, using notations in Eqs. ([notation1], @notation2), one might attempt to show that Eq. (@match2) is equivalent to $I_(3)(rho) = sum^(3)_(k = 1) S(rho_(overline(k))) - 2 S(rho)$ as argued below. $  tilde(J)_(3)(rho) & : = & S(rho^(times.circle 2) | | times.circle^(1)_(k = 3) rho_(overline(k))) nonumber \ & = & S(rho_(1 2 3) times.circle rho_(1 2 3) | | rho_(1 2) times.circle rho_(3 1) times.circle rho_(2 3)) nonumber \ & equiv & S(rho_(1 2 3) times.circle rho_(4 5 6) | | rho_(1 2) times.circle rho_(3 4) times.circle rho_(5 6)) nonumber \ & = & - t r(rho_(1 2 3) times.circle rho_(4 5 6) log(rho_(1 2) times.circle rho_(3 4) times.circle rho_(5 6))) + t r(rho_(1 2 3) times.circle rho_(4 5 6) log(rho_(1 2 3) times.circle rho_(4 5 6))) nonumber \ & = & - t r(rho_(1 2 3) times.circle rho_(4 5 6) log(rho_(1 2) times.circle I_(3 4) times.circle I_(5 6))) - t r(rho_(1 2 3) times.circle rho_(4 5 6) log(I_(1 2) times.circle rho_(3 4) times.circle I_(5 6))) nonumber \ & - & t r(rho_(1 2 3) times.circle rho_(4 5 6) log(I_(1 2) times.circle I_(3 4) times.circle rho_(5 6))) + t r(rho_(1 2 3) times.circle rho_(4 5 6) log(rho_(1 2 3) times.circle I_(4 5 6))) + t r(rho_(1 2 3) times.circle rho_(4 5 6) log(I_(1 2 3) times.circle rho_(4 5 6)))nonumber \ & = & - t r_(1 2)(rho_(1 2) log rho_(1 2)) /* \color{blue} -> blue */ - t r_(3 4)(rho_(3) times.circle rho_(4) log rho_(3 4)) - t r_(5 6)(rho_(5 6) log rho_(5 6)) + t r_(1 2 3)(rho_(1 2 3) log rho_(1 2 3)) + t r_(4 5 6)(rho_(4 5 6) log rho_(4 5 6)) nonumber \ & limits(=)^(?) & S(rho_(1 2)) + /* \color{blue} -> blue */S(rho_(3 4)) + S(rho_(5 6)) - S(rho_(1 2 3)) - S(rho_(4 5 6)) \ & equiv & S(rho_(1 2)) + S(rho_(3 1)) + S(rho_(2 3)) - 2 S(rho_(1 2 3)) = I_(3)(rho).  $ <qmi4>
 But this is not correct because the second term in Eq. (@qmi4) cannot be obtained from the previous equation.

 Thus, even if we define quantum dual total correlation of a multipartite system in terms of quantum relative entropy alternatively as $  tilde(J)_(n)(rho) : = S(rho_(1 2 ... n)^(times.circle(n - 1)) | | times.circle^(1)_(k = n) rho_(overline(k))),  $ <qr-ent2>
 and use the notations as discussed above, Eq. (@qr-ent2) is not equivalent to Eq. (@vn-ent).

 /* Begin acknowledgments */
 AK is very thankful to Jaehak Lee, Gibeom Noh, Changsuk Noh and Jiyong Park for pointing out the subtle mistake in Ref. #cite(<asu-qmi>).

/* End acknowledgments */

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ A. Kumar, __, #link("https://doi.org/10.1103/PhysRevA.96.012332")[Phys. Rev. A \bf96, 012332 (2017)].

 ] <asu-qmi>
#figure(kind: "bib", supplement: none, caption: [2])[ J. Lee, G. Noh, C. Noh and J. Park, __, #link("https://doi.org/10.1103/PhysRevA.108.066401")[Phys. Rev. A \bf108(6), 066401 (2023)].

 ] <lee>
#figure(kind: "bib", supplement: none, caption: [3])[ N. J. Cerf, S. Massar, and S. Schneider, __, #link("https://doi.org/10.1103/PhysRevA.66.042309")[Phys. Rev. A \bf66, 042309 (2002)].

 ] <cerf>

