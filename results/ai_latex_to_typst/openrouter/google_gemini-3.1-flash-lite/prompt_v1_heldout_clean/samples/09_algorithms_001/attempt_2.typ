#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 1] \
  Source-backed Image2Struct algorithm sample
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  caption: [Source-backed algorithmic procedure],
  block[
    #set par(leading: 0.8em)
    #let indent = h(2em)
    #let comment(c) = h(1fr) + text(fill: gray)[// #c]

    #text(weight: "bold")[for] $t in {-1, dots, -T^"traceback"}$ #comment("Initialization of " + $delta_t^"turned_on"$ + " and " + $delta_t^"turned_off"$) \
    #indent $delta_t^"turned_on" arrow.l 0$ \
    #indent $delta_t^"turned_off" arrow.l 0$ \
    #indent #text(weight: "bold")[if] $S_(u,t)^"STOP" - S_(t-1)^"STOP" = 1$ #comment("Replace by " + $S_(u,t)^"OFF" - S_(t-1)^"OFF" = 1$ + " if STOP is not defined.") \
    #indent #indent $delta_t^"turned_off" arrow.l 1$ \
    #indent #text(weight: "bold")[else if] $S_(u,t)^"START" - S_(t-1)^"START" = 1$ #comment("Replace by " + $S_(u,t)^"OFF" - S_(t-1)^"OFF" = -1$ + " if START is not defined.") \
    #indent #indent $delta_t^"turned_on" arrow.l 1$ \
    #indent #text(weight: "bold")[end if] \
    #text(weight: "bold")[end for] \

    #text(weight: "bold")[for] $t in {-1, dots, -T^"traceback"}$ #comment("Initialization of " + $delta_t^"stable"$, $delta_t^"entered_up"$ + " and " + $delta_t^"entered_down"$) \
    #indent $delta_t^"stable" arrow.l 0$ \
    #indent $delta_t^"entered_up" arrow.l 0$ \
    #indent $delta_t^"entered_down" arrow.l 0$ \
    #indent #text(weight: "bold")[if] $S_(u,t)^"STOP" - S_(t-1)^"STOP" = 1$ \
    #indent #indent $delta_t^"stable" arrow.l 1$ \
    #indent #text(weight: "bold")[else if] $S_(u,t)^"ON_UP" - S_(t-1)^"ON_UP" = 1$ \
    #indent #indent $delta_t^"entered_up" arrow.l 1$ \
    #indent #text(weight: "bold")[else if] $S_(u,t)^"ON_UP" - S_(t-1)^"ON_UP" = 1$ \
    #indent #indent $delta_t^"entered_down" arrow.l 1$ \
    #indent #text(weight: "bold")[end if] \
    #text(weight: "bold")[end for] \

    #text(weight: "bold")[for] $t in {-1, dots, -T^"traceback"}$ #comment("Initialization of " + $delta_t^"stable"$, $delta_t^"entered_up"$ + " and " + $delta_t^"entered_down"$) \
    #indent $delta_t^"stable" arrow.l 0$ \
    #indent $delta_t^"entered_up" arrow.l 0$ \
    #indent $delta_t^"entered_down" arrow.l 0$ \
    #indent #text(weight: "bold")[if] $S_(u,t)^"ON_FLAT" - S_(t-1)^"ON_FLAT" = 1$ \
    #indent #indent $delta_t^"stable" arrow.l 1$ \
    #indent #text(weight: "bold")[else if] $S_(u,t)^"ON_UP" - S_(t-1)^"ON_UP" = 1$ \
    #indent #indent $delta_t^"entered_up" arrow.l 1$ \
    #indent #text(weight: "bold")[else if] $S_(u,t)^"ON_DOWN" - S_(t-1)^"ON_DOWN" = 1$ \
    #indent #indent $delta_t^"entered_down" arrow.l 1$ \
    #indent #text(weight: "bold")[end if] \
    #text(weight: "bold")[end for] \

    #text(weight: "bold")[for] $t in {-1, dots, -T^"traceback"}$ #comment("Initialization of " + $delta_t^"flat,down,stop"$ + " or " + $delta_t^"down_to_stop"$) \
    #indent $delta_t^"flat,down,stop" arrow.l floor (S_(u,t)^"STOP" + S_(t-1)^"ON_DOWN" + S_(t-2)^"ON_FLAT") / 3 floor$ \
    #indent $delta_t^"down_to_stop" arrow.l 0$ \
    #indent #text(weight: "bold")[if] $S_(u,t)^"STOP" - S_(t-1)^"ON_DOWN" = 0$ \
    #indent #indent $delta_t^"down_to_stop" arrow.l 1$ \
    #indent #text(weight: "bold")[end if] \
    #text(weight: "bold")[end for] \

    $U_(-1) = S_(-1)^"ON_UP" times S_(-2)^"ON_UP" times (P_(u,t_(-1)) - P_(u,t_(-2)))$ #comment("Initial condition on " + $U_t$) \
    $D_(-1) = S_(-1)^"ON_DOWN" times S_(-2)^"ON_DOWN" times (P_(u,t_(-1)) - P_(u,t_(-2)))$ #comment("Initial condition on " + $D_t$)
  ]
)
