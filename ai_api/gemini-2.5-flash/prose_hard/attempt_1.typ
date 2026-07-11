#set page(
  // Typst's default page settings are similar to LaTeX's article class.
  // Margins are typically 2cm on all sides by default.
  // The page number is automatically placed at the bottom center.
)

#set text(lang: "en")

= Methodology <sec:methodology>
As discussed in Section @sec:methodology, our approach leverages deep reinforcement learning#footnote[Specifically, Proximal Policy Optimization (PPO).] to align outputs with human preferences.

== Data Processing
The corpus is tokenized using `Byte-Pair Encoding` (BPE) with a vocabulary size of 50,257.

#blockquote[
  "Alignment remains one of the most critical open problems in modern artificial intelligence, bridging the gap between raw computational capability and safe, intended utility."
]