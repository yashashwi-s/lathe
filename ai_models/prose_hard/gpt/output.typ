#set page(paper: "us-letter", margin: 1in)
#set text(size: 10pt, font: "New Computer Modern")
#set par(justify: true)
#set heading(numbering: "1.")

= Methodology [sec:methodology](sec:methodology)

As discussed in Section~@sec:methodology, our approach leverages deep reinforcement learning#footnote[Specifically, Proximal Policy Optimization (PPO).] to align outputs with human preferences.

== Data Processing

The corpus is tokenized using `Byte-Pair Encoding` (BPE) with a vocabulary size of 50,257.

> "Alignment remains one of the most critical open problems in modern artificial intelligence, bridging the gap between raw computational capability and safe, intended utility."
