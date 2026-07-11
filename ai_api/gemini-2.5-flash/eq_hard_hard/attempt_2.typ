#set page(width: auto, height: auto) // Match the reference render's implicit page size

The inverse of the partitioned block matrix is defined using the Schur complement:
$
#mat(A, B; C, D)^(-1)
=
#mat(
  A^(-1) + A^(-1) B (D - C A^(-1) B)^(-1) C A^(-1), -A^(-1) B (D - C A^(-1) B)^(-1);
  -(D - C A^(-1) B)^(-1) C A^(-1), (D - C A^(-1) B)^(-1)
)
$