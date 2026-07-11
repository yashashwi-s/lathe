#set page(width: auto, height: auto, margin: 1in)
#set text(size: 10pt)

#v(1in)

#align(center)[
  #context {
    #move(x: 1.58cm, y: 0cm)[
      #align(bottom + center, text("Pascal's Triangle Structure"))
    ]

    #for i in range(1, 6) {
      #for j in range(1, i + 1) {
        #let tikz_x = (j - i/2) * 1cm
        #let tikz_y = (-i * 0.8) * 1cm

        #let typst_x = tikz_x + 1.58cm
        #let typst_y = -tikz_y - 0.5cm

        #move(x: typst_x, y: typst_y)[
          #circle(radius: 0.08cm, fill: black)
        ]
      }
    }
  }
]