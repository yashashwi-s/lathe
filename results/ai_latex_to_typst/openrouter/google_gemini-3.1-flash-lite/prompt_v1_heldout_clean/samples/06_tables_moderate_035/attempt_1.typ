#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Moderate Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.01260_table_2],
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    stroke: (x, y) => if y == 1 { (bottom: 0.5pt) } else { none },
    [ID], [Redshift], [Observer Frame \ Time Lag \ (days)], [JAV-ICCF \ Gap \ (days)], [Peak-Median \ Cut], [Peak Proportion], [Final Quality \ Rating],
    [DES J022514.39-044700.14], [1.928], [$217 plus.minus 50$], [37], [gold], [0.945], [gold],
    [DES J022327.85-040119.16], [1.922], [$396 plus.minus 33$], [50], [gold], [0.68], [gold],
    [DES J022537.03-050109.34], [1.936], [$294 plus.minus 17$], [13], [gold], [0.346], [bronze],
    [DES J033401.79-265054.28], [1.952], [$604 plus.minus 29$], [61], [bronze], [0.389], [bronze],
    [DES J025159.70-005159.89], [1.988], [$113 plus.minus 27$], [45], [gold], [0.822], [gold],
    [DES J032703.62-274425.27], [2.031], [$556 plus.minus 35$], [19], [gold], [0.39], [bronze],
    [DES J002959.21-434835.24], [2.041], [$442 plus.minus 18$], [2], [gold], [0.482], [silver],
    [DES J021921.81-043642.21], [2.092], [$379 plus.minus 29$], [8], [gold], [0.375], [bronze],
    [DES J021941.16-044100.36], [2.096], [$413 plus.minus 36$], [19], [gold], [0.357], [bronze],
    [DES J032829.96-274212.23], [2.15], [$480 plus.minus 27$], [34], [bronze], [0.355], [bronze],
    [DES J032939.97-284952.40], [2.188], [$237 plus.minus 31$], [11], [gold], [0.357], [bronze],
    [DES J022001.63-052216.92], [2.219], [$599 plus.minus 49$], [6], [gold], [0.63], [gold],
    [DES J003743.89-434715.68], [2.257], [$527 plus.minus 23$], [52], [silver], [0.529], [silver],
    [DES J033655.83-290218.23], [2.283], [$499 plus.minus 25$], [76], [gold], [0.364], [bronze],
    [DES J022410.96-050653.95], [2.315], [$552 plus.minus 42$], [3], [gold], [0.735], [gold],
    [DES J033843.76-294922.54], [2.328], [$307 plus.minus 12$], [3], [gold], [0.667], [gold],
    [DES J004056.56-431446.40], [2.384], [$295 plus.minus 37$], [5], [gold], [0.331], [bronze],
    [DES J025102.06-004142.78], [2.425], [$227 plus.minus 40$], [1], [gold], [0.578], [silver],
    [DES J022354.81-044814.94], [2.452], [$934 plus.minus 31$], [83], [gold], [0.51], [silver],
    [DES J024511.94-011317.50], [2.462], [$116 plus.minus 37$], [6], [bronze], [0.336], [bronze],
    [DES J025100.64+001707.38], [2.459], [$409 plus.minus 37$], [71], [bronze], [0.359], [bronze],
    [DES J032640.93-283206.80], [2.492], [$507 plus.minus 15$], [41], [gold], [0.484], [silver],
    [DES J003957.42-434107.92], [2.5], [$512 plus.minus 17$], [19], [gold], [0.384], [bronze],
    [DES J022259.87-063326.65], [2.563], [$325 plus.minus 23$], [18], [gold], [0.435], [bronze],
    [DES J003352.72-425452.55], [2.593], [$386 plus.minus 14$], [65], [bronze], [0.409], [bronze],
    [DES J022330.15-043004.09], [2.677], [$331 plus.minus 20$], [53], [gold], [0.349], [bronze],
    [DES J022620.86-045946.48], [2.745], [$378 plus.minus 21$], [6], [gold], [0.425], [bronze],
    [DES J024514.93-004101.83], [2.773], [$260 plus.minus 31$], [25], [gold], [0.351], [bronze],
    [DES J025105.13-001732.01], [3.451], [$307 plus.minus 24$], [2], [gold], [0.537], [silver]
  )
)

