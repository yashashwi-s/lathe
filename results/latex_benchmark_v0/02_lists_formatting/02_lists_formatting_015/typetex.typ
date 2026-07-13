#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Extracted Lists
<extracted-lists>
The list environments below are extracted from arXiv LaTeX source and
wrapped for pdfLaTeX validation.

+ If we analytically continue along a simple loop around #mi(`z=0`) in
  the counterclockwise direction, #mi(`t`) becomes #mi(`t+1`). (It will
  be convenient to also introduce #mi(`q=e^{2\pi it}`), which remains
  single-valued near #mi(`z=0`)\.)

+ There are cycles #mi(`\gamma_0`) and #mi(`\gamma_1`) such that
  #mi(`\int_{\gamma_0}\omega(z)`) is single valued near #mi(`z=0`), and
  $ #mitex(`t=\frac{\int_{\gamma_1}\omega(z)}{\int_{\gamma_0}\omega(z)}`) $
  in an angular sector near #mi(`z=0`).

+ There is a period function for #mi(`\omega(z)`),
  $ #mitex(`f_0(z):=\int_{\gamma_0}\omega(z)`) $ which is single-valued
  near #mi(`z=0`). This period function is unique up to multiplication
  by a constant. (This implies that the cycle #mi(`\gamma_0`) is also
  unique up to a constant multiple.)

  In particular, the family of meromorphic #mi(`n`)-forms
  $ #mitex(`\widetilde\omega(z):=\frac{\omega(z)}{\int_{\gamma_0}\omega(z)}`) $
  will have the property that
  $ #mitex(`\int_{\gamma}\widetilde\omega(z)\equiv1`) $ for some
  #mi(`\gamma`), and it is the unique such family up to constant
  multiple.

+ Fixing a choice of period function #mi(`f_0(z)`) as in part (1), there
  is a period function $ #mitex(`f_1(z):=\int_{\gamma_1}\omega(z)`) $
  such that #mi(`\varphi(z):=f_1(z)/f_0(z)`) transforms as
  $ #mitex(`\varphi(z)\mapsto\varphi(z)+1`) $ upon transport around
  #mi(`z=0`) in the counterclockwise direction. The ratio
  #mi(`\varphi(z)`) is unique up to the addition of a constant.
