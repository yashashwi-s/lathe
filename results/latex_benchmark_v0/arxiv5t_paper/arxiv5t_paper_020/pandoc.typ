#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#footnote[$""^(*)$ Equal contribution \ $""^dagger$ Coresponding Author]

= Introduction
<introduction>
#figure([#block[
  #box(image("fig/metrics.png"))
  ]],
  caption: [
    Performance comparison on the RealBlur-J~[rim2020real] test dataset
    in terms of PSNR and GMACs. Our proposed MLWNet achieves both higher
    accuracy and smaller complexity in comparison with other
    state-of-the-arts.
  ]
)
<fig:metrics>

Most current top-performing single-image blind deblurring algorithms are
based on DNNs, which can be structurally categorized into
single-scale~[kong2023efficient][chen2022simple][zou2021sdwnet][kupyn2019deblurgan][tsai2022banet][tsai2022stripformer]
and multi-scale
approaches~[tao2018scale][zamir2021multi][cho2021rethinking][kim2022mssnet][li2022learning.]
Compared to single-scale methods, multi-scale methods are built on the
idea of moving from coarse-to-fine, and thus they decompose the
challenging single-image blind deblurring problem into easier-to-solve
sub-problems to restore the blurred image step-by-step.

Earlier DNNs exploiting the coarse-to-fine concept usually employ
estimators of different scales to produce restored images
gradually~[tao2018scale][nah2017deep][park2020multi.] However, not only is
the extracted semantic information not sufficiently representative, but
the use of the same complexity at different scales may lead to redundant
computations; More advanced multi-scale algorithms~[cho2021rethinking]
use a global encoder-decoder, which significantly reduces the
algorithm's runtime, multiple upsampling and downsampling leads to
insufficient restoration of detailed information, and therefore such
algorithms require the introduction of additional fusion modules to
encode input images for fusion with deeper semantics. In addition,
existing multi-scale algorithms use multiple-input and multiple-output
(MIMO) architectures, which require the introduction of manually
constructed downsampled image pairs, and usually employ simple
interpolation algorithms to generate low-resolution images for the sake
of efficiency, which is obviously not reliable.

We note that the gradual insertion of images used by existing
coarse-to-fine algorithms is redundant. Referring to numerous
algorithms~[lin2017feature][tan2020efficientdet][liu2018path][ghiasi2019fpn][kim2022mstr][wang2023yolov7]
that are widely used in downstream tasks, the network starts with a
single input and also extracts features at different scales. These
features can be aggregated by simple feature fusion to ultimately obtain
competitive results. That is, a DNN itself possesses the ability to
learn effective features at different scales. This inspired us to design
a multi-scale architecture that retains an original image as input and
sequentially restores images at each scale in output stage. This is not
only more theoretically sound, but also eliminates the time required to
generate pairs of images of different resolutions, as well as the huge
complexity increase brought about by fusion modules between RGB domain
and deep features.

The coarse-to-fine algorithm has another inherent defect. During
progressive restoration, the solution of the upper-level problem takes
the solution of the lower-level as initialization~[kim2022mssnet.]
Although this reduces the difficulty of solving the upper-level problem,
due to the smaller resolution of lower-level spatial, the features
transmitted upwards are semantically precise but spatially ambiguous,
thus the reatoration ability of multi-scale network in spatial details
is limited. Hence, there is an urgent need to improve the quality of
restoration of high-frequency detail part. A simple approach is to
introduce a frequency domain transform as an alternative to a spatial
domain transform. This would provide the algorithm with a choice and
direct its attention to different frequencies. In this paper, we
consider using the discrete wavelet transform for the following reasons:

+ Many recent state-of-the-art deblurring
  algorithms~[mao2021deep][kong2023efficient][zou2021sdwnet] have
  introduced the discrete Fourier transform (DFT) as a frequency prior,
  which provides information that helps the algorithm to identify and
  select high-and low-frequency components that need to be preserved
  during restoration. Compared to DFT, the discrete wavelet transform
  (DWT) is better suited to deal with images containing more abrupt
  signals~[daubechies1990wavelet.]

+ Realistic blur and synthetic blur have significant distributional
  differences~[rim2022realistic.] In the real world, due to the short
  exposure time of a camera, realistic blur has a specific
  directionality~[tsai2022banet], i.e., the blur trajectory is regionally
  continuous; conversely, synthetic blur has an unnatural and
  discontinuous trajectory. To fully utilize the potential deblurring
  guidance brought by this trajectory continuity, we use 2D-DWT to
  reveal blur directionality, distinguish changes in the blur signal
  along different directions, and provide the algorithm with a reliable
  basis for deblurring through adaptive learning.

