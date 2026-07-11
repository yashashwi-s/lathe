#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
Most competitive neural sequence transduction models have an
encoder-decoder structure. Here, the encoder maps an input sequence of
symbol representations #mi(`(x_1, ..., x_n)`) to a sequence of
continuous representations #mi(`\mathbf{z} = (z_1, ..., z_n)`). Given
#mi(`\mathbf{z}`), the decoder then generates an output sequence
#mi(`(y_1,...,y_m)`) of symbols one element at a time. At each step the
model is auto-regressive, consuming the previously generated symbols as
additional input when generating the next.

The Transformer follows this overall architecture using stacked
self-attention and point-wise, fully connected layers for both the
encoder and decoder.

==== Encoder:
<encoder>
The encoder is composed of a stack of #mi(`N=6`) identical layers. Each
layer has two sub-layers. The first is a multi-head self-attention
mechanism, and the second is a simple, position-wise fully connected
feed-forward network. We employ a residual connection around each of the
two sub-layers, followed by layer normalization. That is, the output of
each sub-layer is #mi(`\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))`),
where #mi(`\mathrm{Sublayer}(x)`) is the function implemented by the
sub-layer itself. To facilitate these residual connections, all
sub-layers in the model, as well as the embedding layers, produce
outputs of dimension #mi(`d_{\text{model}}=512`).
