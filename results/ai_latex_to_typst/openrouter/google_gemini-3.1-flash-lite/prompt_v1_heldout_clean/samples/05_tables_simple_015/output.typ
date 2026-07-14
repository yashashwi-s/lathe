#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Simple Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.03910_table_3],
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    stroke: (x, y) => if y == 0 or y == 1 or y == 36 { (top: 0.5pt + black, bottom: 0.5pt + black) } else { none },
    align: (left, left, left, left, right, right, right),
    [Date], [Configuration], [Time], [Object], [$tau_0$ \ [ms]], [Seeing \ ["]], [FT],
    table.hline(),
    [2 Apr 2022], [A0-G1-J2-J3], [4:20:05], [$epsilon$ TrA], [3.88], [0.97], [1],
    [], [], [4:34:15], [X TrA], [3.89], [0.86], [0.9908],
    [], [], [4:56:25], [$eta$ Ara], [3.96], [0.86], [1],
    [3 Apr 2022], [A0-G1-J2-J3], [7:39:42], [$epsilon$ TrA], [4.78], [0.71], [1],
    [], [], [7:53:23], [X TrA], [4.41], [0.74], [0.8899],
    [], [], [8:19:07], [$eta$ Ara], [5.19], [0.62], [0.9909],
    [5 Apr 2022], [A0-G1-J2-J3], [6:14:54], [$beta$ TrA], [4.77], [0.66], [1],
    [], [], [6:31:07], [X TrA], [4.98], [0.63], [0.9083],
    [], [], [6:53:11], [$zeta$ Ara], [5.35], [0.52], [0.9847],
    [7 Apr 2022], [A0-G1-J2-J3], [4:49:29], [$epsilon$ TrA], [4.53], [0.87], [1],
    [], [], [5:00:47], [X TrA], [4.22], [0.93], [0.8909],
    [], [], [5:24:48], [$eta$ Ara], [5.41], [0.65], [1],
    [], [A0-G1-J2-J3], [8:34:25], [$beta$ TrA], [3.85], [0.82], [1],
    [], [], [8:46:51], [X TrA], [4.41], [0.67], [0.2752],
    [], [], [9:10:37], [$zeta$ Ara], [4.16], [0.71], [1],
    [8 Apr 2022], [A0-G1-J2-J3], [8:16:31], [$beta$ TrA], [5.85], [0.52], [1],
    [], [], [8:30:49], [X TrA], [5.51], [0.53], [0.9174],
    [], [], [8:57:36], [$zeta$ Ara], [4.79], [0.67], [1],
    [11 Apr 2022], [A0-G1-J2-K0], [7:12:22], [$beta$ TrA], [1.54], [1.03], [1],
    [], [], [7:26:23], [X TrA], [2.91], [0.88], [0.9083],
    [], [], [7:52:45], [$zeta$ Ara], [3.22], [1.01], [0.9083],
    [29 Apr 2022 $N$], [A0-B2-D0-C1], [4:06:29], [X TrA], [10.35], [0.28], [1],
    [], [], [4:30:20], [$zeta$ Ara], [10.35], [0.28], [0.9909],
    [], [], [6:08:57], [X TrA], [8.87], [0.41], [1],
    [], [], [6:32:41], [$zeta$ Ara], [9.30], [0.51], [1],
    [1 May 2022 $L$], [A0-B2-D0-C1], [8:48:52], [X TrA], [3.73], [0.69], [1],
    [], [], [9:12:28], [$zeta$ Ara], [3.37], [0.72], [1],
    [30 May 2022 $N$], [K0-G2-D0-J3], [2:51:17], [$beta$ TrA], [4.00], [0.70], [1],
    [], [], [3:02:13], [X TrA], [4.40], [0.62], [0.9909],
    [], [], [3:23:52], [$zeta$ Ara], [3.18], [0.63], [1],
    [], [], [4:34:25], [$beta$ TrA], [4.37], [0.59], [1],
    [], [], [4:57:49], [X TrA], [3.90], [0.59], [0.9091],
    [], [], [5:23:54], [$zeta$ Ara], [3.84], [0.49], [1],
    [5 Jul 2022], [A0-G2-J2-J3], [3:07:57], [$beta$ TrA], [5.49], [0.41], [1],
    [], [], [3:26:39], [X TrA], [5.14], [0.50], [0.9182],
    [], [], [3:48:57], [$zeta$ Ara], [4.96], [0.46], [1]
  )
)

#figure(
  caption: [Source table 2: 2512.00193_table_8],
  table(
    columns: (auto, auto),
    stroke: (x, y) => if y == 1 { (bottom: 0.5pt + black) } else { none },
    [*Benchmark*], [*Optimized for*],
    [Aider polyglot], [TRUE],
    [ANLI], [TRUE],
    [ARC AI2], [TRUE],
    [ARC-AGI], [TRUE],
    [Balrog], [FALSE],
    [BBH], [TRUE],
    [BoolQ], [TRUE],
    [CadEval], [FALSE],
    [CSQA2], [FALSE],
    [Cybench], [TRUE],
    [DeepResearch Bench], [FALSE],
    [Factorio learning environment], [FALSE],
    [Fiction.LiveBench], [FALSE],
    [FrontierMath-2025-02-28-Private], [TRUE],
    [GeoBench], [FALSE],
    [GPQA diamond], [TRUE],
    [GSM8K], [TRUE],
    [GSO-Bench], [FALSE],
    [HellaSwag], [TRUE],
    [LAMBADA], [TRUE],
    [Lech Mazur Writing], [FALSE],
    [LiveBench], [TRUE],
    [MATH level 5], [TRUE],
    [MCBench], [FALSE],
    [MMLU], [TRUE],
    [OpenBookQA], [TRUE],
    [OSUniverse], [FALSE],
    [OSWorld], [TRUE],
    [OTIS Mock AIME 2024-2025], [TRUE],
    [PIQA], [TRUE],
    [ScienceQA], [TRUE],
    [SimpleBench], [FALSE],
    [SuperGLUE], [TRUE],
    [SWE-Bench verified], [TRUE],
    [Terminal Bench], [TRUE],
    [The Agent Company], [FALSE],
    [TriviaQA], [TRUE],
    [VideoMME], [TRUE],
    [VPCT], [FALSE],
    [WeirdML], [FALSE],
    [Winogrande], [TRUE]
  )
)