To make 2D-DWT fit the data distribution and feature layer space more
closely, we implemented 2D-DWT with an adaptive data distribution by
using group convolution, transferring feature space from the spatial
domain into the wavelet domain, generating sub-signals with different
frequency features and different directional features, and then
constructing wavelet losses for them in order to constrain them by
self-supervision. Experimental results demonstrate that the proposed
method has advanced performance in terms of accuracy and efficiency
(Fig.~@fig:metrics).

In summary, our contributions are as follows:

- We propose a single-input and multiple-output(SIMO) multi-scale
  baseline for progressive image deblur, which reduces the complexity of
  existing multi-scale deblurring algorithms and improves the overall
  efficiency of image restoration networks.

- We construct a learnable discrete wavelet transform node(LWN) to
  provide reliable frequency and direction selection for the algorithm,
  which promotes the algorithm's restoration of the high-frequency
  components of edges and details.

- For the network to work better, reasonable multi-scale loss is
  proposed to guide pixel-by-pixel and scale-by-scale restoration. We
  also created reasonable self-supervised losses for the learnable
  wavelet transform to limit the learning direction of the wavelet
  kernel.

- We demonstrate the effectiveness of our algorithm under several motion
  blur datasets, especially real datasets, and obtain highly competitive
  results.

#figure(image("fig/overall_perfect.png"),
  caption: [
    The overall architecture of the proposed MLWNet, the SEB is a simple
    module designed with reference~[chen2022simple], the WFB and WHB
    apply the LWN that implements the learnable 2D-DWT. In training
    phase, supervised learning is performed using $cal(L)_(m u l t i)$
    and self-supervised restraint of the wavelet kernel is performed
    using $cal(L)_(w a v e l e t)$. In testing phase, only the highest
    scale restored images is output.
  ]
)
<fig:overall>

= Related Work
<related-work>
#strong[Single-scale Deblurring Algorithm.] Image deblurring have
developed rapidly in recent
years~[kupyn2018deblurgan][zhang2020deblurring][zhang2019deep][chen2022simple][kong2023efficient][li2023efficient.]
To preserve richer image details, Kupyn et al.~[kupyn2018deblurgan]
viewed deblurring as a special case of image-to-image conversion, and
for the first time utilized a GAN to recover images with richer details.
To provide a high-quality and simple baseline, Chen et
al.~[chen2022simple] proposed a nonlinear activation-free network that
obtained excellent results. Zamir et al.~[zamir2022restormer] proposed a
transformer with an encoder--decoder architecture that can be applied to
higher-resolution images and utilizes cross-channel attention. Kong et
al.~[kong2023efficient] utilized a domain-based self-attention solver to
reduce the transformer complexity and suppress artefacts. However, such
single-scale algorithms estimate complex restoration problems directly
and may require the design of restorers of higher complexity, which is
suboptimal in terms of efficiency~[kim2022mssnet.]

#strong[Multi-scale Deblurring Algorithm.] Multi-scale motion blur
removal methods aim to achieve progressive clear image recovery using a
multi-stage or multi-sub-network approach. The multi-scale algorithm
previously used in the field of image deblurring is based on
MIMO~[nah2017deep][tao2018scale][park2020multi][cho2021rethinking][li2022learning.]
Recently, Cho et al.~[cho2021rethinking] proposed MIMO-UNet, which
employs a multi-output single decoder as well as a multi-output single
decoder to simulate a multi-scale architecture consisting of stacked
networks, thereby greatly simplifying complexity. Zamir et
al.~[zamir2021multi] designed a multi-stage progressive image recovery
network to simplify the information flow between multiple sub-networks.
As shown in Sec.~@baseline, our proposed multi-scale approach further
simplifies the structure of multi-scale networks and better balances the
accuracy and complexity.

#strong[Application of Frequency in Deblurring.] Frequency is an
important property of images, in recent years frequency domain has been
introduced into numerous DNNs to be solved for various
tasks~[suvorov2022resolution][wang2022image][zhong2022detecting][kong2023efficient][yang2020fda][qin2021fcanet.]
Mao et al.~[mao2021deep] proposed DeepRFT, which introduced a residual
module based on the Fourier transform into an advanced algorithm. Kong
et al.~[kong2023efficient] proposed FFTformer, which introduced the
Fourier transform into a feed-forward network to effectively utilize
different frequency information. Zou et al.~[zou2021sdwnet] proposed
SDWNet, which utilized frequency domain information as a complement to
spatial domain information. Different from these methods, we introduce a
learnable 2D-DWT capable of adapting to the data distribution and
feature space, more suitable not only for dealing with digital images
rich in mutation signals, but also for dealing with real blurring.

= Proposed Method
<proposed-method>
Our proposed MLWNet(Fig.~@fig:overall) aims to explore an efficient
multi-scale architectural approach to achieve high-quality blind
deblurring of a single image. First, we designed a novel and highly
scalable SIMO multi-scale baseline to address the performance bottleneck
faced by partially multi-scale networks. It takes a single image as an
input and gradually generates a series of sharp images from the bottom
up. Then, we propose a learnable wavelet transform node (LWN) for image
deblurring, and it enhances the proposed algorithm's ability to restore
detail information.

