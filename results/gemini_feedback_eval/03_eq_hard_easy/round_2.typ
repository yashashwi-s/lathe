The errors indicate that the content within the `#align` function is being parsed as regular Typst code rather than mathematical expressions. This is unexpected for a math function like `align` when used inside a math block (`$ ... $`).

To explicitly tell Typst that each argument to `#align` is a mathematical expression, we can wrap each line in the `math()` function. This forces the parser to interpret the content as math, resolving the "invalid number suffix", "invalid character `&`", and "unexpected equals sign" errors.

```typst
The system of linear equations can be represented as:
$
#align(
  math(3x + 2y - z & = 1),
  math(2x - 2y + 4z & = -2),
  math(-x + frac(1, 2)y - z & = 0),
)
$