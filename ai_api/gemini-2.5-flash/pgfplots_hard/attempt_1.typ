To convert the given LaTeX document to Typst, we need to use a Typst package that supports 3D plotting, as Typst's built-in `plot` function is primarily for 2D. The `@preview/plot-3d` package is suitable for this purpose. We also need the `@preview/calc` package for mathematical functions like `exp` and `pow`.

Here's the equivalent Typst code:

```typst
#set page(
  width: 612pt,
  height: 792pt,
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in), // Standard article margins
)
#set text(font: "Latin Modern Math", lang: "en") // Use Latin Modern Math for consistency with LaTeX

// Import the 3D plotting package and the calculation package
#import "@preview/plot-3d:0.1.0": *
#import "@preview/calc:0.1.0" as calc

// Center the plot on the page
#align(center)[
  #plot-3d(
    width: 15cm, // Adjust width to visually match the reference image
    height: 15cm, // Adjust height to visually match the reference image
    view-azimuth: 60deg, // Corresponds to LaTeX's view={60}{...}
    view-elevation: 30deg, // Corresponds to LaTeX's view={...}{30}
    x-label: $x$, // X-axis label
    y-label: $y$, // Y-axis label
    z-label: $z$, // Z-axis label
    grid: true, // Enable major grid lines
    colormap: "viridis", // Use the viridis colormap
    surface(
      // The function to plot: exp(-x^2 - y^2)
      function: (x, y) => calc.exp(-(x.pow(2)) - (y.pow(2))),
      x-domain: (-2, 2), // X-axis domain
      y-domain: (-2, 2), // Y-axis domain
      samples: 20, // Number of samples along each dimension
    )
  )
]
```