== Multi-scale Baseline
<baseline>
Our multi-scale network maintains an encoder-decoder architecture, but
retains the original image with the highest resolution as input, and
restores sharp images of various scales sequentially in the output
stage. In this way, we eliminate the complexity of the fusion module
when dealing RGB images of different scales and with deep semantics.

For ease of understanding, we will introduce here the Encoder phase,
multi-scale semantic Fusion phase (hereafter referred to as Fusion
phase), and Decoder phase sequentially. As shown in Fig.~@fig:overall,
the Encoder stage consists of several gray Simple Encoder Blocks(SEB),
where information flows top-down for feature extraction; the Fusion
stage consists of several green Wavelet Fusion Blocks(WFB), where
information flows bottom-up for semantic fusion at different scales; and
the Decoder stage consists of several purple Wavelet Head Blocks(WHB),
and the bottom-up flow of information enables gradual restoration.

The Encoder stage is responsible for full feature extraction,
downsampling feature maps once after each block, and then passing the
feature maps to the Fusion stage or the Decoder stage as needed, whose
outputs $E_(o u t)^i$ to block of the $i - t h$ layer can be denoted as:
$ E_(o u t)^i & = {phi.alt_i (e m b e d \( x \))\, & upright("if ") i = i_(m a x)\
phi.alt_i (E_(o u t)^(i - 1))\, & o t h e r w i s e\
\
 $<eq:backbone> where $phi.alt_i$ represent the block of corresponding
layer of Encoder. The Fusion stage adapts and fuses information from
different scales of semantics produced in Encoder to generate
intermediate representations with deep semantics and shallow details.
The Fusion stage's outputs $E_(o u t)^i$ to the block of $i - t h$ layer
is expressed as in Eq.~@eq:neck, where $delta_i$ represents the block of
the corresponding layer of Fusion.
$ F_(o u t)^i & = {delta_i (E_(o u t)^i + E_(o u t)^(i - 1))\, & upright("if ") i = i_(m i n)\
delta_i (F_(o u t)^(i - 1) + E_(o u t)^i)\, & o t h e r w i s e\
\
 $<eq:neck> The Decoder stage utilizes the information passed by both
the Encoder and Fusion stages to progressively upsample the feature maps
and generating pre-output feature maps at each scale separately. Output
$D_(o u t)^i$ to the block of the $i - t h$ layer is denoted as in
Eq.~[eq:head.] Here $xi_i$ represents the block of the corresponding
layer of the Decoder.
$ D_(o u t)^i & = {xi_i (E_(o u t)^0)\, & upright("if ") i = i_(m i n)\
xi_i (D_(o u t)^(i - 1))\, & upright("if ") i > i_(m i n) upright(" and ") i < i_(m a x)\
xi_i (D_(o u t)^(i - 1) + F_(o u t)^(i - 1))\, & upright("if ") i = i_(m a x)\
\
 $<eq:head>

Each block in the Decoder is followed by a $3 times 3$ convolution to
generate a restored image at each scale. To improve inference
efficiency, all but the highest-scale outputs are generated in the
training phase to compute the multi-scale loss. We note that this design
also have a similar role with auxiliary head~[yu2021bisenet] in
facilitating the model's learning of the recovered uniform patterns.

#figure([#block[
  #box(image("fig/wavelet-conv.png"))
  ]],
  caption: [
    \(a)The process of learnable 2D-wavelet convolution. (b)The
    construction process of the $N times N$ 2D-wavelet kernel.
  ]
)
<fig:wavelet-conv>

== Learnable Discrete Wavelet Transform
<ldwt>
To alleviate the defects of multi-scale architectures in the recovery of
detail information, we design LWN and constructed the WFB and WHB based
on it. Unlike the Fourier transform, the wavelet transform has adaptive
time-frequency resolution, and performs excellently on digital images
rich in mutation signal. Its use in conjunction with DNNs has gained
increasing widespread
attention~[liu2020densely][liu2019multi][wolter2021adaptive][ha2021adaptive.]

