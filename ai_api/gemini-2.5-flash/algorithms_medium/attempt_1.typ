#set page(
  width: auto,
  height: auto,
  margin: 1in,
)

// Define the thickness for the horizontal rules, matching LaTeX's \hrule
#let rule_thickness = 0.4pt

// Top horizontal rule
#line(length: 100%, stroke: rule_thickness)
#v(0.5em) // Vertical space after the top rule

// Algorithm caption
#block(
  width: 100%,
  inset: (left: 0pt, right: 0pt), // No horizontal padding for the caption block
)[
  #text(weight: "bold")[Algorithm 1] Binary Search Validation
]

#v(0.5em) // Vertical space before the middle rule
// Middle horizontal rule
#line(length: 100%, stroke: rule_thickness)
#v(0.5em) // Vertical space after the middle rule

// Pseudocode body
#block(
  width: 100%,
  inset: (left: 0pt, right: 0pt), // No horizontal padding for the pseudocode block
)[
  // Define the standard indentation step for pseudocode lines
  #let indent_step = 1.5em

  // If statement
  #text(weight: "bold")[if] $target = array[mid]$ #text(weight: "bold")[then]
  #indent(indent_step)[
    #text(weight: "bold")[return] $mid$
  ]

  // Else If statement
  #text(weight: "bold")[else if] $target < array[mid]$ #text(weight: "bold")[then]
  #indent(indent_step)[
    $high <- mid - 1$
  ]

  // Else statement
  #text(weight: "bold")[else]
  #indent(indent_step)[
    $low <- mid + 1$
  ]

  // End If statement
  #text(weight: "bold")[end if]
]

#v(0.5em) // Vertical space before the bottom rule
// Bottom horizontal rule
#line(length: 100%, stroke: rule_thickness)