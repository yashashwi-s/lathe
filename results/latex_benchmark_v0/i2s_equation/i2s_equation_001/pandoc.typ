#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ alpha_3 & lt.eq^(upright("(i)")) sum_(s in cal(S)\,a in cal(A)) d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sqrt(frac(C_(sans(c l i p p e d))^star.op log N / delta, N min {d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s \, a \, nu_0 \( s \) \; rho #scale(x: 120%, y: 120%)[\)] \, frac(1, S (A + B))}) sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & lt.eq sqrt(frac(C_(sans(c l i p p e d))^star.op log N / delta, N)) sum_(s in cal(S)\,a in cal(A)) sqrt(d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & quad + sqrt(frac(C_(sans(c l i p p e d))^star.op S (A + B) log N / delta, N)) sum_(s in cal(S)\,a in cal(A)) sqrt(d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)]) dot.op sqrt(d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & lt.eq^(upright("(ii)")) sqrt(C_(sans(c l i p p e d))^star.op / N log N / delta) dot.op sqrt(S A) dot.op sqrt(sum_(s in cal(S)\,a in cal(A)) d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & quad + sqrt(frac(C_(sans(c l i p p e d))^star.op S (A + B) log N / delta, N)) [sum_(s in cal(S)\,a in cal(A)) d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s \, a \, nu_0 \( s \) \; rho #scale(x: 120%, y: 120%)[\)]] sqrt(sum_(s in cal(S)\,a in cal(A)) d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & lt.eq 2 sqrt(frac(C_(sans(c l i p p e d))^star.op S (A + B) log N / delta, N)) sqrt(sum_(s in cal(S)\,a in cal(A)) d^(mu^star.op\,nu_0) #scale(x: 120%, y: 120%)[\(] s\,a\,nu_0\(s\)\;rho #scale(x: 120%, y: 120%)[\)] sans(V a r)_(P_(s\,a\,nu_0\(s\))) (V_(sans(p e))^(-)))\
 & =^(upright("(iii)")) 2 sqrt(frac(C_(sans(c l i p p e d))^star.op S (A + B), N) log N / delta) sqrt(sum_(s in cal(S)) d^(mu^star.op\,nu_0) (s \; rho) "𝔼"_(a tilde.op mu^star.op\(s\)\,b tilde.op nu_0\(s\)) [sans(V a r)_(P_(s\,a\,b)) (V_(sans(p e))^(-))])\
 & lt.eq^(upright("(iv)")) 2 sqrt(frac(C_(sans(c l i p p e d))^star.op S (A + B), N) log N / delta) sqrt(sum_(s in cal(S)) d^(mu^star.op\,nu_0) (s \; rho) sans(V a r)_(P_s^(mu^star.op\,nu_0)) (V_(sans(p e))^(-))) . $