For ease of understanding, the 1D-DWT case is given here first. For the
input discrete signal $t$, given the wavelet function
$psi_(j\,k)\(t\)= 2^(j / 2) psi\(2^j t - k\)$ for scaling factor $j$,
time factor $k$, and scale function
$phi.alt_(j\,k)\(t\)= 2^(j / 2) phi.alt\(2^j t - k\)$, the decomposition
of the input signal $t$ at $j_0$ is given by:
$ f\(t\)= sum_(j > j_0) sum_k d_(j\,k) psi_(j\,k)\(t\)+ sum_k c_(j_0\,k) phi.alt_(j_0\,k) (t) $
In this process, $d_(j\,k) = ⟨f \( t \) \, psi_(j\,k) \( t \)⟩$
represents the detail coefficients (i.e., high-frequency components),
$c_(j_0\,k) = ⟨f \( t \) \, phi.alt_(j_0\,k) \( t \)⟩$ represents the
approximation coefficients (i.e., low-frequency components) so that the
input signal can be disassembled step by step into a rich wavelet domain
signal. In order to use wavelet transform in DNN, we introduce the
analysis vectors
$arrow(a)_0\[k\]= ⟨1 / sqrt(2) phi.alt \( t / 2 \) \, phi.alt \( t - k \)⟩$,
$arrow(a)_1\[k\]= ⟨1 / sqrt(2) psi \( t / 2 \) \, phi.alt \( t - k \)⟩$
to represent the high and low frequency filters respectively, then:
$  & c_(j + 1\,p) = sum_k arrow(a)_0\[k - 2 p\]c_(j\,k)\
 & d_(j + 1\,p) = sum_k arrow(a)_1\[k - 2 p\]c_(j\,k) $<eq:cd>

According to Eq.~@eq:cd, the decomposition of the original signal over
the wavelet basis can be viewed as a recursive convolution of the
original signal with a specific filter using a step size of 2.
Similarly, the inverse wavelet transform can be realized by transposed
convolution of two synthetic vectors $arrow(s)_0$ and $arrow(s)_1$. We
extend the above situation to 2D by efficiently extracting axial
high-frequency information using 2D discrete wavelet transform (2D-DWT),
and designing learnable methods to make it adaptive to the data
distribution and feature layers. Fig.~@fig:wavelet-conv\(b) presents the
construction process of the forward wavelet convolution kernel in 2D,
which can be expressed as:
$ cal(F)_(l l) & = arrow(a_0) times arrow(a_0)^T\,cal(F)_(l h) = arrow(a_0) times arrow(a_1)^T\
cal(F)_(h l) & = arrow(a_1) times arrow(a_0)^T\,cal(F)_(h h) = arrow(a_1) times arrow(a_1)^T\
cal(K)_w & = upright("cat") (cal(F)_(l l) \, cal(F)_(l h) \, cal(F)_(h l) \, cal(F)_(h h)) $
We set $arrow(a_0)$ and $arrow(a_1)$ as learnable filters;
$cal(F)_(l l)$, $cal(F)_(l h)$, $cal(F)_(h l)$, and $cal(F)_(h h)$ are
low-frequency, horizontal high-frequency, vertical high-frequency, and
diagonal high-frequency convolution operators obtained from vector outer
products; The wavelet kernel $cal(K)_w$ is spliced from above
convolution operators.

Then we implement learnable wavelet transform as a group convolution
like Fig.~@fig:wavelet-conv\(a), given a set of input feature maps
$cal(X)_(i n) in (C \, H \, W)$, its projection in wavelet domain
$cal(X)_(o u t) in (4 C \, H / 2 \, W / 2)$ (low-frequency, horizontal
high-frequency, vertical high-frequency, and diagonal high-frequency
component) is generated through the wavelet convolution. Similarly, the
construction method of the inverse kernel and the forward propagation
can be easily deduced, since they are inverse processes of each other.

Then, a natural question can then be posed: how to ensure the
correctness of the wavelet kernel learning and ensure that it does not
degrade into a general group convolution and cause performance
degradation?

A common practice is to introduce the principle of perfect
reconstruction~[wolter2021adaptive][liu2019multi] to constrain adaptive
wavelets, for a complex $z in bb(C)$, given a filter $arrow(x)$ that
applies to the $z$-transform, its $z$-transform can be expressed as
$X\(z\)= sum_(n in bb(Z)) arrow(x)\(n\)z^(- n)$. Then
$arrow(a)_0$,$arrow(a)_1$,$arrow(s)_0$,$arrow(s)_1$ can be obtained as
their corresponding z-transforms $A_0$,$A_1$,$S_0$,$S_1$, which must
then be satisfied if perfect reconstruction is desired:
$ A_0\(- z\)S_0\(z\)+ A_1\(- z\)S_1\(z\)= 0 $<eq:ac>
$ A_0\(z\)S_0\(z\)+ A_1\(z\)S_1\(z\)= 2 $<eq:pr>

Eq.~@eq:ac is known as alaising cancellation condition, which is used to
the cancellation of the aliasing effects arising from the downsampling.
We will give a detailed derivation of Eq.~@eq:ac and Eq.~@eq:pr in the
appendix.

After wavelet convolution, to achieve frequency restoration in the
wavelet domain, the input $cal(X)$ wavelet domain component was
separated into a separate dim, we use depth-wise convolution with an
expansion factor of $r$ for wavelet domain feature extraction and
transformation after the wavelet positive transform, and $1 times 1$
convolution for channel expansion and scaling, and finally a learnable
wavelet inverse transform is used to reduce the wavelet domain feature
maps to the spatial domain for output, which constitutes the LWN. We
follow the rules of~[chen2022simple] and design structurally similar
Wavelet Head Block (WHB) and Wavelet Fusion Block (WFB), both with LWN
as an important base module, but used for semantic aggregation and
multiscale output at different scales, respectively; thus, WHB adds the
recovery convolution branch after WFB.

