#set page(width: auto, height: auto, margin: 1in) // Set page to auto-fit content with 1-inch margins

// Define a reusable style for the flowchart nodes
#let node_style(content) = rect(
  stroke: 1pt + black, // Draw a 1pt black border
  fill: rgb("#dde6ff"), // Fill with a light blue color (approximates blue!10)
  inset: (x: 10pt, y: 5pt), // Add horizontal and vertical padding
  radius: 2pt, // Slightly rounded corners
  min-height: 1cm, // Ensure a minimum height of 1cm
  align(center, content), // Center the text horizontally and vertically
)

// Define constants for spacing and arrow thickness
#let node_distance = 2cm
#let arrow_thickness = 1.5pt // "thick" in TikZ is often around 1.5pt

// Center the entire diagram on the page
#align(center, {
  // Use layout to measure node sizes before positioning them
  #layout(it => {
    // Create the content for each node
    let node_a_content = node_style("Input Data")
    let node_b_content = node_style("Feature Extraction")
    let node_c_content = node_style("Classification")

    // Measure the actual size of each node
    let measured_a = measure(node_a_content, it.rest)
    let measured_b = measure(node_b_content, it.rest)
    let measured_c = measure(node_c_content, it.rest)

    // Calculate the top-left positions of each node, starting node A at (0,0)
    let pos_a_tl = (0pt, 0pt)
    let pos_b_tl = (pos_a_tl.x + measured_a.width + node_distance, 0pt)
    let pos_c_tl = (pos_b_tl.x + measured_b.width + node_distance, 0pt)

    // Determine the overall width and height needed for the bounding box
    let total_width = pos_c_tl.x + measured_c.width
    let max_height = max(measured_a.height, measured_b.height, measured_c.height)

    // Create a box to serve as the drawing canvas
    box(
      width: total_width,
      height: max_height,
      // Place the nodes within the box using their calculated top-left positions
      place(pos_a_tl.x, pos_a_tl.y, node_a_content),
      place(pos_b_tl.x, pos_b_tl.y, node_b_content),
      place(pos_c_tl.x, pos_c_tl.y, node_c_content),

      // Draw the arrows between the nodes
      // Arrow from A to B
      line(
        (pos_a_tl.x + measured_a.width, pos_a_tl.y + measured_a.height / 2), // Right-middle of node A
        (pos_b_tl.x, pos_b_tl.y + measured_b.height / 2), // Left-middle of node B
        stroke: arrow_thickness + black,
        end: arrow.head, // Add an arrow head at the end
      ),
      // Arrow from B to C
      line(
        (pos_b_tl.x + measured_b.width, pos_b_tl.y + measured_b.height / 2), // Right-middle of node B
        (pos_c_tl.x, pos_c_tl.y + measured_c.height / 2), // Left-middle of node C
        stroke: arrow_thickness + black,
        end: arrow.head, // Add an arrow head at the end
      ),
    )
  })
})

// Add page number at the bottom center, matching the original LaTeX output
#set align(bottom + center)
#page-number()