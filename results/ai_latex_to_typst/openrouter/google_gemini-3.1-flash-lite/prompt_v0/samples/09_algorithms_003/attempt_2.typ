#set page(margin: 1in)
#set text(size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 3] \
  Source-backed Image2Struct algorithm sample \
  #v(1em)
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  block(stroke: 0.5pt + black, inset: 10pt)[
    #set align(left)
    #let comment(c) = h(1fr) + text(fill: gray)[// #c]
    #let indent = h(2em)

    *for* $t in {-1, dots.h, -T^"traceback"}$ #comment("Retrieve the values of " + $P_(u,t)$) \
    #indent $P_(u,t) arrow.l "Power.GetValue"(t)$ \
    *end for* \
    *for* $t in {-1, dots.h, -T^"traceback"}$ #comment("Initial conditions on the state variables") \
    #indent *if* $P_(u,t) > "MinimumPower.GetValue"(t)$ \
    #indent #indent $S_(u,t)^"OFF" arrow.l 0$ \
    #indent #indent $S_(u,t)^"STOP" arrow.l 0$ \
    #indent #indent $S_(u,t)^"START" arrow.l 0$ \
    #indent #indent *if* $P_(u,t) < P_(u,t-1)$ #comment("Exact initialization required only if the FLAT state is defined.") \
    #indent #indent #indent $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent #indent #indent $S_(t-1)^"ON_DOWN" arrow.l 1$ \
    #indent #indent #indent $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent #indent *else if* $P_(u,t) > P_(u,t-1)$ \
    #indent #indent #indent $S_(t-1)^"ON_UP" arrow.l 1$ \
    #indent #indent #indent $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent #indent #indent $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent #indent *else if* $P_(u,t) = P_(u,t-1)$ \
    #indent #indent #indent $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent #indent #indent $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent #indent #indent $S_(t-1)^"ON_FLAT" arrow.l 1$ \
    #indent #indent *end if* \
    #indent *else if* $P_(u,t) > 0$ #comment("Reconstruct the startups and shutdowns") \
    #indent #indent *if* $P_(u,t) < P_(u,t-1)$ \
    #indent #indent #indent $S_t^"STOP" arrow.l 1$ \
    #indent #indent #indent $S_t^"START" arrow.l 0$ \
    #indent #indent *else* \
    #indent #indent #indent $S_t^"STOP" arrow.l 0$ \
    #indent #indent #indent $S_t^"START" arrow.l 1$ \
    #indent #indent *end if* \
    #indent *else* #comment("Final possibility: the unit is OFF.") \
    #indent #indent $S_(u,t)^"OFF" arrow.l 1$ \
    #indent #indent $S_(u,t)^"STOP" arrow.l 0$ \
    #indent #indent $S_(u,t)^"START" arrow.l 0$ \
    #indent #indent $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent #indent $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent #indent $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent *end if* \
    *end for*
  ],
  caption: [Initialization of the control and state variables]
)