== Loss
<loss>
#strong[Multi-scale Loss]. Follow PSNR loss~[chen2022simple], we propose
multi-scale loss function as the main loss of the algorithm for
calculating the pixel difference between restored image and GT at each
scale:
$ cal(L)_(m u l t i)\(x\,y\) & = sum_(k = 1)^K w_k times cal(L)_(p s n r) (x_k \, y_k)\
 $<eq:multi_loss> where $x$, $y$ denote the output and GT, respectively,
$k$ denotes the downsampling level, $w_k$ represents the weights under
the corresponding scale. Our design of $w_k$ is based on the simple
finding that we cannot produce absolutely accurate downsampled clear
images, and that the accuracy gap is progressively enlarged with
decreasing scales. To ensure that lower scale output layers do not
negatively affect the final output, we empirically set the loss weight
$w_k$ to $1 / k$ for the corresponding k-scale.

#strong[Wavelet Loss]. Both Eq.~@eq:ac and Eq.~@eq:pr can be easily
converted losses optimized toward a minimum of 0, here we use the mean
square error. Then, based on the convolvable nature of the $z$
transform, it is possible to construct convolutionally equivalent
substitutions for polynomial multiplications for the perfect
reconstruction condition:
$ L_(w a v e l e t)\(theta_i\) & = (sum_k^(N - 1) (⟨a_0 \, s_0⟩_k + ⟨a_1 \, s_1⟩_k) - hat(V)_(floor.l N / 2 floor.r))^2\
 & = (sum_k^(N - 1) (⟨(- 1)^k a_0 \, s_0⟩_k + ⟨\( - 1 \)^k a_1 \, s_1⟩_k))^2 $<eq:ac_loss>
where $k$ denotes the position of the filter when it performs the
convolution, $hat(V)$ is a vector with a center position value of two,
and $theta_i$ denotes the constructed filter

#strong[Overall Loss]\.Based on the multi-scale loss and wavelet loss,
the loss function used in this study is:
$ cal(L)_(t o t a l)\(x\,y\)= cal(L)_(w a v e l e t)\(theta_i\)+ cal(L)_(m u l t i)\(x\,y\) $<eq:total_loss>

#figure([#block[
  #box(image("fig/result_realblur.jpeg"))
  ]],
  caption: [
    Visual comparisons on the RealBlur-J dataset~[rim2020real.] The
    proposed method generates an image with clearer characters.
  ]
)
<fig:result_realblur>

= Experimental Results
<experimental-results>
== Datasets and Implementation Details
<datasets-and-implementation-details>
We evaluate our method on the realistic datasets RealBlur~[rim2020real]
and RSBlur~[rim2022realistic], as well as the synthetic dataset
GoPro~[nah2017deep], they are all composed of blurry-sharp image pairs.
During training we use AdamW optimizer ($alpha = 0.9$ and $beta = 0.9$)
for a total of 600K iterations. The initial value of the learning rate
is $10^(- 3)$ and is updated with cosine annealing schedule. The patch
size is set to be 256 × 256 pixels and we followed the training strategy
of~[zamir2022restormer][tsai2022stripformer.] For data augmentation, we
only use random flips and random rotations. Our experiments are
performed on NVIDIA GeForce RTX 3090 GPUs and Intel Xeon Gold 6130 CPU.

== Comparison with State-of-the-Art Methods
<comparison-with-state-of-the-art-methods>
We have compared our method with several advanced deblurring methods and
use the PSNR and SSIM to evaluate the quality of restored images.

#strong[Evaluations on the RealBlur dataset.] Since our proposed method
is driven by real-world deblurring, we first conduct comparisons on
RealBlur~[rim2020real.] The quantitative analysis results are shown in
Tab.~[tab:RealBlur], the PSNR value of our method is 1.02dB and 0.49dB
higher than state-of-the-art GRL on the RealBlur-J and RealBlur-R
datasets respectively. Compared to other multi-scale architectures, our
method has fewer model computational and running time while the
performance is better. Fig.~@fig:result_realblur shows visual comparison
on RealBlur-J dataset, our method obtains restored text with richer edge
details, while achieving the best contrast, sharpness, brightness, and
structural details of the image.

