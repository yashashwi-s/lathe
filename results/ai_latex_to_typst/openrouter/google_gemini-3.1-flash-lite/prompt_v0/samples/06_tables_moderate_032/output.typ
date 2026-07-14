#set page(margin: 1in)
#set text(font: "Linux Libertine", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Moderate Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  table(
    columns: (auto, auto, auto),
    stroke: none,
    table.header(
      [*Category*], [*Parameter*], [*Value*],
      table.hline(stroke: 0.8pt)
    ),
    [*Model Architecture*], [Base model], [bert-base-uncased],
    [], [Architecture], [BertForTokenClassification],
    [], [Hidden size], [768],
    [], [Intermediate size], [3072],
    [], [Hidden layers], [12],
    [], [Attention heads], [12],
    [], [Activation], [GELU],
    [], [Dropout], [0.1],
    [], [Tokenizer], [BertTokenizer (max length=512, padding/truncation)],
    [], [Number of labels], [5],
    [], [Label mapping], ["O": 0, "B-C": 1, "I-C": 2, "B-E": 3, "I-E": 4],
    table.hline(stroke: 0.5pt),
    [*Dataset*], [Name/source], [CausalPalUkr_Train_Test],
    [], [Task type], [Token Classification / NER],
    [], [Train/val/test split], [75-15],
    [], [Preprocessing], [Lowercase, truncate/ pad to 512, first subword labeling],
    table.hline(stroke: 0.5pt),
    [*Optimization*], [Optimizer], [AdamW (adamw_torch)],
    [], [Learning rate], [7e-5],
    [], [Scheduler], [Linear decay, 36 warmup steps],
    [], [Weight decay], [0.01],
    [], [Betas], [(0.9, 0.999)],
    [], [Epsilon], [1e-8],
    [], [Batch size / device], [16],
    [], [Gradient accumulation], [1],
    [], [Max grad norm], [1.0],
    [], [Epochs], [10],
    [], [FP16/BF16], [Disabled],
    table.hline(stroke: 0.5pt),
    [*Reproducibility*], [Seed], [42],
    [], [Data seed], [None],
    [], [Dataloader drop last], [False],
    [], [Dataloader workers], [0],
    [], [FP16 full eval], [False],
    table.hline(stroke: 0.5pt),
    [*Training Environment*], [Transformers], [4.50.3],
    [], [PyTorch], [2.6.0+cu124],
    [], [Datasets], [3.5.0],
    [], [Tokenizers], [0.21.1],
    [], [Hardware], [1x NVIDIA A100 40GB],
    table.hline(stroke: 0.5pt),
    [*Evaluation*], [Metrics], [Token-level Precision],
    [], [Validation freq], [after each epoch],
    table.hline(stroke: 0.5pt),
    [*HF model*], [pgarco/CausalPalUkr_token], [],
    table.hline(stroke: 0.8pt)
  ),
  caption: [Source table 1: 2512.03214_table_6]
)

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    [*Networks*], [*High-level*], [*Low-level*], [*Learning Rate*],
    table.hline(stroke: 0.5pt),
    [Actor], [128,128], [64,64], [3e-4],
    [Termination condition], [64,64], [\\], [3e-4],
    table.hline(stroke: 0.5pt),
    [Reward critic], [\\], [128,128], [1e-3],
    [Cost critic], [\\], [128,128], [1e-3],
    table.hline(stroke: 0.8pt),
    [*Parameters*], [*Value*], [*Parameters*], [*Value*],
    table.hline(stroke: 0.5pt),
    [GAE coefficient], [0.95], [Clip $epsilon$], [0.2],
    [Iterations], [20,000], [Episodes $E$], [10],
    [Batch size], [128], [Learning rate $alpha_lambda$], [0.01],
    [Tolerance $d$], [0.025], [], [],
    table.hline(stroke: 0.8pt)
  ),
  caption: [Source table 2: 2512.03059_table_4]
)
