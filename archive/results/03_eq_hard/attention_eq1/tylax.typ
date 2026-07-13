#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

                  We compute the matrix of outputs as:

 $  upright(A t t e n t i o n)(Q, K, V) = upright(s o f t m a x)(frac(Q K^(T), sqrt(d_(k)))) V  $

 Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.

 #math.equation(block: true, numbering: none)[
$  upright(M u l t i H e a d)(Q, K, V) & = upright(C o n c a t)(upright(h e a d_(1)), . . ., upright(h e a d_(h)))W^(O) \ "where" space.nobreak upright(h e a d_(i)) & = upright(A t t e n t i o n)(Q W^(Q)_(i), K W^(K)_(i), V W^(V)_(i)) \  $
]

 Where the projections are parameter matrices $W^(Q)_(i) in RR^(d_("model")times d_(k))$, $W^(K)_(i) in RR^(d_("model")times d_(k))$, $W^(V)_(i) in RR^(d_("model")times d_(v))$ and $W^(O) in RR^(h d_(v) times d_("model"))$.

 In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.

 $  upright(F F N)(x)= max(0, x W_(1) + b_(1)) W_(2) + b_(2)  $

 Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.

 #math.equation(block: true, numbering: none)[
$  P E_((p o s,2 i)) = sin(p o s / 1 0 0 0 0^(2 i /d_("model"))) \ P E_((p o s,2 i + 1)) = cos(p o s / 1 0 0 0 0^(2 i /d_("model")))  $
]