#block[
l|c|c|c|c||c & & & \ & PSNR & SSIM & PSNR & SSIM & \
DeblurGAN-v2~[kupyn2019deblurgan] & 29.69 & 0.870 & 36.44 & 0.935 & 0.04s
\ SRN~[tao2018scale] & 31.38 & 0.909 & 38.65 & 0.965 & 0.07s \
MPRNet~[zamir2021multi] & 31.76 & 0.922 & 39.31 & 0.972 & 0.09s \
SDWNet~[zou2021sdwnet] & 30.73 & 0.896 & 38.21 & 0.963 & 0.04s \
MIMO-UNet+~[cho2021rethinking] & 31.92 & 0.919 & - & - & 0.02s \
MIMO-UNet++~[cho2021rethinking] & 32.05 & 0.921 & - & - & - \
DeepRFT+~[mao2021deep] & 32.19 & 0.931 & 39.84 & 0.972 & 0.09s \
BANet~[tsai2022banet] & 32.00 & 0.923 & 39.55 & 0.971 & 0.06s \
BANet+~[tsai2022banet] & 32.42 & 0.929 & 39.90 & 0.972 & 0.12s \
Stripformer~[tsai2022stripformer] & 32.48 & 0.929 & 39.84 &
#underline[0.974] & 0.04s \ MSSNet~[kim2022mssnet] & 32.10 & 0.928 &
39.76 & 0.972 & 0.06s \ MSDI-Net~[li2022learning] & 32.35 & 0.923 & - & -
& 0.06s \ MAXIM-3S~[tu2022maxim] & 32.84 & #underline[0.935] & 39.45 &
0.962 & - \ FFTformer~[kong2023efficient] & 32.62 & 0.933 & 40.11 & 0.973
& 0.13s \ GRL-B~[li2023efficient] & 32.82 & 0.932 & #underline[40.20] &
#underline[0.974] & 1.28s \ MLWNet-S & #underline[33.02] & 0.933 & - & -
& 0.04s \ MLWNet-B & #strong[33.84] & #strong[0.941] & #strong[40.69] &
#strong[0.976] & 0.05s \

]
#strong[Evaluations on the RSBlur dataset.] We further conduct
experiments on the latest real-world deblurring dataset
RSBlur~[rim2022realistic] and follow the protocol of this dataset for
fair comparison. Tab.~@tab:RSBlur summarizes the quantitative evaluation
results of our method with advanced algorithms. The proposed MLWNet
achieved the highest PSNR and SSIM, which were 34.94 and 0.880
respectively. In addition, the model we trained on RSBlur dataset also
achieved the best results on RealBlur-J dataset. We show some visual
comparisons in Fig.~[fig:result_rsblur.] We note that our method
outperforms other methods in low-light blurry scenes, proving that the
proposed method makes textures and structures clearer.

#figure([#block[
  #box(image("fig/result_rsblur.jpeg"))
  ]],
  caption: [
    Visual comparisons on the RSBlur dataset~[rim2022realistic.] The
    deblurring performance of the proposed method in low-light is
    impressive, The recovery of characters and texture structures far
    exceeds other advanced methods.
  ]
)
<fig:result_rsblur>

#block[
#figure(
  align(center)[#table(
    columns: 5,
    align: (left,center,center,center,center,),
    table.cell(rowspan: 2)[Method], table.cell(align: center, colspan: 2)[RSBlur], table.cell(align: center, colspan: 2)[RealBlur-J],
    [PSNR], [SSIM], [PSNR], [SSIM],
    [SRN~[tao2018scale]], [32.53], [0.840], [29.86], [0.886],
    [MIMO-Unet~[cho2021rethinking]], [32.73], [0.846], [29.53], [0.876],
    [MIMO-Unet+~[cho2021rethinking]], [33.37], [0.856], [29.99], [0.889],
    [MPRNet~[zamir2021multi]], [33.61], [0.861], [30.46], [#underline[0.899]],
    [Restormer~[zamir2022restormer]], [33.69], [0.863], [#underline[30.48]], [0.891],
    [Uformer-B~[wang2022uformer]], [33.98], [0.866], [30.37], [#underline[0.899]],
    [SFNet~[cui2023selective]], [#underline[34.35]], [#underline[0.872]], [30.26], [0.897],
    [MLWNet-B], [#strong[34.94]], [#strong[0.880]], [#strong[30.53]], [#strong[0.905]],
  )]
  , caption: [Quantitative evaluations trained on the RSBlur
  dataset~[rim2022realistic], the RealBlur-J dataset was used for testing
  only.]
  , kind: table
  )

] <tab:RSBlur>
In addition, we evaluate the RSBlur dataset using models trained only on
RealBlur-J to fairly compare the generalization of methods to real
scenarios. As shown in Tab.~@tab:J2RSBlur, our method produced results
with highest PSNR value of 30.91. The results of Tab.~@tab:RSBlur and
Tab.~@tab:J2RSBlur show that our model has a better generalization
ability.

#block[
#figure(
  align(center)[#table(
    columns: 4,
    align: (left,center,center,center,),
    table.cell(rowspan: 2)[Method], table.cell(align: center, colspan: 2)[~[rim2020real]$arrow.r$
    ~[rim2022realistic]], table.cell(rowspan: 2)[],
    [PSNR], [SSIM],
    [DeblurGAN-v2~[kupyn2019deblurgan]], [30.15], [0.766], [42.0],
    [MPRNet~[zamir2021multi]], [29.56], [0.785], [760.8],
    [MIMO-UNet+~[cho2021rethinking]], [29.69], [0.792], [154.4],
    [BANet~[tsai2022banet]], [30.19], [0.806], [263.9],
    [BANet+~[tsai2022banet]], [#underline[30.24]], [#underline[0.809]], [588.7],
    [MSSNet~[kim2022mssnet]], [29.86], [0.806], [154.0],
    [FFTformer~[kong2023efficient]], [29.70], [0.787], [131.8],
    [MLWNet-B], [#strong[30.91]], [#strong[0.818]], [108.2],
  )]
  , caption: [Quantitative evaluation for generalizability shows the
  results of models trained on the RealBlur-J dataset and tested on the
  RSBlur dataset, MACs are measured on 256 × 256 patches.]
  , kind: table
  )

] <tab:J2RSBlur>
#figure([#block[
  #box(image("fig/result_gopro.jpeg"))
  ]],
  caption: [
    Visual comparisons on the GoPro dataset~[nah2017deep.] Our method
    better preserves texture information without sharpening.
  ]
)
<fig:result_gopro>

