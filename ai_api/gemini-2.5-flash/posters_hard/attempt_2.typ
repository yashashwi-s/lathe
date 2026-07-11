#set page(paper: "a0", margin: 4cm)

// Title and Subtitle
#align(center)[
  #set text(size: 80pt, weight: "bold")
  Advancements in Solid-State Battery Technologies \
  #set text(size: 48pt)
  Energy Research Laboratory
]

#v(2cm)

// Set default text size for the main content block
#set text(size: 28pt)

// Set properties for section-like headings
#set heading(level: 2, text(size: 36pt, weight: "bold"))
#set heading(outlined: false) // Ensure no outline is generated

#columns(3, [
  #heading(level: 2, "Introduction")
  Solid-state electrolytes offer significant safety advantages over volatile liquid counterparts.

  #heading(level: 2, "Methodology")
  We synthesized a lithium-lanthanum-zirconium-oxide (LLZO) ceramic membrane.

  #heading(level: 2, "Results")
  Ionic conductivity reached $10^-3$ S/cm at room temperature.
])