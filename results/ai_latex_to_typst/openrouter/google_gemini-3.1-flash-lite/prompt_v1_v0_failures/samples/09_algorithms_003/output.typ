#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 3] \
  Source-backed Image2Struct algorithm sample \
  #v(1em)
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  block[
    #set align(left)
    #let indent = h(2em)
    #let indent2 = h(4em)
    #let indent3 = h(6em)
    #let indent4 = h(8em)

    #line(length: 100%)
    *for* $t in {-1, dots.h, -T^"traceback"}$ #h(1fr) // Retrieve the values of $P_(u,t)$ \
    #indent $P_(u,t) arrow.l "Power.GetValue"(t)$ \
    *end for* \
    *for* $t in {-1, dots.h, -T^"traceback"}$ #h(1fr) // Initial conditions on the state variables \
    #indent *if* $P_(u,t) > "MinimumPower.GetValue"(t)$ \
    #indent2 $S_(u,t)^"OFF" arrow.l 0$ \
    #indent2 $S_(u,t)^"STOP" arrow.l 0$ \
    #indent2 $S_(u,t)^"START" arrow.l 0$ \
    #indent2 *if* $P_(u,t) < P_(u,t-1)$ #h(1fr) // Exact initialization required only if the FLAT state is defined. \
    #indent3 $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent3 $S_(t-1)^"ON_DOWN" arrow.l 1$ \
    #indent3 $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent2 *else if* $P_(u,t) > P_(u,t-1)$ \
    #indent3 $S_(t-1)^"ON_UP" arrow.l 1$ \
    #indent3 $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent3 $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent2 *else if* $P_(u,t) = P_(u,t-1)$ \
    #indent3 $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent3 $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent3 $S_(t-1)^"ON_FLAT" arrow.l 1$ \
    #indent2 *end if* \
    #indent *else if* $P_(u,t) > 0$ #h(1fr) // Reconstruct the startups and shutdowns \
    #indent2 *if* $P_(u,t) < P_(u,t-1)$ \
    #indent3 $S_t^"STOP" arrow.l 1$ \
    #indent3 $S_t^"START" arrow.l 0$ \
    #indent2 *else* \
    #indent3 $S_t^"STOP" arrow.l 0$ \
    #indent3 $S_t^"START" arrow.l 1$ \
    #indent2 *end if* \
    #indent *else* #h(1fr) // Final possibility: the unit is OFF. \
    #indent2 $S_(u,t)^"OFF" arrow.l 1$ \
    #indent2 $S_(u,t)^"STOP" arrow.l 0$ \
    #indent2 $S_(u,t)^"START" arrow.l 0$ \
    #indent2 $S_(t-1)^"ON_UP" arrow.l 0$ \
    #indent2 $S_(t-1)^"ON_DOWN" arrow.l 0$ \
    #indent2 $S_(t-1)^"ON_FLAT" arrow.l 0$ \
    #indent *end if* \
    *end for*
    #line(length: 100%)
  ],
  caption: [Initialization of the control and state variables]
)
