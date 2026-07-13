#set page(width: 363pt, height: 272pt, margin: (left: 15pt, right: 15pt, top: 15pt, bottom: 15pt))
#set text(font: "CMU Serif", size: 10pt) // Using CMU Serif for a Beamer-like font

// Define Beamer-like colors
#let beamer-blue = rgb("#336699") // A common Beamer blue for titles
#let block-title-bg = rgb("#DDEEFF") // Light blue for block title
#let alertblock-title-bg = rgb("#FFCCCC") // Light red for alertblock title
#let alertblock-content-bg = rgb("#FFF0F0") // Very light red for alertblock content
#let alertblock-border-color = rgb("#FF9999") // Red for alertblock border

// Custom block function to mimic Beamer's \begin{block}
#let beamer-block(title, body) = {
  v(1em) // Spacing before the block
  // Title part of the block
  rect(
    fill: block-title-bg,
    radius: (top-left: 4pt, top-right: 4pt, bottom-left: 0pt, bottom-right: 0pt),
    inset: (x: 10pt, y: 5pt),
    width: 100%,
    [
      #text(weight: "bold", title)
    ]
  )
  // Body part of the block
  rect(
    fill: white,
    radius: (top-left: 0pt, top-right: 0pt, bottom-left: 4pt, bottom-right: 4pt),
    inset: (x: 10pt, y: 10pt),
    stroke: (paint: gray, thickness: 0.5pt), // Corrected stroke syntax
    width: 100%,
    [
      #body
    ]
  )
}

// Custom alertblock function to mimic Beamer's \begin{alertblock}
#let beamer-alertblock(title, body) = {
  v(1em) // Spacing before the block
  // Title part of the alertblock
  rect(
    fill: alertblock-title-bg,
    radius: (top-left: 4pt, top-right: 4pt, bottom-left: 0pt, bottom-right: 0pt),
    inset: (x: 10pt, y: 5pt),
    width: 100%,
    [
      #text(weight: "bold", title)
    ]
  )
  // Body part of the alertblock
  rect(
    fill: alertblock-content-bg,
    radius: (top-left: 0pt, top-right: 0pt, bottom-left: 4pt, bottom-right: 4pt),
    inset: (x: 10pt, y: 10pt),
    stroke: (paint: alertblock-border-color, thickness: 0.5pt), // Corrected stroke syntax
    width: 100%,
    [
      #body
    ]
  )
}

// --- Page 1: Title Page ---
#align(center)[
  #v(80pt) // Adjust vertical position to match the reference image
  #text(fill: beamer-blue, size: 20pt, "Quarterly Financial Review")
  #v(1.5em) // Vertical spacing
  #text(size: 14pt, "CFO Office")
  #v(1em) // Vertical spacing
  #text(size: 12pt, "July 9, 2026")
]

// --- Page 2: Revenue Breakdown ---
#pagebreak()
#align(left)[
  #text(fill: beamer-blue, size: 14pt, weight: "bold", "Revenue Breakdown")
]

#beamer-block[Q2 Highlights][
  Software licensing revenue grew by 22% year-over-year, largely driven by enterprise renewals.
]

#beamer-alertblock[Risk Factors][
  Hardware supply chain disruptions present a continuous challenge through Q3.
]