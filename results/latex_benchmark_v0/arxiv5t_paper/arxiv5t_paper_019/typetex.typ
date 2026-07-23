#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Introduction
<introduction>
In Ref. [asu-qmi] two different expressions of quantum dual total
correlation were obtained: one in terms of von Neumann entropy and other
in terms of quantum relative entropy. It was claimed that the two
expressions are equivalent. In a comment [lee] on Ref. [asu-qmi], Lee
#emph[et al.] have shown that the quantum dual total correlation of an
#mi(`n`)-partite quantum state cannot be represented as the quantum
relative entropy between #mi(`(n - 1)`) copies of the quantum state and
the product of #mi(`n`) different reduced quantum states for
#mi(`n \ge 3`). They arrived at this conclusion by considering
explicitly the "support" condition of quantum relative entropy.
Essentially, what Lee #emph[et al.] have shown is that the following two
expressions are not equal for #mi(`n \ge 3`):

$ #mitex(`
 
I_n(\rho) := \sum^n_{k=1} S(\rho_{\overline{k}}) - (n-1) S(\rho),
`) $ where #mi(`\rho_{\overline{k}} = tr_k (\rho)`) denotes the
#mi(`(n-1)`)-partite quantum state obtained by taking the partial trace
on the #mi(`k^{th}`) party of #mi(`\rho`), and

$ #mitex(`

J_n(\rho) := S(\rho^{\otimes (n-1)} || \otimes^n_{k=1} \rho_{\overline{k}}),
`) $ where the quantum relative entropy is
$ #mitex(`S(\tau || \sigma) := 
  \begin{cases} 
   tr (\tau \log \tau) - tr (\tau \log \sigma) & \text{if } supp(\tau) \subseteq supp(\sigma) \\
   \infty       & \text{otherwise.} 
  \end{cases}`) $

To justify their claim, authors provide two examples which imply that
the above two expressions of #mi(`n`)-partite quantum mutual information
are not equivalent. #mi(`I_n(\rho)`) in Eq. ([vn-ent]) is non-negative
and non-increasing under local CPTP maps [cerf], and therefore is a
suitable monotonic measure of multi-partite correlations, while
#mi(`J_n(\rho)`) in Eq. ([qr-ent1]) is not.

= Reaffirming claim of Lee #emph[et al.]
<reaffirming-claim-of-lee-et-al.>
The claim of Lee #emph[et al.] is right. In this article we show
analytically why the above two expressions are not equivalent. We begin
with expression of #mi(`I_n(\rho)`) \[Eq. ([vn-ent])\] and proceed to
show that this is not equal to #mi(`J_n(\rho)`) \[Eq. ([qr-ent1])\], as
argued below.

$ #mitex(`\begin{eqnarray}
I_n(\rho) &=& \sum^n_{k=1} S(\rho_{\overline{k}}) - (n-1) S(\rho) \nonumber \\
%&=& \sum^n_{k=1} S(\rho_{\overline{k}}) + \sum^n_{k=1} S(\rho_{k}) - n S(\rho) +S(\rho) - \sum^n_{k=1} S(\rho_{k}) \nonumber \\
&=& \sum^n_{k=1} \big(S(\rho_{k}) + S(\rho_{\overline{k}}) - S(\rho) \big) - \big(\sum^n_{k=1} S(\rho_{k}) - S(\rho) \big) \nonumber \\
&=& \sum^n_{k=1} S(\rho || \rho_k \otimes \rho_{\overline{k}}) - S(\rho || \otimes^n_{k=1} \rho_{k})  \\
&=& S \big(\rho^{\otimes n} || \otimes^n_{k=1} (\rho_{k} \otimes \rho_{\overline{k}}) \big) - S(\rho || \otimes^n_{k=1} \rho_{k})  \\
&\overset{?}{=}& {\color{blue}S \big(\rho \otimes \rho^{\otimes (n-1)} || (\otimes^n_{k=1}~ \rho_{k}) \otimes (\otimes^n_{k=1}~ \rho_{\overline{k}}) \big)} - S(\rho || \otimes^n_{k=1} \rho_{k})  \\
&=& S(\rho || \otimes^n_{k=1} \rho_{k}) + S(\rho^{\otimes (n-1)} || \otimes^n_{k=1} \rho_{\overline{k}}) - S(\rho || \otimes^n_{k=1} \rho_{k}) \nonumber \\
&=& S(\rho^{\otimes (n-1)} || \otimes^n_{k=1} \rho_{\overline{k}}) = J_n(\rho), 
\end{eqnarray}`) $ where quantum relative entropy in Eq. ([qmi1]) and Eq.
([qmi2]) is properly matched to satisfy the "support" condition in the
sense that $ #mitex(`\begin{eqnarray}
S(\rho || \otimes^n_{k=1} \rho_{k}) &\equiv & S(\rho_{12\cdots n} || \otimes^n_{k=1} \rho_{k}) \nonumber \\
S(\rho || \rho_k \otimes \rho_{\overline{k}}) &\equiv & S(\rho_{k\overline{k}} || \rho_k \otimes \rho_{\overline{k}}) \nonumber \\
S \big(\rho^{\otimes n} || \otimes^n_{k=1} (\rho_{k} \otimes \rho_{\overline{k}}) \big) &\equiv & S \big(\rho_{12\cdots n} \otimes \rho_{23\cdots n1} \otimes \cdots \otimes \rho_{n1\cdots (n-1)} || \otimes^n_{k=1} (\rho_{k} \otimes \rho_{\overline{k}}) \big), \nonumber
\end{eqnarray}`) $ where #mi(`\overline{1} = 23 \cdots n`),
#mi(`\overline{2} = 34 \cdots n1`) and
#mi(`\overline{k} = (k+1) \cdots n1 \cdots (k-1)`). Eq. ([qmi1]) and Eq.
([qmi2]) are alternate expressions equivalent to Eq. ([vn-ent]) in terms
of quantum relative entropy. We, however, prescribe to use Eq. ([vn-ent])
in computing quantum dual total correlation. Eq. ([problem]) is not
correct for two reasons: (i) noncommutativity of tensor product, and
(ii) "matching" issue of subsystems. Therefore, we cannot arrive at Eq.
([qmi3]).

= Second Rebuttal
<second-rebuttal>
Let us reconsider Eq. ([qr-ent1]) for #mi(`n=3`) explicitly.
$ #mitex(`\begin{eqnarray}
J_3(\rho) &=& S(\rho^{\otimes 2} || \otimes^3_{k=1} \rho_{\overline{k}}) \nonumber \\ 
&=& S(\rho_{123} \otimes \rho_{123} || \rho_{23} \otimes \rho_{31} \otimes \rho_{12}). 
\end{eqnarray}`) $ Here we see that the subsystems in the first and the
second arguments of the quantum relative entropy are not properly
matched. However, the subsystems in the above expression could be
matched up if we adopt the following conventions: (i) interpret the
first argument in the usual way, with the subsystems in their standard
order and (ii) interpret the tensor product in the second argument with
the values of #mi(`k`) running from #mi(`n`) to #mi(`1`). That is, for
#mi(`n=3`), if we define $ #mitex(`\begin{eqnarray}
\tilde{J}_3(\rho) &:=& S(\rho^{\otimes 2} || \otimes^1_{k=3} \rho_{\overline{k}}) \nonumber \\
&=& S(\rho_{123} \otimes \rho_{123} || \rho_{12} \otimes \rho_{31} \otimes \rho_{23}), 
\end{eqnarray}`) $ then we see that the subsystems are properly matched.
Now, let us adopt the following notations: $ #mitex(`\begin{eqnarray}
\rho_{123}^{\otimes 2} &=& \rho_{123} \otimes \rho_{123} 
 \equiv  \rho_{A_1A_2A_3} \otimes \rho_{B_1B_2B_3} 
 \equiv  \rho_{123} \otimes \rho_{456},  \\
 %
