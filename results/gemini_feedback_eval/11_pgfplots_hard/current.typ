// The original LaTeX code uses PGFPlots to generate a 3D surface plot.
// Typst does not have a built-in 3D plotting engine for such complex graphics.
// The idiomatic and recommended way to include plots like this in Typst
// is to generate them externally using a dedicated plotting library
// (e.g., Python's Matplotlib/Plotly, Gnuplot, R, Julia's Plots.jl, etc.)
// and then include the resulting image (SVG, PNG, PDF) in your Typst document.

// The previous attempt failed because "surface_plot.svg" was not found.
// This file needs to be generated externally and placed in the same directory
// as your Typst file, or its path needs to be specified correctly.

// As a placeholder, we will display a message.
// To see the actual plot, you must generate "surface_plot.svg" yourself
// using an external tool and then uncomment the 'image' line below.

#figure(
  // Uncomment the line below and ensure 'surface_plot.svg' exists
  // image("surface_plot.svg", width: 80%),

  // Placeholder content when the image is not available:
  box(
    width: 80%,
    height: 200pt, // Approximate height for a plot
    stroke: 1pt + gray,
    align(center, text(red)[
      _3D Plot Placeholder_ \
      Please generate `surface_plot.svg` externally \
      (e.g., using Python/Matplotlib, Gnuplot, etc.) \
      and place it in the document directory. \
      Then uncomment the `image()` line in the source.
    ])
  ),
  caption: [A 3D surface plot of $z = exp(-x^2-y^2)$.]
)