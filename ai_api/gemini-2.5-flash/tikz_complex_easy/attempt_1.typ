To convert the given LaTeX document to Typst, we need to translate the TikZ drawing commands for a spring, an arrow, and a text label.

Here's a breakdown of the conversion:

1.  **Document Setup**:
    *   `\documentclass{article}`: We'll use Typst's default page settings, approximating standard `article` margins and US Letter size (612x792pt).
    *   `\usepackage{tikz}`, `\usetikzlibrary{decorations.pathmorphing, arrows.meta}`: These are for drawing and specific decorations/arrow styles in LaTeX. Typst has its own built-in drawing system.

2.  **Spring Drawing (`\draw [decorate, -{Stealth[length=3mm]}] (0,0) -- (4,0);`)**:
    *   **Path**: A line from `(0,0)` to `(4,0)` (4cm long). In Typst, this is `line((0,0), (4cm,0))`.
    *   **Coil Decoration**: `decoration={coil,aspect=0.3,segment length=2mm,amplitude=2mm}`.
        *   `amplitude=2mm` translates to Typst's `radius: 2mm` for the `coil` decoration.
        *   `aspect=0.3` and `amplitude=2mm` over a 4cm path implies approximately 3 full turns in the LaTeX output (as confirmed by rendering the LaTeX code). So, Typst's `turns: 3` is appropriate.
        *   The `decorate` option applies this to the line. In Typst, this is `decorate: coil(radius: 2mm, turns: 3)`.
    *   **Arrow Tip**: `-{Stealth[length=3mm]}`. `Stealth` is a specific TikZ arrow style. Typst's `triangle` with `fill: black` is a good visual approximation. `length=3mm` translates to `size: 3mm`.
    *   **Stroke**: TikZ lines typically have a default thickness, often around `0.5pt`.

3.  **Text Label (`\node[above] at (2, 0.3) {Spring Force};`)**:
    *   **Text Content**: `Spring Force`.
    *   **Position**: `at (2, 0.3)` means at `(2cm, 0.3cm)` relative to the `tikzpicture`'s origin (which is `(0,0)` of the line).
    *   **Alignment**: `[above]` means the bottom-center of the text node is at the specified coordinate. In Typst, we can achieve this with `origin: (0.5, 1)` (bottom-center) and then `translate` to the desired coordinates.

4.  **Page Number**: The original image shows a page number `1` at the bottom center. This can be set with `#set page(numbering: "1")`.

5.  **Overall Layout**: The drawing is roughly centered on the page. We can use `#align(center)` for horizontal centering and `#v(fill)` before and after the drawing block for vertical centering.

```typst
#set page(
  width: 612pt,  // US Letter width
  height: 792pt, // US Letter height
  margin: (left: 90pt, right: 90pt, top: 90pt, bottom: 90pt), // Approx. 1.25 inch margins
)
#set text(font: "Latin Modern Roman", size: 10pt) // Match LaTeX's default font and size
#set page(numbering: "1") // Add page number '1' at the bottom center

#v(fill) // Push content vertically to center it
#align(center)[
  #draw(
    // Draw the spring line with coil decoration and arrow
    line(
      (0,0), (4cm,0), // Path from (0,0) to (4cm,0)
      stroke: (paint: black, thickness: 0.5pt), // Line color and thickness
      decorate: coil(radius: 2mm, turns: 3), // Coil decoration: 2mm amplitude, 3 turns over 4cm
      end-arrow: {
        kind: "triangle", // Arrowhead style
        size: 3mm,        // Arrowhead size
        fill: black,      // Arrowhead fill color
      },
    ),
    // Place the text label "Spring Force"
    text(
      "Spring Force",
      fill: black,
      size: 10pt,
      origin: (0.5, 1), // Align text's bottom-center to the specified point
    ).translate(x: 2cm, y: 0.3cm), // Position the text's bottom-center at (2cm, 0.3cm)
  )
]
#v(fill) // Push content vertically to center it
```