#strong[Evaluations on the GoPro dataset.] We conduct a extensive
comparison with advanced algorithms on GoPro~[nah2017deep.]
Tab.~@tab:gopro shows the quantitative evaluation results. The gap
between our method and the state-of-the-art FFTformer is only 0.001 in
SSIM value, while the running time is reduced by 60%. We show a visual
comparison on the GoPro dataset in Fig.~[fig:result_gopro.] We can see
that our method recovers blurred textures well without sharpening. For
the reasons why the proposed MLWNet does not achieve optimal performance
in synthetic blurry, we conducted a detailed analysis in Sec.~[analysis.]

#block[
#figure(
  align(center)[#table(
    columns: 4,
    align: (left,center,center,center,),
    table.cell(rowspan: 2)[Method], table.cell(align: center, colspan: 2)[GOPRO], table.cell(rowspan: 2)[],
    [PSNR], [SSIM],
    [DeblurGAN-v2~[kupyn2019deblurgan]], [29.55], [0.934], [0.04s],
    [SRN~[tao2018scale]], [30.26], [0.934], [0.07s],
    [DMPHN~[zhang2019deep]], [31.20], [0.945], [0.21s],
    [SDWNet~[zou2021sdwnet]], [31.26], [0.966], [0.04s],
    [MPRNet~[zamir2021multi]], [32.66], [0.959], [0.09s],
    [MIMO-UNet+~[cho2021rethinking]], [32.45], [0.957], [0.02s],
    [DeepRFT+~[mao2021deep]], [33.23], [0.963], [0.09s],
    [MAXIM-3S~[tu2022maxim]], [32.86], [0.961], [-],
    [Stripformer~[tsai2022stripformer]], [33.08], [0.962], [0.04s],
    [MSDI-net~[li2022learning]], [33.28], [0.964], [0.06s],
    [Restormer~[zamir2022restormer]], [33.57], [0.966], [0.08s],
    [NAFNet~[chen2022simple]], [33.69], [0.967], [0.04s],
    [FFTformer~[kong2023efficient]], [#strong[34.21]], [#strong[0.969]], [0.13s],
    [GRL-B~[li2023efficient]], [#underline[33.93]], [#underline[0.968]], [1.28s],
    [MLWNet-B], [33.83], [#underline[0.968]], [0.05s],
  )]
  , caption: [Quantitative evaluations trained and tested on the GoPro
  dataset~[nah2017deep.] Our proposed MLWNet obtains competitive results
  with a combination of time efficiency and accuracy.]
  , kind: table
  )

] <tab:gopro>
= Analysis and Discussion
<analysis>
In this section, we provide a more in-depth analysis and show the
contribution of each component of the proposed method. We perform 20w
iterations on the RealBlur-J dataset for abtation with a batch size of 8
to train our method using a version of the model with a width of 32, and
the results are shown in Tab.~[tab:wavelet.]

#strong[Single-scale vs. Multi-scale]. Given that each node of the
baseline network is composed of SEB, we have deformed the multi-scale
and single-scale according to the architecture. Multi-scale architecture
has improved PSNR and SSIM values to varying degrees, indicating that
the SIMO strategy we adopt helps remove motion blur to a certain extent.
As shown in Sec.~@baseline, we use SIMO for coarse-to-fine restoration,
and only use multiple outputs to calculate multi-scale losses during
training.

