#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Moderate Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.05256\_table\_2],
  table(
    columns: (auto, auto, auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 1 or y == 7 { (bottom: 0.5pt + black) } else { none },
    align: (left, left, left, center, center),
    [*Clinical Case*], [*ICD Code*], [*Text Reference*], [*Age*], [*Gender*],
    [A], [R52, K08.89], [pain, toothache], [56], [female],
    [B], [K08.109], [edentulism], [54], [female],
    [C], [E11.9 M79.81 \ R05 T14.8], [abdominal wall \ hematoma, cough, DM \ ID, hematoma, right \ anterior rectal hematoma], [61], [male],
    [D], [B00.9 B99.9 \ C15.9 F17.210 \ K22.2 R13.10 \ R50.9 R60.9 \ R63.4], [dysphagia, edema, \ esophageal carcinoma, \ fever, herpes simplex, \ infection, partial narrowing \ of the esophageal \ lumen, smoker, weightloss], [67], [male],
    [E], [B99.9 C81.90 \ G93.40 K72.00 \ K72.90 K92.1 \ K92.2 R58 \ R69 R74.0], [acute liver failure, \ digestive bleeding, disease, \ elevated transaminases, \ encephalopathy, hemorrhage, \ hepatic encephalopathy, \ Hodgkin's disease, infection, \ liver failure, manes], [16], [male],
    [F], [I10 K42.9 \ K56.60 K92.2 \ N80.5 R10.32 \ R10.814 \ R19.8 R58], [AHT, colon endometriosis, \ colon hemorrhage, \ hemorrhage, pain in FII, \ pain on deep palpation \ in FII, rectal urgency, \ sigma level stricture \ imaging, umbilical hernia], [42], [female],
  )
)

#figure(
  caption: [Source table 2: 2512.01260\_table\_3],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 30 { (bottom: 0.5pt + black) } else { none },
    align: (left, center, center, center, center, center),
    [ID], [Final Quality \ Rating], [Rest-Frame Lag \ (days)], [Luminosity \ ($lambda L_("1350Å") "erg" s^(-1)$)], [Linewidth \ (km $s^(-1)$)], [BH Mass \ ($10^8 M_sun$)],
    [DES J022514.39-044700.14], [gold], [$74 plus.minus 17$], [$1.82 times 10^(46)$], [$3610 plus.minus 31$], [$8.4 plus.minus 2.7$],
    [DES J022327.85-040119.16], [gold], [$136 plus.minus 11$], [$3.54 times 10^(45)$], [$3808 plus.minus 171$], [$17.2 plus.minus 4.3$],
    [DES J022537.03-050109.34], [bronze], [$100 plus.minus 6$], [$6.95 times 10^(45)$], [$4190 plus.minus 34$], [$15.3 plus.minus 3.6$],
    [DES J033401.79-265054.28], [bronze], [$205 plus.minus 10$], [$9.74 times 10^(45)$], [$3605 plus.minus 77$], [$23.3 plus.minus 5.5$],
    [DES J025159.70-005159.89], [gold], [$38 plus.minus 9$], [$1.78 times 10^(45)$], [$4239 plus.minus 135$], [$6 plus.minus 2$],
    [DES J032703.62-274425.27], [bronze], [$183 plus.minus 12$], [$1.27 times 10^(46)$], [$4398 plus.minus 43$], [$30.9 plus.minus 7.4$],
    [DES J002959.21-434835.24], [silver], [$145 plus.minus 6$], [$6.11 times 10^(46)$], [$3595 plus.minus 11$], [$16.4 plus.minus 3.8$],
    [DES J021921.81-043642.21], [bronze], [$123 plus.minus 9$], [$1.1 times 10^(46)$], [$3519 plus.minus 125$], [$13.3 plus.minus 3.3$],
    [DES J021941.16-044100.36], [bronze], [$133 plus.minus 12$], [$4.69 times 10^(45)$], [$4146 plus.minus 83$], [$20 plus.minus 5$],
    [DES J032829.96-274212.23], [bronze], [$152 plus.minus 9$], [$8.88 times 10^(45)$], [$2791 plus.minus 59$], [$10.3 plus.minus 2.5$],
    [DES J032939.97-284952.40], [bronze], [$74 plus.minus 10$], [$7.7 times 10^(45)$], [$3929 plus.minus 138$], [$10 plus.minus 2.7$],
    [DES J022001.63-052216.92], [gold], [$186 plus.minus 15$], [$7.54 times 10^(45)$], [$3548 plus.minus 64$], [$20.4 plus.minus 5$],
    [DES J003743.89-434715.68], [silver], [$162 plus.minus 7$], [$1.39 times 10^(46)$], [$3672 plus.minus 60$], [$19.1 plus.minus 4.5$],
    [DES J033655.83-290218.23], [bronze], [$152 plus.minus 8$], [$1.6 times 10^(46)$], [$4228 plus.minus 77$], [$23.7 plus.minus 5.6$],
    [DES J022410.96-050653.95], [gold], [$167 plus.minus 13$], [$6.16 times 10^(45)$], [$3647 plus.minus 57$], [$19.4 plus.minus 4.7$],
    [DES J033843.76-294922.54], [gold], [$92 plus.minus 4$], [$5.61 times 10^(45)$], [$2781 plus.minus 198$], [$6.2 plus.minus 1.6$],
    [DES J004056.56-431446.40], [bronze], [$87 plus.minus 11$], [$1.61 times 10^(46)$], [$3655 plus.minus 44$], [$10.1 plus.minus 2.7$],
    [DES J025102.06-004142.78], [silver], [$66 plus.minus 12$], [$2.27 times 10^(45)$], [$3317 plus.minus 172$], [$6.3 plus.minus 1.9$],
    [DES J022354.81-044814.94], [silver], [$271 plus.minus 9$], [$3.82 times 10^(46)$], [$4134 plus.minus 23$], [$40.4 plus.minus 9.4$],
    [DES J024511.94-011317.50], [bronze], [$34 plus.minus 11$], [$7.83 times 10^(45)$], [$4021 plus.minus 90$], [$4.8 plus.minus 1.9$],
    [DES J025100.64+001707.38], [bronze], [$118 plus.minus 11$], [$7.59 times 10^(45)$], [---], [---],
    [DES J032640.93-283206.80], [silver], [$145 plus.minus 4$], [$7.56 times 10^(45)$], [$4328 plus.minus 58$], [$23.7 plus.minus 5.5$],
    [DES J003957.42-434107.92], [bronze], [$146 plus.minus 5$], [$9.86 times 10^(45)$], [$3636 plus.minus 57$], [$16.8 plus.minus 3.9$],
    [DES J022259.87-063326.65], [bronze], [$91 plus.minus 6$], [$8.99 times 10^(45)$], [$4352 plus.minus 95$], [$15 plus.minus 3.6$],
    [DES J003352.72-425452.55], [bronze], [$107 plus.minus 4$], [$3.44 times 10^(46)$], [$3876 plus.minus 19$], [$14 plus.minus 3.3$],
    [DES J022330.15-043004.09], [bronze], [$90 plus.minus 5$], [$4.21 times 10^(45)$], [---], [---],
    [DES J022620.86-045946.48], [bronze], [$101 plus.minus 6$], [$4.43 times 10^(45)$], [$3650 plus.minus 104$], [$11.7 plus.minus 2.8$],
    [DES J024514.93-004101.83], [bronze], [$69 plus.minus 8$], [$5.92 times 10^(45)$], [---], [---],
    [DES J025105.13-001732.01], [silver], [$69 plus.minus 5$], [$1.35 times 10^(46)$], [---], [---],
  )
)
