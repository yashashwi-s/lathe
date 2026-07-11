#import "@preview/plot:0.1.0" as plot
#import "@preview/calc:0.1.0" as calc

// Set the page layout to match the default 'article' class in LaTeX.
// A common default paper size for 'article' is Letter (8.5in x 11in),
// which corresponds to 612pt x 792pt.
// Default margins for 'article' are often around 1 inch.
#set page(
  paper: "letter",
  margin: 1in,
  // Add a footer with the page number, centered, to match the LaTeX output.
  footer: [
    #h(1fr) #text(10pt, counter(page).display()) #h(1fr)
  ]
)

// Create the plot.
// The plot is a block element and will be placed at the top-left
// of the content area, respecting the page margins, similar to LaTeX.
#plot.plot(
  width: 8cm,
  height: 6cm,
  // Enable major grid lines for both x and y axes, matching 'grid=major'.
  x-grid: true,
  y-grid: true,
  // Set the visible range of the x-axis, matching the LaTeX output's axis labels.
  x-domain: (-6, 6),
  // Set the visible range of the y-axis, matching the LaTeX output's axis labels.
  y-domain: (-1, 1),
  // Define x-axis ticks to appear every 2 units, matching the LaTeX output.
  x-ticks: (step: 2),
  // Define y-axis ticks to appear every 1 unit, matching the LaTeX output.
  y-ticks: (step: 1),
  // Add the sine function plot.
  plot.func(
    // The function to plot is `sin(x)`. In pgfplots, `sin(deg(x))` is used
    // to plot `sin(x)` where `x` is in radians, as `sin` by default expects degrees.
    // Typst's `calc.sin` directly expects radians.
    func: calc.sin,
    // The domain over which the function is evaluated and drawn, matching LaTeX's `domain=-5:5`.
    domain: (-5, 5),
    // Set the line color to blue and thickness to 'thick' (typically 1.5pt in pgfplots).
    stroke: (paint: blue, thickness: 1.5pt),
    // Number of samples for the function, matching LaTeX's `samples=50`.
    samples: 50,
  )
)