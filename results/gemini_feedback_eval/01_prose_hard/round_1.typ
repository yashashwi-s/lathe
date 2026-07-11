#set text(lang: "en")

#heading(level: 1, "Methodology") <sec:methodology>
As discussed in Section #link(<sec:methodology>), our approach leverages deep reinforcement learning #footnote[Specifically, Proximal Policy Optimization (PPO).] to align outputs with human preferences.

#heading(level: 2, "Data Processing")
The corpus is tokenized using #raw("Byte-Pair Encoding") (BPE) with a vocabulary size of 50,257.

#blockquote[
  "Alignment remains one of the most critical open problems in modern artificial intelligence, bridging the gap between raw computational capability and safe, intended utility."
]