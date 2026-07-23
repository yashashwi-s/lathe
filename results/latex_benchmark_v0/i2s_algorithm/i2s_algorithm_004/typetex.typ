#import "@preview/mitex:0.2.4": *
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
#mi(`I^{train} = \left\{1,..,\mathcal{I}^{train}\right\}`) and
#mi(`I^{test}= \left\{1,..,\mathcal{I}^{test}\right\}`). . In the
training dataset, estimate outcome model using cross-validation:
#mi(`\mu_{train}`) . In the test set, construct predicted treatment
effects using predictions from model #mi(`\mu_{train}`). Obtain
#mi(`\tau^{Op,train}_{i,t} = E[\hat{Y}(p)_{train} - \hat{Y}(O)_{train}|X=x_{i,t} , i \in I^{test}]`),
where #mi(`\hat{Y}(p)_{train}`) is the predicted outcome under program
#mi(`p`) constructed using #mi(`\mu_{train}`) and
#mi(`\hat{Y}(O)_{train}`) is the predicted outcome under #emph[Out of
Dare IT] and #mi(`t \in \left\{1,...,15\right\}`) denotes months.
Compute mean treatment effects per user as:
#mi(`\tau^{Op,train}_{i} = 1/t \times \sum_{t=1}^{15}\tau^{Op,train}_{i,t}`),
. Assign treatment to maximize treatment effects subject to capacity
constraint. Let #mi(`Q^{p}`) be the capacity limit of program #mi(`p`)
and #mi(`z_{ip}`) an indicator variable taking the value of one when
applicant #mi(`i`) is assigned to program #mi(`p`) and zero otherwise.
We solve the following constrained optimization problem:
$ #mitex(`\max_{z_{ip}}\sum_{i=1}^{I}\sum_{p=1}^{P}z_{ip}\tau_{i}^{Op,train} \text{ s.t. }\sum_{i=1}^{I}z_{ip} \leq Q^{p} \forall_{p} \text{ \& }\sum_{i=p}^{P}z_{ip} = 1\forall_{i \in I^{test}}.`) $
The first constraint ensures that the capacity constraints are not
violated. The second one is that every applicant is assigned to one
program. There is no capacity limit on being #emph[Out of Dare IT]. We
use #emph[LP Solve] algorithm to solve the problem. We obtain optimal
allocation
#mi(`\mathcal{A}_{X,Q}^{*} = \left\{a_{i}^{*},...,a_{\mathcal{I}^{test}}^{*}\right\}`),
. Using the test set, estimate new outcome and propensity models using
cross-fitting and obtain predictions: #mi(`\hat{\mu}_{i,k}`) and
#mi(`\hat{e}_{i,k}`) for all #mi(`i \in I^{test}`). See Appendix
[cross_fit_appendix] for details of the cross-fitting procedure. Obtain
#mi(`\hat{Y}_{i,k}(a^{*})`) the AIPW estimates of the predicted outcomes
using cross-fitted models trained in the test set, . Obtain
#mi(`\hat{V}_{X,Q}^{*} = \frac{1}{|I^{test}|}\times \sum_{i=1}^{\mathcal{I}^{test}}\hat{Y}_{i,k}(a^{*})`)
as the mean of predicted outcomes under the allocation
#mi(`\mathcal{A}_{X,Q}^{*}`). Estimate standard errors clustered at the
applicant level: #mi(`\sigma_{X,Q}^{*}`). \
#mi(`(\mathcal{A}_{X,Q}^{*},\hat{V}_{X,Q}^{*},\sigma_{X,Q}^{*},\hat{Y}_{1,k}(a^{*}),...,\hat{Y}_{\mathcal{I}^{test},k}(a^{*}) )`)

]
