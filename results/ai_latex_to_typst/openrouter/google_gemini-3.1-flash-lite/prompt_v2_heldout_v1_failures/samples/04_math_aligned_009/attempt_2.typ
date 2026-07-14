#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center, text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures])
#align(center, [Source-backed grouped formula sample])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
B := A^* union (A^* + c) \
C := (A^* + 7c - d) union (A^* + 8c - d) \
D := (A^* + 10c - d) union (A^* + 11c - d) \
E := (A^* + 17c - 2d) union (A^* + 18c - 2d) \
F := (A^* + 30c - 3d) union (A^* + 31c - 3d) \
G := (A^* + 37c - 4d) union (A^* + 38c - 4d) \
H := (A^* + 40c - 4d) union (A^* + 41c - 4d) \
I := (A^* + 47c - 5d) union (A^* + 48c - 5d) \
J := B union C union D union E union F union G union H union I
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

#text("Delta_{(n+1 l-1)}^{(0)}(x_1,...,x_m|z_1,...,z_{n+1}|z_{n+2},...,z_N) = sum_{k=1}^{n+1} (prod_{i=n+2}^{N}(z_i-z_k q^{-2})) / (prod_{j=1, j != k}^{n+1} (z_k-z_j)q^{-1}) Delta^{(n l)}(x_1,...,x_m|z_1,...,z_{n+1}|z_k, z_{n+2},...,z_N)")

*Expression 3.* The following expression is taken from a source-backed formula corpus.

#text("| ||phi_{n,t}(b)||^2 - ||b||^2 | = | ||phi_{n,t}(b)^* phi_{n,t}(b)|| - ||b^* b|| |")
#text("<= | ||phi_{n,t^{-1}}(b^*)|| phi_{n,t}(b) - ||phi_{n,e}(b^* b)|| | + | ||phi_{n,e}(b^* b)|| - ||b^* b|| |")
#text("<= | ||phi_{n,t^{-1}}(b^*) phi_{n,t}(b) - phi_{n,e}(b^* b)|| | + | ||phi_{n,e}(b^* b)|| - ||b^* b|| |")

*Expression 4.* The following expression is taken from a source-backed formula corpus.

#text("[ M_i , p_j ] = i epsilon_{ijk} p_k , [ M_i , p_0 ] = 0")
#text("[ N_i , p_0 ] = i p_i , [ p_mu , p_nu ] = 0")
#text("[ N_i , p_j ] = i delta_{ij} [ kappa c sinh(p_0 / kappa c) e^{-p_0 / kappa c} + 1/(2 kappa c) (p)^2 ] - i / (kappa c) p_i p_j")

*Expression 5.* The following expression is taken from a source-backed formula corpus.

#text("X_1 := { w in W_per^{1,r}(S) : w = 0 on { zeta = -1 } }")
#text("X_2 := L^infinity([-1,0])")
#text("Y := { u in (W_per^{1,r'}(S))^* : u = A + partial_xi B_1 + partial_zeta B_2, for A, B_1, B_2 in L^r(S) }")