#strong[WFB and WHB]. We default to using WFB and WHB via
$cal(L)_(w a v e l e t)$ statute in this section, we also proved the
effectiveness of LWN, because LWN is a subpart of the first two. After
applying them, the PSNR index improved by 0.25dB compared to the
multi-scale baseline, which shows that LWN and its extension modules can
easily help multi-scale algorithms improve detail recovery capabilities.
Fig.~@fig:feature shows the four types of feature maps generated after
forward learnable wavelet convolution. We can see that the high and low
frequencies of the input feature map are mixed together, and after
wavelet group convolution, the network exerts different attention on the
feature information in different directions or frequencies.

#strong[Effectiveness of $cal(L)_(w a v e l e t)$]. By adding unreduced
WFB and WHB to the baseline without using wavelet loss, the performance
improvement of the baseline is minimal and does not break the bottleneck
of multiscale detail recovery, which suggests that the wavelet
convolution degenerates into a general group convolution that only
serves to deepen the network, proving that merely deepening the network
is ineffective for the restoration of detail information.

#block[
#figure(
  align(center)[#table(
    columns: 7,
    align: (center,center,center,center,center,center,center,),
    table.header([SIMO], [WFB], [WFB], [$cal(L)_(w a v e l e t)$], [PSNR], [SSIM], [MACs(G)],),
    table.hline(),
    [], [], [], [], [32.29], [0.924], [19.24],
    [], [], [], [], [32.37], [0.929], [19.29],
    [], [], [], [], [32.40], [0.928], [28.21],
    [], [], [], [], [32.49], [0.928], [25.28],
    [], [], [], [], [32.57], [0.929], [22.22],
    [], [], [], [], [32.62], [0.931], [28.21],
  )]
  , caption: [Ablation study on components of the proposed MLWNet. We
  set the baseline network to use SEB in its entirety, and models that
  do not use SIMO will represent single scales using SISO.]
  , kind: table
  )

] <tab:wavelet>
#figure([#block[
  #box(image("fig/feature.pdf"))
  ]],
  caption: [
    Feature maps representing high-and low-frequency components
    generated after learnable wavelet convolution. Zoom in on the screen
    for the best view.
  ]
)
<fig:feature>

#strong[Limitations and analysis]. It is observed from
Tab.~[tab:RealBlur-]@tab:J2RSBlur that our method fails to achieve the
same expected high performance with synthetic blur as it does with
realistic blur. We try to analyze the reasons for this phenomenon via
dataset comparison and experimental results. First, the average frame
synthesis method used in the synthetic blur dataset leads to unnatural
discontinuous blur trajectories, thereby introducing strange
high-frequency information interference (see Fig.~@fig:synthetic).
Second, synthetic data tends to produce an unnatural mixture of
frequencies. It is easy to mix with the average color area at the edge
of the texture, causing the confusion of high-low frequency information.

#figure([#block[
  #box(image("fig/synthetic.jpeg"))
  ]],
  caption: [
    The difference between realistic blur (a) and synthetic blur (b). In
    the green box, the synthetic blur appears with color averaging
    resulting in high and low frequency confusion, and in the blue box
    has unnatural discontinuous trajectories.
  ]
)
<fig:synthetic>

#block[
#figure(
  align(center)[#table(
    columns: 6,
    align: (center,center,center,center,center,center,),
    table.header([Noise Level], [L1], [L2], [L3], [L4], [L5],),
    table.hline(),
    [GoPro], [34.81], [34.66], [33.76], [33.19], [32.63],
    [RealBlur-J], [33.92], [33.81], [33.97], [33.93], [33.54],
  )]
  , caption: [Performance comparison at different noise difference
  levels, where L3 contains the noise difference mean.]
  , kind: table
  )

] <tab:noise>
Finally, there is a large difference in noise levels between synthetic
blur and real blur. We follow~[chen2015efficient] to calculate the noise
level of each testset, and divided the noise difference between clear
images and blurred images of GoPro and RealBlur-J into 5 levels for
separate testing. As shown in Tab.~@tab:noise, we note that as the noise
difference increases, our method maintains good performance on
RealBlur-J, while the performance drops fast on GoPro. This shows that
our method is robust to the noise of real blur, and that there are
differences in the noise between synthetic blur and real blur.

= Conclusion
<conclusion>
In this paper, we propose a SIMO-based multi-scale architecture to
achieve efficient motion deblurring. We have developed a learnable
discrete wavelet transform module, which not only improves the
algorithm's ability to recover details, but is also more applicable to
the real world. In addition, we construct a reasonable multi-scale loss
to guide the recovery of blurred images pixel by pixel and scale by
scale, and constrain the learning direction of the wavelet kernel with
self-supervised loss to achieve better image deblurring. Through
extensive experiments on multiple real and synthetic datasets, we
demonstrate that it outperforms existing state-of-the-art methods in
terms of quality and efficiency of image restoration, especially with
optimal deblurring performance and generalization in real scenes.
