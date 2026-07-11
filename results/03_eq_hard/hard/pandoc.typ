The inverse of the partitioned block matrix is defined using the Schur
complement:
$ mat(delim: "(", A, B; C, D)^(- 1) = mat(delim: "(", A^(- 1) + A^(- 1) B\(D - C A^(- 1) B\)^(- 1)C A^(- 1), - A^(- 1) B\(D - C A^(- 1) B\)^(- 1); -\(D - C A^(- 1) B\)^(- 1)C A^(- 1), \(D - C A^(- 1) B\)^(- 1)) $
