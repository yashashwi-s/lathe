#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

                  Most competitive neural sequence transduction models have an encoder-decoder structure. Here, the encoder maps an input sequence of symbol representations $(x_(1), . . ., x_(n))$ to a sequence of continuous representations $upright(bold(z)) =(z_(1), . . ., z_(n))$. Given $upright(bold(z)) $, the decoder then generates an output sequence $(y_(1),. . .,y_(m))$ of symbols one element at a time. At each step the model is auto-regressive, consuming the previously generated symbols as additional input when generating the next.

 The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder.

===== Encoder:
The encoder is composed of a stack of $N = 6 $ identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position-wise fully connected feed-forward network. We employ a residual connection around each of the two sub-layers, followed by layer normalization. That is, the output of each sub-layer is $upright(L a y e r N o r m)(x + upright(S u b l a y e r)(x))$, where $upright(S u b l a y e r)(x)$ is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension $d_("model")= 5 1 2 $.