#figure(
  caption: [Source table 2: 2512.02315_table_1],
  table(
    columns: (auto, auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 1 or y == 35 { (bottom: 0.5pt) } else { none },
    [Assay], [Type], [Similarity to train], [Closest protein],
    [AMFR_HUMAN_Tsuboyama_2023_4G3O], [Stability], [23%], [CUE1_YEAST],
    [RCD1_ARATH_Tsuboyama_2023_5OAO], [Stability], [20%], [NUSG_MYCTU],
    [SR43C_ARATH_Tsuboyama_2023_2N88], [Stability], [39%], [CBX4_HUMAN],
    [FECA_ECOLI_Tsuboyama_2023_2D1U], [Stability], [20%], [RPC1_BP434],
    [PKN1_HUMAN_Tsuboyama_2023_1URF], [Stability], [21%], [DN7A_SACS2],
    [CSN4_MOUSE_Tsuboyama_2023_1UFM], [Stability], [20%], [UBE4B_HUMAN],
    [SPA_STAAU_Tsuboyama_2023_1LP1], [Stability], [22%], [HECD1_HUMAN],
    [NKX31_HUMAN_Tsuboyama_2023_2L9R], [Stability], [32%], [PITX2_HUMAN],
    [EPHB2_HUMAN_Tsuboyama_2023_1F0M], [Stability], [25%], [PR40A_HUMAN],
    [SQSTM_MOUSE_Tsuboyama_2023_2RRU], [Stability], [29%], [OTU7A_HUMAN],
    [MAFG_MOUSE_Tsuboyama_2023_1K1V], [Stability], [24%], [RPB1_HUMAN],
    [SCIN_STAAR_Tsuboyama_2023_2QFF], [Stability], [23%], [HVP_LAMBD],
    [DNJA1_HUMAN_Tsuboyama_2023_2LO1], [Stability], [23%], [HECD1_HUMAN],
    [VRPI_BPT7_Tsuboyama_2023_2WNM], [Stability], [19%], [MYO3_YEAST],
    [ESTA_BACSU_Nutschel_2020], [Stability], [15%], [CALM1_HUMAN],
    [CASP3_HUMAN_Roychowdhury_2020], [Enz. Activity], [48%], [CASP7_HUMAN],
    [BLAT_ECOLX_Deng_2012], [Enz. Activity], [18%], [CD19_HUMAN],
    [BLAT_ECOLX_Jacquier_2013], [Enz. Activity], [18%], [CD19_HUMAN],
    [BLAT_ECOLX_Stiffler_2015], [Enz. Activity], [18%], [CD19_HUMAN],
    [BLAT_ECOLX_Firnberg_2014], [Enz. Activity], [18%], [CD19_HUMAN],
    [VKOR1_HUMAN_Chiasson_2020_activity], [Enz. Activity], [13%], [RPC1_BP434],
    [VKOR1_HUMAN_Chiasson_2020_abundance], [Abundance], [13%], [RPC1_BP434],
    [Q8WTC7_9CNID_Somermeyer_2022], [Fluoresence], [18%], [Q6WV13_9MAXI],
    [D7PM05_CLYGR_Somermeyer_2022], [Fluoresence], [19%], [MTH3_HAEAE],
    [GFP_AEQVI_Sarkisyan_2016], [Fluoresence], [18%], [Q6WV13_9MAXI],
    [DLG4_RAT_McLaughlin_2012], [Binding], [19%], [PSAE_SYNP2],
    [RL40A_YEAST_Roscoe_2013], [Binding], [20%], [SPG2_STRSG],
    [GRB2_HUMAN_Faure_2021], [Binding], [27%], [SRBS1_HUMAN],
    [DYR_ECOLI_Thompson_2019], [Enz. Activity], [15%], [NUD15_HUMAN],
    [DLG4_HUMAN_Faure_2021], [Binding], [25%], [EPHB2_HUMAN],
    [RL40A_YEAST_Mavor_2016], [Binding], [20%], [SPG2_STRSG],
    [DYR_ECOLI_Nguyen_2023], [Enz. Activity], [15%], [NUD15_HUMAN],
    [RL40A_YEAST_Roscoe_2014], [Binding], [20%], [SPG2_STRSG]
  )
)
