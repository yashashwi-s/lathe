#set document(a4: true, margin: 2.5cm) // Standard A4 margins to match typical article class output
#set text(lang: "en") // Set language for proper hyphenation and typography

// Custom commands for common mathematical terms
#let dmodel = $d_("model")$
#let dffn = $d_("ffn")$
#let dff = $d_("ff")$

We compute the matrix of outputs as:

#equation(label: "eq:attention")[
  #text("Attention")(Q, K, V) = #text("softmax")((Q K^T) / sqrt(d_k))V
]

Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.

#align(
  #text("MultiHead")(Q, K, V) &= #text("Concat")(#text("head")_1, ..., #text("head")_h)W^O,
  #text("where")~#text("head")_i &= #text("Attention")(Q W^Q_i, K W^K_i, V W^V_i),
)

Where the projections are parameter matrices $W^Q_i \in #bb(R)^{#dmodel \times d_k}$, $W^K_i \in #bb(R)^{#dmodel \times d_k}$, $W^V_i \in #bb(R)^{#dmodel \times d_v}$ and $W^O \in #bb(R)^{hd_v \times #dmodel}$.

In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.

#equation(label: "eq:ffn")[
  #text("FFN")(x) = max(0, x W_1 + b_1) W_2 + b_2
]

Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.

#align(
  PE_((pos,2i)) &= sin(pos / 10000^(2i/#dmodel)),
  PE_((pos,2i+1)) &= cos(pos / 10000^(2i/#dmodel)),
)
```