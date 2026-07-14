#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#align(center)[
  #text(size: 17pt, weight: "bold")[Simple Tables]
  #v(0.5em)
  #text(size: 12pt)[Source-backed grouped table sample]
  #v(1em)
]

= Tables

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#let table-data-1 = (
  (strong[Index], strong[Model Name], strong[Model Size (MB)], strong[Dataset]),
  (strong[1], [twmkn9/albert-base-v2-squad2], [12], [SQuAD v2]),
  (strong[2], [valhalla/bart-large-finetuned-squadv1], [388], [SQuAD v1]),
  (strong[3], [deepset/bert-base-cased-squad2], [104], [SQuAD v2]),
  (strong[4], [google/bigbird-roberta-base], [122], [Books, CC-News, Stories and Wikipedia.]),
  (strong[5], [google/bigbird-pegasus-large-arxiv], [551], [Arxiv dataset]),
  (strong[6], [dmis-lab/biobert-v1.1], [104], [NA]),
  (strong[7], [deepset/roberta-base-squad2], [119], [SQuAD v2]),
  (strong[8], [Splend1dchan/canine-c-squad], [126], [NA]),
  (strong[9], [YituTech/conv-bert-base], [101], [NA]),
  (strong[10], [Palak/microsoft\_deberta-large\_squad], [387], [SQuAD v1]),
  (strong[11], [microsoft/deberta-v2-xlarge], [844], [NA]),
  (strong[12], [distilbert-base-uncased], [64], [BookCorpus and English Wikipedia]),
  (strong[13], [bhadresh-savani/electra-base-squad2], [104], [SQuAD v2]),
  (strong[14], [nghuyong/ernie-1.0-base-zh], [96], [Chinese]),
  (strong[15], [xlm-mlm-en-2048], [637], [Masked language modeling]),
  (strong[16], [google/fnet-base], [80], [Colossal Clean Crawled Corpus (C4)]),
  (strong[17], [funnel-transformer/small], [125], [BookCorpus, English Wikipedia, Clue Web, GigaWord, and Common Crawl]),
  (strong[18], [EleutherAI/gpt-neo-1.3B], [1255], [Pile]),
  (strong[19], [hf-internal-testing/tiny-random-gptj], [1], [NA]),
  (strong[20], [gpt2], [119], [WebText]),
  (strong[21], [kssteven/ibert-roberta-base], [119], [NA]),
  (strong[22], [allenai/led-base-16384], [155], [NA]),
  (strong[23], [allenai/longformer-large-4096-finetuned-triviaqa], [415], [NA]),
  (strong[24], [facebook/mbart-large-cc25], [583], [Multilingual mbart model]),
  (strong[25], [mnaylor/mega-base-wikitext], [8], [wikitext-103]),
  (strong[26], [csarron/mobilebert-uncased-squad-v2], [24], [SQuAD v2]),
  (strong[27], [microsoft/mpnet-base], [105], [NA]),
  (strong[28], [google/mt5-small], [165], [101 languages]),
  (strong[29], [RUCAIBox/mvp], [388], [NA]),
  (strong[30], [sijunhe/nezha-cn-base], [98], [Chinese]),
  (strong[31], [uw-madison/nystromformer-512], [104], [BookCorpus and English Wikipedia]),
  (strong[32], [facebook/opt-350m], [316], [BookCorpus, CC-Stories, The Pile, Pushshift.io, and CCNewsV2]),
  (strong[33], [bert-base-uncased], [105], [BookCorpus and English Wikipedia]),
  (strong[34], [google/rembert], [550], [Multilingual Wikipedia data over 110 languages.]),
  (strong[35], [roberta-base], [119], [BookCorpus, English Wikipedia, CC-News, OpenWebText, and Stories]),
  (strong[36], [andreasmadsen/efficient\_mlm\_m0.40], [339], [NA]),
  (strong[37], [ArthurZ/dummy-rocbert-qa], [112], [NA]),
  (strong[38], [tau/splinter-base], [103], [BookCorpus and English Wikipedia]),
  (strong[39], [squeezebert/squeezebert-uncased], [49], [BookCorpus and English Wikipedia]),
  (strong[40], [t5-small], [58], [Colossal Clean Crawled Corpus (C4)]),
  (strong[41], [xlm-mlm-en-2048], [637], [Masked language modeling]),
  (strong[42], [xlnet-base-cased], [112], [XLNet model pre-trained on English language]),
  (strong[43], [uw-madison/yoso-4096], [121], [Masked language modeling]),
  (strong[44], [SRDdev/QABERT-small], [64], [30k samples from the Stanford Question Answering Dataset]),
  (strong[45], [bert-large-uncased-whole-word-masking-finetuned-squad], [320], [BookCorpus and English Wikipedia]),
  (strong[46], [facebook/bart-large-cnn], [388], [CNN Daily Mail]),
  (strong[47], [ahotrod/electra\_large\_discriminator\_squad2\_512], [319], [SQuAD v2]),
)

#figure(
  caption: [Source table 1: 2512.00323\_table\_8],
  block(
    width: 100%,
    table(
      columns: (auto, auto, auto, auto),
      align: left,
      stroke: 0.5pt,
      ..table-data-1.flatten()
    )
  )
)

#figure(
  caption: [Source table 2: 2512.00323\_table\_10],
  block(
    width: 100%,
    table(
      columns: (auto, auto, auto, auto),
      align: left,
      stroke: 0.5pt,
      ..table-data-1.flatten()
    )
  )
)
