#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
We compute the matrix of outputs as:

$ #mitex(`\begin{equation}
   \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\end{equation}`) $

Multi-head attention allows the model to jointly attend to information
from different representation subspaces at different positions. With a
single attention head, averaging inhibits this.

$ #mitex(`\begin{align*}
    \mathrm{MultiHead}(Q, K, V) &= \mathrm{Concat}(\mathrm{head_1}, ..., \mathrm{head_h})W^O\\
    \text{where}~\mathrm{head_i} &= \mathrm{Attention}(QW^Q_i, KW^K_i, VW^V_i)\\
\end{align*}`) $

Where the projections are parameter matrices
#mi(`W^Q_i \in \mathbb{R}^{d_{\text{model}}\times d_k}`),
#mi(`W^K_i \in \mathbb{R}^{d_{\text{model}}\times d_k}`),
#mi(`W^V_i \in \mathbb{R}^{d_{\text{model}}\times d_v}`) and
#mi(`W^O \in \mathbb{R}^{hd_v \times d_{\text{model}}}`).

In addition to attention sub-layers, each of the layers in our encoder
and decoder contains a fully connected feed-forward network, which is
applied to each position separately and identically. This consists of
two linear transformations with a ReLU activation in between.

$ #mitex(`\begin{equation}
   \mathrm{FFN}(x)=\max(0, xW_1 + b_1) W_2 + b_2
\end{equation}`) $

Since our model contains no recurrence and no convolution, in order for
the model to make use of the order of the sequence, we must inject some
information about the relative or absolute position of the tokens in the
sequence.

$ #mitex(`\begin{align*}
    PE_{(pos,2i)} = \sin(pos / 10000^{2i/d_{\text{model}}}) \\
    PE_{(pos,2i+1)} = \cos(pos / 10000^{2i/d_{\text{model}}})
\end{align*}`) $
