#import "@preview/fontawesome:0.5.0": *

#set page(
  paper: "a4",
  margin: (top: 1.27cm, left: 1cm, right: 1cm, bottom: 2cm),
)

#set text(font: "Helvetica", size: 10pt)
#set par(spacing: 0.65em)

// Colors
#let ecv-blue = rgb("#003399")
#let ecv-light = rgb("#e6ebf5")

// Helper: two-column row
#let ecv-row(label, content, top-space: 4pt) = {
  v(top-space)
  grid(
    columns: (3.5cm, 1fr),
    gutter: 0.5cm,
    align(top + right, text(fill: ecv-blue, weight: "bold", size: 9pt, label)),
    align(top + left, content),
  )
}

// Section header
#let ecv-section(title) = {
  v(8pt)
  block(
    width: 100%,
    fill: ecv-blue,
    inset: (x: 4pt, y: 3pt),
    text(fill: white, weight: "bold", size: 10pt, upper(title))
  )
}

// ─── HEADER ─────────────────────────────────────────────────────────────────
#block(
  width: 100%,
  fill: ecv-light,
  inset: (x: 8pt, y: 6pt),
)[
  #grid(
    columns: (1fr, auto),
    [
      #text(size: 16pt, weight: "bold", fill: ecv-blue)[Name, Surname]
    ],
    [],
  )

  #v(4pt)

  #let info-row(label, value) = {
    grid(
      columns: (3.5cm, 1fr),
      gutter: 0.5cm,
      align(right, text(fill: ecv-blue, weight: "bold", size: 9pt, label)),
      align(left, text(size: 9pt, value)),
    )
    v(1pt)
  }

  #info-row("Address:", "(Remove if not relevant), (Remove if not relevant), (Remove if not relevant)")
  #info-row("Telephone:", "(Remove if not relevant)")
  #info-row("Mobile:", "(Remove if not relevant)")
  #info-row("Fax:", "(Remove if not relevant)")
  #info-row("E-mail:", link("mailto:email@email.com")[email\@email.com])
  #info-row("Professional e-mail:", link("mailto:email@email.it")[email\@email.it])
  #info-row("PEC:", link("mailto:emailo@pec.it")[email\@pec.it])
  #info-row("Homepage:", link("https://www.homepage.com")[www.homepage.com])
  #info-row("Matrix/Riot:", "(Remove if not relevant)")
  #info-row("Skype:", "(Remove if not relevant)")
  #info-row("YouTube:", link("https://www.youtube.com/myChannel")[www.youtube.com/myChannel])
  #info-row("Nationality:", "(Remove if not relevant)")
  #info-row("Date of birth:", "(Remove if not relevant)")
  #info-row("Gender:", "(Remove if not relevant)")
]

#v(6pt)

// Desired employment
#ecv-row(
  [Desired employment /\nOccupational field],
  text(size: 12pt, weight: "bold")[(Remove if not relevant)],
  top-space: 6pt,
)

// ─── WORK EXPERIENCE ────────────────────────────────────────────────────────
#ecv-section("Work experience")

#ecv-row("Dates", [Add separate entries for each relevant post occupied, starting from the most recent. (Remove if not relevant).])
#ecv-row("Occupation or position held", […])
#ecv-row("Main activities and responsibilities", […])
#ecv-row("Name and address of employer", […])
#ecv-row("Type of business or sector", […])

// ─── EDUCATION AND TRAINING ─────────────────────────────────────────────────
#ecv-section("Education and training")

#ecv-row("Dates", [Add separate entries for each relevant course you have completed, starting from the most recent. (Remove if not relevant).])
#ecv-row("Title of qualification awarded", […])
#ecv-row("Principal subjects / Occupational skills covered", […])
#ecv-row("Name and type of organization providing education and training", […])
#ecv-row(
  "Level in national or international classification",
  […#super([1])],
)

#v(2pt)
#text(size: 8pt)[#super([1])If appropriate.]

// ─── PERSONAL SKILLS AND COMPETENCES ────────────────────────────────────────
#ecv-section("Personal skills and competences")

#v(5pt)
#ecv-row(
  "Mother tongue(s)",
  text(weight: "bold")[Specify mother tongue],
)

#v(5pt)
#ecv-row(
  "Other language(s)",
  text(size: 12pt)[],
)

// Language table header
#v(4pt)
#block(width: 100%, inset: (left: 4.1cm))[
  #set text(size: 8pt, fill: ecv-blue, weight: "bold")
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr, 1fr),
    gutter: 2pt,
    grid.cell(colspan: 2, align(center)[UNDERSTANDING]),
    grid.cell(colspan: 2, align(center)[SPEAKING]),
    align(center)[WRITING],
  )
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr, 1fr),
    gutter: 2pt,
    align(center)[Listening],
    align(center)[Reading],
    align(center)[Spoken interaction],
    align(center)[Spoken production],
    align(center)[],
  )
]

// Language rows
#let lang-row(lang) = {
  v(2pt)
  block(width: 100%, inset: (left: 0pt))[
    #grid(
      columns: (3.5cm, 0.5cm, 1fr, 1fr, 1fr, 1fr, 1fr),
      gutter: 2pt,
      align(right + top, text(fill: ecv-blue, weight: "bold", size: 9pt, lang)),
      [],
      align(center)[],
      align(center)[],
      align(center)[],
      align(center)[],
      align(center)[],
    )
  ]
}

#lang-row("Language")
#lang-row("Language")

#v(4pt)
#block(width: 100%, inset: (left: 4.1cm))[
  #set text(size: 8pt)
  (*) Common European Framework of Reference for Languages
]

#v(10pt)
#ecv-row(
  text(size: 12pt)[Social skills and\ncompetences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Organisational skills\nand competences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Technical skills and\ncompetences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Computer skills and\ncompetences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Artistic skills and\ncompetences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Other skills and\ncompetences],
  [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).],
  top-space: 10pt,
)
#ecv-row(
  text(size: 12pt)[Driving licence(s)],
  [State here whether you hold a driving licence and if so for which categories of vehicle. (Remove if not relevant).],
)

// ─── ADDITIONAL INFORMATION ──────────────────────────────────────────────────
#ecv-section("Additional information")

#ecv-row(
  "",
  [Include here any other information that may be relevant, for example contact persons, references, etc. (Remove heading if not relevant).],
  top-space: 10pt,
)
#ecv-row("", text(weight: "bold")[Personal interests])
#ecv-row("", […])

// ─── ANNEXES ────────────────────────────────────────────────────────────────
#ecv-section("Annexes")

#ecv-row("", [List any item attached to the CV])

// ─── SIGNATURE ───────────────────────────────────────────────────────────────
#v(5.0cm)
#v(-2.5cm)

#v(0.5cm)
#let today-str = "14 July 2026"

#grid(
  columns: (2fr, 1fr),
  [
    #text[Place #smallcaps[(Province)], #today-str]
    #v(0.3cm)
    #line(length: 7cm)
    #v(0.1cm)
    #text(size: 9pt)[Place and date]
  ],
  [
    #v(0.63cm)
    #line(length: 5cm)
    #v(0.1cm)
    #h(1.5cm)#text[Name Surname]
  ],
)

// Footer
#place(
  bottom + center,
  dy: -0.5cm,
  block(width: 100%)[
    #line(length: 100%, stroke: 0.5pt + ecv-blue)
    #v(2pt)
    #align(center)[
      #text(size: 8pt, fill: ecv-blue)[Name, Surname]
      #h(1em) | #h(1em)
      #text(size: 8pt)[Page #counter(page).display() / #context counter(page).final().at(0)]
    ]
  ]
)
