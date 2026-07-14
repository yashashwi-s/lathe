#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Algorithmic Pseudocode Sample 3]
  #v(0.5em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
  #v(1.5em)
]

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#v(0.5em)

#block(stroke: 0.5pt, width: 100%, inset: 0pt)[
  #block(width: 100%, inset: (x: 6pt, y: 4pt), below: 0pt)[
    *Algorithm 1* Source-backed algorithmic procedure
  ]
  #line(length: 100%, stroke: 0.5pt)
  #block(width: 100%, inset: (x: 6pt, y: 4pt), above: 0pt, below: 0pt)[
    #text(size: 10pt)[
      *Algorithm 1* Initialization of the control and state variables
    ]
    #v(0.4em)
    #let ind(n) = h(n * 1.5em)
    #let kw(t) = text(weight: "bold", t)
    #let cm(t) = text(style: "italic", fill: gray.darken(20%), sym.triangle.r + " " + t)

    #set par(leading: 0.55em, spacing: 0.55em)
    #text(size: 10pt)[
      #kw[for] $t in \{-1, dots, -T^"traceback"\}$ #kw[do] #h(1fr) #cm[Retrieve the values of $P_{u,t}$] \
      #ind(1)$P_{u,t} <- mono("Power.GetValue")(t)$ \
      #kw[end for] \
      #kw[for] $t in \{-1, dots, -T^"traceback"\}$ #kw[do] #h(1fr) #cm[Initial conditions on the state variables] \
      #ind(1)#kw[if] $P_{u,t} > mono("MinimumPower.GetValue")(t)$ #kw[then] \
      #ind(2)$S_{u,t}^"OFF" <- 0$ \
      #ind(2)$S_{u,t}^"STOP" <- 0$ \
      #ind(2)$S_{u,t}^"START" <- 0$ \
      #ind(2)#kw[if] $P_{u,t} < P_{u,t-1}$ #kw[then] #h(1fr) #cm[Exact initialization required only if the FLAT state is defined.] \
      #ind(3)$S_{t-1}^"ON_UP" <- 0$ \
      #ind(3)$S_{t-1}^"ON_DOWN" <- 1$ \
      #ind(3)$S_{t-1}^"ON_FLAT" <- 0$ \
      #ind(2)#kw[else if] $P_{u,t} > P_{u,t-1}$ #kw[then] \
      #ind(3)$S_{t-1}^"ON_UP" <- 1$ \
      #ind(3)$S_{t-1}^"ON_DOWN" <- 0$ \
      #ind(3)$S_{t-1}^"ON_FLAT" <- 0$ \
      #ind(2)#kw[else if] $P_{u,t} = P_{u,t-1}$ #kw[then] \
      #ind(3)$S_{t-1}^"ON_UP" <- 0$ \
      #ind(3)$S_{t-1}^"ON_DOWN" <- 0$ \
      #ind(3)$S_{t-1}^"ON_FLAT" <- 1$ \
      #ind(2)#kw[end if] \
      #ind(1)#kw[else if] $P_{u,t} > 0$ #kw[then] #h(1fr) #cm[Reconstruct the startups and shutdowns] \
      #ind(2)#kw[if] $P_{u,t} < P_{u,t-1}$ #kw[then] \
      #ind(3)$S_{t}^"STOP" <- 1$ \
      #ind(3)$S_{t}^"START" <- 0$ \
      #ind(2)#kw[else] \
      #ind(3)$S_{t}^"STOP" <- 0$ \
      #ind(3)$S_{t}^"START" <- 1$ \
      #ind(2)#kw[end if] \
      #ind(1)#kw[else] #h(1fr) #cm[Final possibility: the unit is OFF.] \
      #ind(2)$S_{u,t}^"OFF" <- 1$ \
      #ind(2)$S_{u,t}^"STOP" <- 0$ \
      #ind(2)$S_{u,t}^"START" <- 0$ \
      #ind(2)$S_{t-1}^"ON_UP" <- 0$ \
      #ind(2)$S_{t-1}^"ON_DOWN" <- 0$ \
      #ind(2)$S_{t-1}^"ON_FLAT" <- 0$ \
      #ind(1)#kw[end if] \
      #kw[end for]
    ]
    #v(0.4em)
  ]
  #line(length: 100%, stroke: 0.5pt)
]
