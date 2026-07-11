We compute the matrix of outputs as:

$ upright(A t t e n t i o n)\(Q\,K\,V\)= upright(s o f t m a x) (frac(Q K^T, sqrt(d_k))) V $

Multi-head attention allows the model to jointly attend to information
from different representation subspaces at different positions. With a
single attention head, averaging inhibits this.

$ upright(M u l t i H e a d)\(Q\,K\,V\) & = upright(C o n c a t)\(upright(h e a d_1)\,. . .\,upright(h e a d_h)\)W^O\
upright("where") med upright(h e a d_i) & = upright(A t t e n t i o n)\(Q W_i^Q\,K W_i^K\,V W_i^V\)\
 $

Where the projections are parameter matrices
$W_i^Q in bb(R)^(d_(upright("model")) times d_k)$,
$W_i^K in bb(R)^(d_(upright("model")) times d_k)$,
$W_i^V in bb(R)^(d_(upright("model")) times d_v)$ and
$W^O in bb(R)^(h d_v times d_(upright("model")))$.

In addition to attention sub-layers, each of the layers in our encoder
and decoder contains a fully connected feed-forward network, which is
applied to each position separately and identically. This consists of
two linear transformations with a ReLU activation in between.

$ upright(F F N)\(x\)= max\(0\,x W_1 + b_1\)W_2 + b_2 $

Since our model contains no recurrence and no convolution, in order for
the model to make use of the order of the sequence, we must inject some
information about the relative or absolute position of the tokens in the
sequence.

$ P E_(\(p o s\,2 i\)) = sin\(p o s\/10000^(2 i\/d_(upright("model")))\)\
P E_(\(p o s\,2 i + 1\)) = cos\(p o s\/10000^(2 i\/d_(upright("model")))\) $
