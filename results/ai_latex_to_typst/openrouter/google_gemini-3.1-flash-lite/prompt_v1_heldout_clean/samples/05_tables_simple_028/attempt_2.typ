#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

= Simple Tables

Source-backed grouped table sample

#section[Tables]

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.00750\_table\_6],
  table(
    columns: 11,
    stroke: none,
    table.hline(y: 0), table.hline(y: 1),
    table.cell(colspan: 11, align: center)[Inner zone],
    table.hline(y: 2), table.hline(y: 3),
    [Obs date], [$B$], [$N_e$], [$p_1$], [$p_2$], [$\gamma_(min)$], [$\gamma_(max)$], [$\gamma_(break)$], [$U_e$], [$U_B$], [$\eta = U_B/U_e$],
    [], [$10^(-2)$ G], [$cm^(-3)$], [], [], [$10^3$], [$10^6$], [$10^5$], [erg $cm^(-3)$], [erg $cm^(-3)$], [],
    table.hline(y: 4), table.hline(y: 5),
    [09-07-2017], [$5.10^(+1.92)_(-1.15)$], [$1.03^(+0.24)_(-0.14)$], [$2.51^(+0.01)_(-0.01)$], [$3.31^(+0.87)_(-0.25)$], [$3.66^(+0.52)_(-0.57)$], [$6.47^(+5.90)_(-2.62)$], [$6.88^(+3.52)_(-1.43)$], [$9.12 times 10^(-3)$], [$9.93 times 10^(-5)$], [$1.09 times 10^(-2)$],
    [07-08-2017], [$5.40^(+1.23)_(-0.80)$], [$0.17^(+0.05)_(-0.04)$], [$2.66^(+0.14)_(-0.10)$], [$3.26^(+0.74)_(-0.17)$], [$11.4^(+3.42)_(-2.24)$], [$5.67^(+3.87)_(-1.60)$], [$6.28^(+6.16)_(-1.76)$], [$3.91 times 10^(-3)$], [$1.14 times 10^(-4)$], [$2.92 times 10^(-2)$],
    [21-10-2017], [$2.38^(+0.70)_(-0.37)$], [$1.57^(+0.32)_(-0.35)$], [$2.30^(+0.08)_(-0.08)$], [$4.28^(+0.48)_(-0.44)$], [$1.88^(+0.56)_(-0.35)$], [$5.92^(+3.88)_(-2.43)$], [$9.90^(+1.20)_(-1.26)$], [$9.16 times 10^(-3)$], [$2.18 times 10^(-5)$], [$2.39 times 10^(-3)$],
    [07-12-2017], [$1.97^(+0.54)_(-0.39)$], [$1.33^(+0.27)_(-0.32)$], [$2.31^(+0.09)_(-0.08)$], [$4.10^(+0.58)_(-0.43)$], [$2.55^(+0.89)_(-0.55)$], [$8.17^(+6.63)_(-2.99)$], [$11.9^(+1.83)_(-2.21)$], [$1.01 times 10^(-2)$], [$1.65 times 10^(-5)$], [$1.64 times 10^(-3)$],
    [01-08-2018], [$3.87^(+0.82)_(-0.86)$], [$0.95^(+0.22)_(-0.23)$], [$2.36^(+0.09)_(-0.09)$], [$3.68^(+0.85)_(-0.95)$], [$2.92^(+0.76)_(-0.57)$], [$2.79^(+2.63)_(-0.99)$], [$9.08^(+1.79)_(-2.46)$], [$7.78 times 10^(-3)$], [$5.97 times 10^(-5)$], [$7.67 times 10^(-3)$],
    [11-09-2018], [$4.07^(+0.10)_(-0.07)$], [$5.42^(+1.16)_(-1.08)$], [$2.30^(+0.07)_(-0.06)$], [$4.56^(+0.33)_(-0.33)$], [$0.59^(+0.15)_(-0.10)$], [$4.41^(+2.07)_(-1.43)$], [$6.59^(+0.66)_(-0.43)$], [$1.75 times 10^(-2)$], [$1.12 times 10^(-5)$], [$6.41 times 10^(-4)$],
    [22-07-2020], [$3.52^(+0.67)_(-0.56)$], [$1.11^(+0.29)_(-0.18)$], [$2.46^(+0.10)_(-0.08)$], [$3.85^(+0.23)_(-0.17)$], [$2.53^(+0.48)_(-0.48)$], [$7.39^(+6.19)_(-3.25)$], [$6.67^(+0.85)_(-0.62)$], [$6.73 times 10^(-3)$], [$5.02 times 10^(-5)$], [$7.46 times 10^(-3)$],
    [28-07-2021], [$4.11^(+0.84)_(-0.72)$], [$1.04^(+0.26)_(-0.19)$], [$2.18^(+0.11)_(-0.12)$], [$3.55^(+0.19)_(-0.22)$], [$1.11^(+0.24)_(-0.18)$], [$2.52^(+0.10)_(-0.46)$], [$3.61^(+0.50)_(-0.64)$], [$4.09 times 10^(-3)$], [$6.63 times 10^(-5)$], [$1.56 times 10^(-2)$],
    [05-08-2021], [$2.15^(+0.36)_(-0.25)$], [$0.53^(+0.14)_(-0.10)$], [$2.08^(+0.13)_(-0.06)$], [$3.34^(+0.18)_(-0.19)$], [$2.76^(+0.64)_(-0.46)$], [$2.62^(+0.61)_(-0.37)$], [$3.85^(+0.81)_(-0.76)$], [$5.99 times 10^(-3)$], [$1.46 times 10^(-5)$], [$2.44 times 10^(-3)$],
    [05-08-2022], [$1.89^(+0.63)_(-0.42)$], [$0.25^(+0.08)_(-0.05)$], [$2.43^(+0.22)_(-0.14)$], [$3.92^(+0.45)_(-0.36)$], [$14.5^(+4.32)_(-4.21)$], [$5.46^(+7.03)_(-2.04)$], [$7.72^(+1.60)_(-1.78)$], [$8.65 times 10^(-3)$], [$1.39 times 10^(-5)$], [$1.61 times 10^(-3)$],
    table.hline(y: 14), table.hline(y: 15),
    table.cell(colspan: 11, align: center)[Host Galaxy],
    table.hline(y: 16), table.hline(y: 17),
    [], [nuFnu_p_host], [], [], [erg $cm^(-2) s^(-1)$], [], [], [-10.4], [], [], [],
    [], [nu_scale], [], [], [Hz], [], [], [$ -4.2 times 10^(-3)$], [], [], [],
    table.hline(y: 18), table.hline(y: 19)
  )
)

