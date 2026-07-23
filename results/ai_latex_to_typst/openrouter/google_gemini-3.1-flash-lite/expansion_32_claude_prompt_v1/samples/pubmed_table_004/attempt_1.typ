#set page(paper: "us-letter", margin: 1in)
#set text(font: "serif", size: 11pt)

#align(center)[
  #text(size: 1.4em, weight: "bold")[Clinical Table Sample 4] \
  Dataset-expansion sample
]

#v(1em)

#section("Patient Data")
The table below is a medical-literature table reproduced verbatim from a PubMed-derived dataset.

#v(1em)

#let table-data = (
  ("m1", "Dichlorodifluoromethane", "1.35", "1.50", "1.52", "m44", "p-Xylene", "23.54", "22.69", "22.8"),
  ("m2", "Carbon disulfide", "4.11", "2.71", "2.67", "m45", "m-Xylene", "23.54", "22.69", "22.6"),
  ("m3", "Allyl chloride", "4.11", "6.57", "6.57", "m46", "o-Xylenea", "25.16", "22.66", "22.5"),
  ("m4", "Methylene chloride", "4.40", "3.93", "4.12", "m47", "Styrene", "25.3", "23.09", "22.9"),
  ("m5", "1,1-Dichloroethene", "4.57", "6.75", "6.79", "m48", "Bromoformb", "26.23", "26.19", "26.2"),
  ("m6", "Acetone", "4.57", "3.66", "4.22", "m49", "Isopropylbenzene (Cumene)", "26.37", "27.00", "26.76"),
  ("m7", "trans-1,2-Dichloroethene", "4.57", "8.77", "8.76", "m50", "cis-1,4-Dichloro-2-butene", "27.12", "27.18", "27.39"),
  ("m8", "Acrylonitrile", "5.00", "4.52", "4.80", "m51", "Trichlorofluoromethanea", "2.42", "6.04", "5.75"),
  ("m9", "1,1-Dichloroethane", "6.14", "8.62", "8.16", "m52", "1,1,2,2-Tetrachloroethane", "27.29", "25.7", "25.79"),
  ("m10", "Vinyl acetate", "6.43", "11.47", "11.50", "m53", "Bromobenzene", "27.46", "26.85", "26.92"),
  ("m11", "2,2-Dichloropropane", "8.10", "12.42", "12.61", "m54", "1,2,3-Trichloropropanea", "27.55", "27.46", "26.61"),
  ("m12", "Chloromethane", "1.49", "-0.34", "-0.12", "m55", "n-Propylbenzene", "27.58", "27.92", "27.64"),
  ("m13", "cis-1,2-Dichloroethenea", "8.25", "9.82", "9.86", "m56", "2-Chlorotoluene", "28.19", "27.88", "27.96"),
  ("m14", "Propionitrile", "8.51", "5.61", "5.99", "m57", "trans-1,4-Dichloro-2-butene", "28.26", "26.64", "26.75"),
  ("m15", "Chloroform", "9.01", "7.78", "7.50", "m58", "1,3,5-Trimethylbenzene", "28.31", "26.62", "28.48"),
  ("m16", "Methacrylonitrile", "9.19", "8.47", "8.74", "m59", "4-Chlorotoluene", "28.33", "27.85", "27.94"),
  ("m17", "1,1,1-Trichloroethanea", "10.18", "13.58", "12.60", "m60", "Pentachloroethane", "29.41", "28.41", "28.17"),
  ("m18", "Carbon tetrachloride", "11.02", "11.75", "11.23", "m61", "1,2,4-Trimethylbenzenea", "29.47", "26.75", "26.61"),
  ("m19", "1,1-Dichloropropene", "11.50", "14.4", "14.29", "m62", "Acrolein", "3.19", "3.33", "3.44"),
  ("m20", "Benzenea", "1.56", "1.70", "1.84", "m63", "sec-Butylbenzene", "30.25", "31.85", "31.32"),
  ("m21", "Vinyl Chloride", "12.09", "11.39", "11.53", "m64", "tert-Butylbenzene", "30.59", "30.14", "29.86"),
  ("m22", "1,2-Dichloroethane", "14.03", "13.84", "13.67", "m65", "p-Isopropyltoluenea", "30.59", "31.10", "30.85"),
  ("m23", "Trichloroethene", "14.51", "15.14", "15.43", "m66", "1,3-Dichlorobenzene", "30.56", "31.78", "31.94"),
  ("m24", "1,2-Dichloropropane", "15.39", "16.45", "16.45", "m67", "1,4-Dichlorobenzene", "31.22", "32.65", "32.88"),
  ("m25", "Dibromomethane", "15.43", "12.66", "12.21", "m68", "Benzyl chloride", "32.00", "28.35", "28.52"),
  ("m26", "methacrylatea Methyl", "15.50", "15.79", "15.69", "m69", "n-Butylbenzene", "32.23", "32.68", "32.35"),
  ("m27", "1,4-Dioxane", "16.17", "15.46", "15.43", "m70", "1,2-Dichlorobenzene", "32.31", "32.00", "32.17"),
  ("m28", "2-Chloroethyl vinyl ether", "17.32", "15.02", "15.92", "m71", "1,2-Dibromo-3-chloropropanea", "35.30", "33.29", "33.39"),
  ("m29", "4-Methyl-2-pentanone", "17.47", "16.13", "16.81", "m72", "1,2,4-Trichlorobenzene", "38.19", "40.76", "4102"),
  ("m30", "trans-1,3-Dichloropropene", "2.19", "2.08", "1.94", "m73", "Iodomethane", "3.56", "6.13", "5.83"),
  ("m31", "Bromomethane", "18.29", "18.63", "18.53", "m74", "Hexachlorobutadieneb", "38.57", "-", "-"),
  ("m32", "Toluene", "19.38", "15.38", "15.90", "m75", "Naphthalenea", "39.05", "33.39", "33.04"),
  ("m33", "cis-1,3-Dichloropropene", "19.59", "19.34", "19.50", "m76", "1,2,3-Trichlorobenzene", "40.01", "23.49", "40.8"),
  ("m34", "methacrylatea Ethyl", "20.01", "24.52", "24.70", "m77", "1,4-Difluorobenzenea", "13.26", "13.68", "13.6"),
  ("m35", "2-Hexanone", "20.30", "21.03", "21.24", "m78", "Chlorobenzene-d5", "23.10", "23.49", "23.28"),
  ("m36", "Tetrachloroethene", "20.26", "19.88", "19.62", "m79", "1,4-Dichlorobenzene-d4", "31.16", "32.65", "32.88"),
  ("m37", "1,3-Dichloropropanea", "20.51", "16.58", "16.67", "m80", "4-Bromofluorobenzene", "27.83", "25.93", "26.08"),
  ("m38", "Dibromochloromethane", "21.19", "21.94", "21.62", "m81", "1,2-Dichlorobenzene-d4a", "32.30", "32.00", "32.11"),
  ("m39", "1,2-Dibromoethane", "21.52", "20.89", "20.21", "m82", "Dichloroethane-d4", "12.08", "8.62", "8.76"),
  ("m40", "Chloroethane", "2.21", "2.83", "3.03", "m83", "Acetonitrilea", "4.11", "3.23", "4.00"),
  ("m41", "Chlorobenzene", "23.17", "23.52", "23.61", "m84", "Toluene-d8", "18.27", "18.63", "18.53"),
  ("m42", "1,1,1,2-Tetrachloroethane", "23.36", "22.88", "22.81", "m85", "Fluorobenzene", "13.00", "14.04", "14.11"),
  ("m43", "Ethylbenzene", "23.38", "23.26", "23.06", "", "", "", "", "")
)

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
  stroke: 0.5pt,
  align: left + horizon,
  table.header(
    [*NO.*], [*name*], [*tR (min) Exp.*], [*tR MLR*], [*tR ANN*],
    [*NO.*], [*name*], [*tR (min) Exp.*], [*tR MLR*], [*tR ANN*]
  ),
  ..table-data.flatten()
)
