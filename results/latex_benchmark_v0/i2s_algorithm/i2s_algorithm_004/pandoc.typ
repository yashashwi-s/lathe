#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Procedure
<procedure>
The pseudocode below is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

#block[
. Considering the dataset of all applicants to both programs, randomly
split the dataset into train and test with equal probability at the
applicant level, denote the resulting sets as
$I^(t r a i n) = {1 \, . . \, cal(I)^(t r a i n)}$ and
$I^(t e s t) = {1 \, . . \, cal(I)^(t e s t)}$. . In the training
dataset, estimate outcome model using cross-validation: $mu_(t r a i n)$
. In the test set, construct predicted treatment effects using
predictions from model $mu_(t r a i n)$. Obtain
$tau_(i\,t)^(O p\,t r a i n) = E\[hat(Y)\(p\)_(t r a i n)- hat(Y)\(O\)_(t r a i n)\|X = x_(i\,t)\,i in I^(t e s t)\]$,
where $hat(Y)\(p\)_(t r a i n)$ is the predicted outcome under program
$p$ constructed using $mu_(t r a i n)$ and $hat(Y)\(O\)_(t r a i n)$ is
the predicted outcome under #emph[Out of Dare IT] and
$t in {1 \, . . . \, 15}$ denotes months. Compute mean treatment effects
per user as:
$tau_i^(O p\,t r a i n) = 1\/t times sum_(t = 1)^15 tau_(i\,t)^(O p\,t r a i n)$,
. Assign treatment to maximize treatment effects subject to capacity
constraint. Let $Q^p$ be the capacity limit of program $p$ and $z_(i p)$
an indicator variable taking the value of one when applicant $i$ is
assigned to program $p$ and zero otherwise. We solve the following
constrained optimization problem:
$ max_(z_(i p)) sum_(i = 1)^I sum_(p = 1)^P z_(i p) tau_i^(O p\,t r a i n) upright(" s.t. ") sum_(i = 1)^I z_(i p) lt.eq Q^p forall_p upright(" &") sum_(i = p)^P z_(i p) = 1 forall_(i in I^(t e s t)) . $
The first constraint ensures that the capacity constraints are not
violated. The second one is that every applicant is assigned to one
program. There is no capacity limit on being #emph[Out of Dare IT]. We
use #emph[LP Solve] algorithm to solve the problem. We obtain optimal
allocation
$cal(A)_(X\,Q)^(*) = {a_i^(*) \, . . . \, a_(cal(I)^(t e s t))^(*)}$, .
Using the test set, estimate new outcome and propensity models using
cross-fitting and obtain predictions: $hat(mu)_(i\,k)$ and
$hat(e)_(i\,k)$ for all $i in I^(t e s t)$. See Appendix
[cross_fit_appendix] for details of the cross-fitting procedure. Obtain
$hat(Y)_(i\,k)\(a^(*)\)$ the AIPW estimates of the predicted outcomes
using cross-fitted models trained in the test set, . Obtain
$hat(V)_(X\,Q)^(*) = frac(1, \|I^(t e s t)\|) times sum_(i = 1)^(cal(I)^(t e s t)) hat(Y)_(i\,k)\(a^(*)\)$
as the mean of predicted outcomes under the allocation
$cal(A)_(X\,Q)^(*)$. Estimate standard errors clustered at the applicant
level: $sigma_(X\,Q)^(*)$. \
$\(cal(A)_(X\,Q)^(*)\,hat(V)_(X\,Q)^(*)\,sigma_(X\,Q)^(*)\,hat(Y)_(1\,k)\(a^(*)\)\,. . .\,hat(Y)_(cal(I)^(t e s t)\,k)\(a^(*)\)\)$

]
