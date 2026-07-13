#set page(margin: 1in)
#set text(font: "Latin Modern Roman") // Match default LaTeX font

#grid(
  columns: (60%, 40%),
  gutter: 0pt, // No space between the columns, mimicking adjacent minipages

  // Left content block (mimicking first minipage)
  [
    #text(size: 1.44em, strong("Dr. Alan Turing")) \ // \Large is approximately 1.44 times normal size
    Theoretical Computer Scientist
  ],

  // Right content block (mimicking second minipage with \raggedleft)
  [
    #align(right)[
      Bletchley Park, UK \
      aturing@enigma.gov
    ]
  ],
)

// Set page footer for page number, matching LaTeX's default placement
#set page(footer: align(center, counter(page).display("1")))