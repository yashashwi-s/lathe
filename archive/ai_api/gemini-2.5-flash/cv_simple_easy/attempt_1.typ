#set text(font: "Latin Modern Roman") // Matches LaTeX's default font (Computer Modern)

#set page(
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in), // Standard article class margins
  footer: align(center, [#page-number]), // Page number at the bottom center
)

// Center the name and contact information
#align(center)[
  #set text(size: 17.28pt) // Corresponds to LaTeX's \LARGE font size
  *Eleanor Rigby*

  #v(2mm) // Vertical space equivalent to \vspace{2mm}
  eleanor.rigby@abbeyroad.com | (555) 123-4567 | London, UK
]

#v(5mm) // Vertical space equivalent to \vspace{5mm}

// The following paragraph is left-aligned by default in Typst,
// so \noindent is implicitly handled as Typst paragraphs don't indent by default.
Dedicated community organizer and architectural observer with 10 years of experience in localized demographic studies.