#figure(
  caption: [Source table 2: 2512.01786\_table\_4],
  table(
    columns: (4fr, 5fr, 3fr),
    stroke: 0.5pt,
    table.header([*Feature Name*], [*Explanation*], [*Category*]),
    [COUNT_WORD], [Number of words in the context.], [Text size],
    [COUNT_CHAR], [Number of characters in the context.], [Text size],
    [COUNT_SENTENCE], [Number of sentences in the context.], [Text size],
    [COUNT_PARAGRAPH], [Number of paragraphs in the context.], [Text size],
    [CHAR_COMPRESSION], [Ratio of characters in output to input context.], [Text size],
    [WORD_COMPRESSION], [Ratio of words in output to input context.], [Text size],
    [NUM_WORD_SENTENCE], [Average number of words per sentence.], [Text size],
    [NUM_CHAR_WORD], [Average number of characters per word.], [Text size],
    [DIFFICULT_WORD], [Number of difficult words (more than two syllables).], [Special words],
    [STOP_WORDS], [Number of stop words (e.g., “I”, “to”, “and”).], [Special words],
    [MODALITY], [Number of modality verbs (e.g., “can”, “should”).], [Special words],
    [NUMBER_COUNT], [Count of numbers (e.g., date, time, percent).], [Special words],
    [NAMED_ENTITY], [Count of named entities (person, org, date, etc.).], [Special words],
    [FACTUAL_DENSISTY], [Number of entities divided by context length.], [Special words],
    [NGRAM_COUNT], [Count of 3-grams in the context.], [Special words],
    [NEGATION_SENTENCE], [Count of sentences with negation words.], [Special words],
    [COUNT_QUESTION], [Number of questions in the context.], [Special words],
    [TOKEN_ENTROPY], [Shannon entropy on token distribution.], [Text complexity],
    [LEXICAL_DIVERSITY], [Unique words divided by total words.], [Text complexity],
    [READING_INDEX], [Flesch reading ease index.], [Text complexity],
    [NGRAM_REPETITION], [3-gram repetition ratio.], [Text complexity],
    [SENTENCE_SIMILARITY], [Avg. cosine similarity between sentence embeddings.], [Text complexity],
    [SYNTACTIC_AMBIGUITY], [Avg. ambiguous POS tags (IN, TO) per sentence.], [Text complexity],
    [SEMANTIC_AMBIGUITY], [Avg. WordNet senses per word.], [Text complexity],
    [COREFERENCE_CHAIN], [Avg. number of pronouns per sentence.], [Text complexity],
    [COREFERENCE_AMBIGUOUS], [Number of pronoun-ambiguous sentences.], [Text complexity],
    [SYNTACTIC_ANOMALY], [Number of syntactic anomaly sentences.], [Text complexity],
    [RHETORICAL_STRUCTURE], [Sentences with discourse markers/rhetorical structure.], [Text complexity],
    [POLARITY], [Emotional tone score of the context.], [Text complexity],
    [SUBJECTIVITY], [Degree of personal opinion or factuality.], [Text complexity],
    [PCA], [Top 10 principal components from text embeddings.], [Embedding],
    [Topic similarity], [Cosine similarity with predefined topic embeddings.], [Embedding]
  )
)
