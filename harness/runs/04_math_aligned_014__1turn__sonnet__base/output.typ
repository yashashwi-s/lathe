#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#align(center)[
  #text(size: 17pt, weight: "bold")[Aligned Mathematical Structures]
  #v(0.5em)
  #text(size: 12pt)[Source-backed grouped formula sample]
  #v(1em)
]

= Expressions

#par[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

#v(0.5em)
$ M^a_(0c) M^c_(0b) = (M_0^2)^a_b = mat(
  -alpha'/2 [A_mu, A_nu] psi^mu psi^nu + overline(T) T,
  -i sqrt(alpha') (overline(T) A'_mu - A_mu overline(T)) psi^mu;
  -i sqrt(alpha') (T A_mu - A'_mu T) psi^mu,
  -alpha'/2 [A'_mu, A'_nu] psi^mu psi^nu + T overline(T)
) space . $
#v(0.5em)

#par[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

#v(0.5em)
$ norm(r_h^+ u - r_h u)_(0,2)^2
  &= a_h^+(r_h^+ u - r_h u, w) \
  &= a_h^+(r_h^+ u - r_h u, w - w_h^+) + a_h^+(r_h^+ u - r_h u, w_h^+) \
  &= a_h^+(r_h^+ u - r_h u, w - w_h^+) + a_h^+(u - r_h u, w_h^+) \
  &= a_h^+(r_h^+ u - r_h u, w - w_h^+) + a_h^+(u - r_h u, w_h^+ - w_h) \
  &wide + a_h^+(u - r_h u, w_h) - a_h (u - r_h u, w_h) \
  &=: T_1 + T_2 + T_3, $
#v(0.5em)

#par[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

#v(0.5em)
$ sum_(n=1)^infinity c_(1,n) T_1^n lr(({x_tau^0}_(tau=1)^r))
  &equiv sum_(n=1)^infinity c_(1,n) T_1^n lr(({x_tau^0 tilde(f)_0^n}_(tau=1)^r)) , \
  sum_(n=1)^infinity c_(2,n) T_2^n lr(({x_theta^0}_(theta=r+1)^(r+s)))
  &equiv sum_(n=1)^infinity c_(2,n) T_2^n lr(({x_theta^0 tilde(f)_0^n}_(theta=r+1)^(r+s))) . $
#v(0.5em)

#par[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

#v(0.5em)
$ norm(psi_(n,t)(b)^* psi_(n,t)(b)
  &+ (psi_(n,e)(c) + alpha 1_(k_n))^* (psi_(n,e)(c) + alpha 1_(k_n)) - norm(b)^2 1_(k_n)) \
  &<= norm(psi_(n,t)(b)^* psi_(n,t)(b) - psi_(n,e)(b^* b)) + norm(psi_(n,e)(c)^* psi_(n,e)(c) - psi_(n,e)(c^* c)) \
  &= norm(psi_(n,t^(-1))(b^*) psi_(n,t)(b) - psi_(n,e)(b^* b)) + norm(psi_(n,e)(c^*) psi_(n,e)(c) - psi_(n,e)(c^* c)) < 2 epsilon_n $
#v(0.5em)

#par[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

#v(0.5em)
$ &"(i) " B = B_1 union B_2, tilde(B) = E_1 union E_2 " and " omega(E_i) >= 1/2 omega(tilde(B)), i = 1,2; \
  &"(ii) " b(x) - b(y) " does not change sign for all " (x,y) in B_i times E_i, i = 1,2; \
  &"(iii) " |b(x) - m_b (tilde(B))| <= |b(x) - b(y)| " for all " (x,y) in B_i times E_i, i = 1,2. $
