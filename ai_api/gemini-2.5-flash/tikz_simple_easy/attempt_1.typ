To convert the given LaTeX document, which uses `tikz` to draw two intersecting lines, to Typst, we will use Typst's drawing capabilities. The `draw` package from the Typst preview repository provides a convenient way to create vector graphics similar to TikZ.

Here's a breakdown of the conversion steps:

1.  **Document Structure**: The LaTeX `article` class and `\begin{document}`/`\end{document}` are implicitly handled by Typst's default document structure. Typst automatically adds page numbers.
2.  **TikZ Environment**: The `tikzpicture` environment is replaced by `draw.canvas` from the `@preview/draw` package. This creates a drawing canvas.
3.  **Coordinates System**: TikZ uses a standard Cartesian coordinate system where (0,0) is the origin, x increases to the right, and y increases upwards. Typst's default drawing coordinates (and most web graphics) have (0,0) at the top-left, with x increasing to the right and y increasing downwards. To match the visual output, we need to invert the y-coordinates.
    *   The maximum y-coordinate in the TikZ drawing is 2. So, a TikZ y-coordinate `y_tikz` becomes `(2 - y_tikz)` in Typst.
    *   TikZ `(0,0)` becomes Typst `(0, 2-0) = (0,2)`.
    *   TikZ `(3,2)` becomes Typst `(3, 2-2) = (3,0)`.
    *   TikZ `(0,2)` becomes Typst `(0, 2-2) = (0,0)`.
    *   TikZ `(3,0)` becomes Typst `(3, 2-0) = (3,2)`.
4.  **Drawing Lines**:
    *   The TikZ command `\draw[thick, blue] (0,0) -- (3,2);` draws a blue line from (0,0) to (3,2). After coordinate inversion, this becomes a line from `(0pt, 2pt)` to `(3pt, 0pt)` in Typst.
    *   The TikZ command `\draw[thick, red] (0,2) -- (3,0);` draws a red line from (0,2) to (3,0). After coordinate inversion, this becomes a line from `(0pt, 0pt)` to `(3pt, 2pt)` in Typst.
5.  **Line Properties**:
    *   `thick` in TikZ typically corresponds to a line width of `0.8pt`.
    *   `blue` and `red` colors are directly available in Typst.
6.  **Units**: TikZ coordinates without explicit units default to `pt`. We will use `pt` in Typst as well. The drawing is small, so `3pt` by `2pt` is appropriate.

```typst
#set page(numbering: "1") // Ensure page numbering starts at 1, though this is often the default.

// Import the draw package for vector graphics.
// The @preview prefix indicates a package from the official Typst package repository.
#import "@preview/draw:0.1.0" as draw

// Create a drawing canvas.
// We explicitly set the width and height to define the coordinate system
// and bounding box for our drawing, matching the extent of the TikZ drawing.
#draw.canvas(
  width: 3pt,
  height: 2pt,
  {
    // Draw the blue line: TikZ (0,0)--(3,2) becomes Typst (0pt,2pt)--(3pt,0pt)
    draw.path(
      points: ((0pt, 2pt), (3pt, 0pt)),
      stroke: (paint: blue, thickness: 0.8pt)
    )
    // Draw the red line: TikZ (0,2)--(3,0) becomes Typst (0pt,0pt)--(3pt,2pt)
    draw.path(
      points: ((0pt, 0pt), (3pt, 2pt)),
      stroke: (paint: red, thickness: 0.8pt)
    )
  }
)
```