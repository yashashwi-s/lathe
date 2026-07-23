#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "serif")

#align(center)[
  #text(size: 1.44em, weight: "bold")[Equation Sample 5] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #text(size: 1em)[]
]

= Derivation
The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

$
  &v_(m n)^x \
  &= angle.l m | v^x | n angle.r \
  &= delta_(m n) angle.l v^x angle.r (k_x / rho) (-delta_(m,0) + delta_(m,1)) \
  &quad + (1 - delta_(m n)) angle.l v^x angle.r (k_z / rho (k_x / sqrt(k_x^2 + k_y^2)) - i (k_y / sqrt(k_x^2 + k_y^2))) \
  &= delta_(m n) angle.l v^x angle.r (op("sin") theta op("cos") phi) (-delta_(m,0) + delta_(m,1)) \
  &quad + (1 - delta_(m n)) angle.l v^x angle.r (op("cos") theta op("cos") phi - i op("sin") phi), \
  &v_(m n)^y \
  &= delta_(m n) angle.l v^y angle.r (op("sin") theta op("sin") phi) (-delta_(m,0) + delta_(m,1)) \
  &quad + (1 - delta_(m n)) angle.l v^y angle.r (op("cos") theta op("sin") phi - i op("cos") phi), \
  &v_(m n)^z \
  &= delta_(m n) angle.l v^z angle.r op("cos") theta (-delta_(m,0) + delta_(m,1)) \
  &quad + (1 - delta_(m n)) angle.l v^z angle.r (-op("sin") theta) / rho,
$
