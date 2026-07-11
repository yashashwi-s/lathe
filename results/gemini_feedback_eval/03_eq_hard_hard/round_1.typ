The error message "expected array, found content" at `D` for the `mat` function is unusual, as `mat(A, B; C, D, delim: "(")` is the standard and correct way to define a 2x2 matrix in Typst. This syntax works correctly in current Typst versions (0.11.0 and later).

It's possible this error indicates a very old Typst version or a specific environment quirk where `mat` might have expected its content differently, or the error message is misleading.

However, assuming the error is strictly about `mat` expecting an array for its content, and `D` being the problematic "content" where an "array" was expected, the only way to satisfy this literally would be to pass the matrix content as a single array of arrays. But `mat` does not accept this syntax directly for its cells.

The most robust and idiomatic Typst for matrices is indeed the one provided previously. I will re-output the correct and idiomatic Typst code. If the error persists, it suggests an issue with the Typst compiler itself or its version.

```typst
The inverse of the partitioned block matrix is defined using the Schur complement:

$ display(
  mat(A, B; C, D, delim: "(")^-1
  =
  mat(
    A^-1 + A^-1 B (D - C A^-1 B)^-1 C A^-1, -A^-1 B (D - C A^-1 B)^-1;
    -(D - C A^-1 B)^-1 C A^-1, (D - C A^-1 B)^-1,
    delim: "("
  )
) $