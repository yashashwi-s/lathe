#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center, text(size: 1.5em)[Aligned Mathematical Structures])
#align(center, [Source-backed grouped formula sample])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

#text("P_{j,j+i} = sum^{M-j}_{m=i+1} binom(M-j, m) P_{TX}^m (1- P_{TX}) ^{M-j-m} times (M-j-i)/(M-j)m ... (m-i+1)P_K^{m} gamma_i gamma_{m,i} + binom(M-j, i) P_{TX}^i (1- P_{TX}) ^{M-j-i} (M-j-i)/(M-j)i! P_K^{i}gamma_i")

*Expression 2.* The following expression is taken from a source-backed formula corpus.

#text("Q(x) = sum_{x/log x <= p <= x-sqrt x} pi(x-p) + O( sum_{p<= x/log x} pi(x) + sum_{x-sqrt x<= p<= x} x ) = sum_{x/log x <= p <= x-sqrt x} pi(x-p) + O( pi(x) pi( x/log x ) + xsqrt x ) = sum_{x/log x <= p <= x-sqrt x} pi(x-p) + O( x^2/log^3x )")

*Expression 3.* The following expression is taken from a source-backed formula corpus.

#text("partial_{xi} u(xi, 0) - partial_{xi} w(xi, 0) <= partial_{xi} u(xi, 0) - partial_{xi} w(0, 0) + [ partial_{xi} w]_{0,beta} |xi|^beta = [ U_beta (1+beta) cos((1+beta) pi/2) + [ partial_{xi} w]_{0,beta} ] |xi|^beta")

*Expression 4.* The following expression is taken from a source-backed formula corpus.

#text("II+III -> 0; IV= integral_{d(x,p)>= rho}(rho^2/(4epsilon)-n)e^{-(rho^2/(4epsilon)-C)} -> 0; I= e^{-C} integral_{|y|<= rho/sqrt{epsilon}} (|y|^2/2-n) (2pi)^{-n/2} e^{-|y|^2/4}(1+O(epsilon |y|^2) dy -> integral_{R^n} (|y|^2/2-n) (2pi)^{-n/2} e^{-|y|^2/4} dy=0.")

*Expression 5.* The following expression is taken from a source-backed formula corpus.

#text("1/omega(B)||(b-b_B)f_1||^s_{L^s_omega}=1/omega(B) integral_{5B} |b(y)-b_B|^s|f|^sdomega(y) <= ( (1/omega(B) integral_{5B} |b(y)-b_B|^{ss_1'}domega(y) )^{1/s_1'} ) (1/omega(B) integral_{5B} |f|^{ss_1} domega(y))^{1/s_1} <= l(B)^{beta s}||b||^s_{Lambda^beta} M^s_{ss_1}(f)(x)")