\otimes^1_{k=3} \rho_{\overline{k}} &=& \rho_{12} \otimes \rho_{31} \otimes \rho_{23} 
 \equiv  \rho_{A_1A_2} \otimes \rho_{A_3B_1} \otimes \rho_{B_2B_3} 
 \equiv  \rho_{12} \otimes \rho_{34} \otimes \rho_{56}. 
\end{eqnarray}`) $ Then, using notations in Eqs. ([notation1],
[notation2]), one might attempt to show that Eq. ([match2]) is equivalent
to #mi(`I_3(\rho) = \sum^3_{k=1} S(\rho_{\overline{k}}) - 2 S(\rho)`) as
argued below. $ #mitex(`\begin{eqnarray}
\tilde{J}_3(\rho) &:=& S(\rho^{\otimes 2} || \otimes^1_{k=3} \rho_{\overline{k}}) \nonumber \\
&=& S(\rho_{123} \otimes \rho_{123} || \rho_{12} \otimes \rho_{31} \otimes \rho_{23}) \nonumber \\
&\equiv & S(\rho_{123} \otimes \rho_{456} || \rho_{12} \otimes \rho_{34} \otimes \rho_{56}) \nonumber \\
&=& - tr (\rho_{123} \otimes \rho_{456} \log (\rho_{12} \otimes \rho_{34} \otimes \rho_{56})) + tr (\rho_{123} \otimes \rho_{456} \log (\rho_{123} \otimes \rho_{456})) \nonumber \\
&=& - tr (\rho_{123} \otimes \rho_{456} \log (\rho_{12} \otimes I_{34} \otimes I_{56})) - tr (\rho_{123} \otimes \rho_{456} \log (I_{12} \otimes \rho_{34} \otimes I_{56})) \nonumber \\
&-& tr (\rho_{123} \otimes \rho_{456} \log (I_{12} \otimes I_{34} \otimes \rho_{56})) + tr (\rho_{123} \otimes \rho_{456} \log (\rho_{123} \otimes I_{456})) + tr (\rho_{123} \otimes \rho_{456} \log (I_{123} \otimes \rho_{456}))\nonumber \\
&=& - tr_{12} (\rho_{12} \log \rho_{12}) {\color{blue} - tr_{34} (\rho_{3} \otimes \rho_{4} \log \rho_{34})} - tr_{56} (\rho_{56} \log \rho_{56}) + tr_{123} (\rho_{123} \log \rho_{123}) + tr_{456} (\rho_{456} \log \rho_{456}) \nonumber \\
&\overset{?}{=}& S(\rho_{12}) + {\color{blue}S(\rho_{34})} + S(\rho_{56}) - S(\rho_{123}) - S(\rho_{456})  \\
&\equiv & S(\rho_{12}) + S(\rho_{31}) + S(\rho_{23}) - 2 S(\rho_{123}) = I_3 (\rho).
\end{eqnarray}`) $ But this is not correct because the second term in
Eq. ([qmi4]) cannot be obtained from the previous equation.

Thus, even if we define quantum dual total correlation of a multipartite
system in terms of quantum relative entropy alternatively as $ #mitex(`

\tilde{J}_n(\rho) := S(\rho_{12\cdots n}^{\otimes (n-1)} || \otimes^1_{k=n} \rho_{\overline{k}}),
`) $ and use the notations as discussed above, Eq. ([qr-ent2]) is not
equivalent to Eq. ([vn-ent]).

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
