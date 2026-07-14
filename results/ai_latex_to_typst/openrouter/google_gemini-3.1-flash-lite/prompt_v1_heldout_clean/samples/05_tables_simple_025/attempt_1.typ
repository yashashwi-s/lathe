#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Simple Tables] \
  Source-backed grouped table sample \
  #v(1em)
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  table(
    columns: (auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 36 { (top: 0.5pt, bottom: 0.5pt) } else { none },
    align: (left, left, left),
    [#], [Word type], [$f$],
    [1.], [_dat_ (‘that’)], [1999],
    [2.], [_te_ (‘at’, ‘to’, #smallcaps[comp])], [1779],
    [3.], [_er_ (‘there’)], [1370],
    [4.], [_niet_ (‘not’)], [969],
    [5.], [_ik_ (‘I’)], [729],
    [6.], [_hebben_ (‘have’)], [599],
    [7.], [_blijkt_ (‘turns out’)], [460],
    [8.], [_om_ (‘to’)], [434],
    [9.], [_alle_ (‘all’)], [409],
    [10.], [_zijn_ (‘are’, ‘be’, ‘his’)], [386],
    [11.], [_vergeten_ (‘forgotten’)], [385],
    [12.], [_elk_ (‘every’, #smallcaps[neut])], [330],
    [13.], [_de_ (‘the’, #smallcaps[masc/fem/pl])], [324],
    [14.], [_ieder_ (‘every’, #smallcaps[neut])], [317],
    [15.], [_iedere_ (‘every’, #smallcaps[masc/fem])], [317],
    [16.], [_door_ (‘by’)], [315],
    [17.], [_geen_ (‘no’)], [294],
    [18.], [_aan_ (‘to’, #smallcaps[prep])], [287],
    [19.], [_veel_ (‘a lot of’)], [281],
    [20.], [_elke_ (‘every’, #smallcaps[masc/fem])], [280],
    [21.], [_hier_ (‘here’)], [280],
    [22.], [_u_ (‘you’, #smallcaps[form])], [272],
    [23.], [_daar_ (‘there’)], [269],
    [24.], [_op_ (‘on’)], [268],
    [25.], [_weinig_ (‘a few’)], [268],
    [26.], [_massa's_ (‘masses’)], [262],
    [27.], [_werkt_ (‘works’)], [255],
    [28.], [_deze_ (‘this’, #smallcaps[masc/fem])], [253],
    [29.], [_worden_ (‘become’)], [240],
    [30.], [_jij_ (‘you’, #smallcaps[inform])], [238],
    [31.], [_je_ (‘you’, #smallcaps[inform])], [226],
    [32.], [_wordt_ (‘becomes’)], [224],
    [33.], [_waar_ (‘where’)], [216],
    [34.], [_een_ (‘a’, ‘one’)], [213],
    [35.], [_is_ (‘is’)], [210],
  ),
  caption: [Source table 1: 2512.02195_table_7]
)

#figure(
  table(
    columns: (auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 36 { (top: 0.5pt, bottom: 0.5pt) } else { none },
    align: (left, left, left),
    [#], [Word type], [$f$],
    [1.], [_dat_ (‘that’)], [1937],
    [2.], [_te_ (‘at’, ‘to’, #smallcaps[comp])], [1829],
    [3.], [_er_ (‘there’)], [1353],
    [4.], [_niet_ (‘not’)], [929],
    [5.], [_ik_ (‘I’)], [714],
    [6.], [_hebben_ (‘have’)], [570],
    [7.], [_om_ (‘to’)], [448],
    [8.], [_blijkt_ (‘turns out’)], [422],
    [9.], [_zijn_ (‘are’, ‘be’, ‘his’)], [396],
    [10.], [_vergeten_ (‘forgotten’)], [389],
    [11.], [_alle_ (‘all’)], [354],
    [12.], [_de_ (‘the’, #smallcaps[masc/fem/pl])], [330],
    [13.], [_geen_ (‘no’)], [330],
    [14.], [_ieder_ (‘every’, #smallcaps[neut])], [315],
    [15.], [_door_ (‘by’)], [304],
    [16.], [_elke_ (‘every’, #smallcaps[masc/fem])], [301],
    [17.], [_u_ (‘you’, #smallcaps[form])], [294],
    [18.], [_elk_ (‘every’, #smallcaps[neut])], [293],
    [19.], [_aan_ (‘to’, #smallcaps[prep])], [278],
    [20.], [_hier_ (‘here’)], [276],
    [21.], [_jij_ (‘you’, #smallcaps[inform])], [272],
    [22.], [_iedere_ (‘every’, #smallcaps[masc/fem])], [268],
    [23.], [_daar_ (‘there’)], [267],
    [24.], [_op_ (‘on’)], [259],
    [25.], [_veel_ (‘a lot of’)], [258],
    [26.], [_weinig_ (‘a few’)], [250],
    [27.], [_je_ (‘you’, #smallcaps[inform])], [249],
    [28.], [_massa's_ (‘masses’)], [249],
    [29.], [_deze_ (‘this’, #smallcaps[masc/fem])], [238],
    [30.], [_een_ (‘a’, ‘one’)], [236],
    [31.], [_worden_ (‘become’)], [233],
    [32.], [_werkt_ (‘works’)], [221],
    [33.], [_wordt_ (‘becomes’)], [209],
    [34.], [_waar_ (‘where’)], [207],
    [35.], [_is_ (‘is’)], [206],
  ),
  caption: [Source table 2: 2512.02195_table_9]
)
