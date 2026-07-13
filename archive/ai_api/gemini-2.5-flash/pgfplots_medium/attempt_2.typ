#set page(
  width: 612pt,
  height: 792pt,
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
  footer: [
    #h(1fr) #text(10pt, "1") #h(1fr)
  ],
)

#import "@preview/plot:1.0.1" as plot // Changed package version to 1.0.1 to attempt to resolve "package not found" error.

#plot.plot(
  x-label: "Time (s)",
  y-label: "Voltage (V)",
  legend: plot.legend(pos: top + left),
  plot.line(
    ((0,0), (1,2.1), (2,3.5), (3,4.2), (4,4.8)),
    stroke: red,
    marker: "square",
    legend: "Experimental",
  ),
)