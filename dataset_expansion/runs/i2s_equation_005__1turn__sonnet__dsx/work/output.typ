#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true)
#show math.equation: set text(font: "New Computer Modern Math")

#align(center)[
  #text(size: 17pt, weight: "bold")[Equation Sample 5]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(0.5em)

$
v_(m n)^x
&= angle.l m | v^x | n angle.r \
&= delta_(m n) angle.l v^x angle.r (k_x / rho)(-delta_(m,0) + delta_(m,1))
+ (1 - delta_(m n)) angle.l v^x angle.r (k_z / rho dot k_x / sqrt(k_x^2 + k_y^2) - i k_y / sqrt(k_x^2 + k_y^2)) \
&= delta_(m n) angle.l v^x angle.r (sin theta cos phi)(-delta_(m,0) + delta_(m,1))
+ (1 - delta_(m n)) angle.l v^x angle.r (cos theta cos phi - i sin phi), \
v_(m n)^y
&= delta_(m n) angle.l v^y angle.r (sin theta sin phi)(-delta_(m,0) + delta_(m,1))
+ (1 - delta_(m n)) angle.l v^y angle.r (cos theta sin phi - i cos phi), \
v_(m n)^z
&= delta_(m n) angle.l v^z angle.r cos theta (-delta_(m,0) + delta_(m,1))
+ (1 - delta_(m n)) angle.l v^z angle.r (-sin theta) / rho, \
$
