#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Introduction
<introduction>
6D object pose estimation aims to estimate the 6D pose of an object
including its location and orientation, which has a wide range of
applications, such as augmented reality
[marchand2015pose][Rambach20186DoFOT], robotic manipulation
[perez2016robot][busam2015stereo], and automatic driving [wu20196d.]
Recently, various methods
[peng2019pvnet][xu2022rnnpose][su2022zebrapose][castro2023crt][kehl2017ssd][hu2020single][wang2021gdr][chen2020end][hodan2020epos]
have been proposed to conduct RGB-based 6D object pose estimation since
RGB images are easy to obtain. Despite the increased efforts, a variety
of challenges persist in RGB-based 6D object pose estimation, including
occlusions, cluttered backgrounds, and changeable environment
[xiang2018posecnn][peng2019pvnet][di2021so][wang2021occlusion][mei2022spatial.]
These challenges can introduce significant noise and indeterminacy into
the pose estimation process, leading to error-prone predictions
[peng2019pvnet][di2021so][mei2022spatial.]

Meanwhile, diffusion models [NEURIPS2020_DDPM][song2021denoising] have
achieved appealing results in various generation tasks such as image
synthesis [NEURIPS2020_DDPM][dhariwal2021diffusion] and image editing
[meng2021sdedit.] Specifically, diffusion models are able to recover
high-quality determinate samples (e.g., clean images) from a noisy and
indeterminate input data distribution (e.g., random noise) via a
step-by-step denoising process [NEURIPS2020_DDPM][song2021denoising.]
Motivated by such a strong denoising capability
[NEURIPS2020_DDPM][gu2022stochastic][gong2023diffpose], we aim to leverage
diffusion models to handle the RGB-based 6D object pose estimation task,
since this task also involves tackling noise and indeterminacy. However,
it can be difficult to directly use diffusion models to estimate the
object pose, because diffusion models often start denoising from random
Gaussian noise [NEURIPS2020_DDPM][song2021denoising.] Meanwhile, in
RGB-based 6D object pose estimation, the object pose is often extracted
from an intermediate representation, such as keypoint heatmaps
[chen2020end], pixel-wise voting vectors [peng2019pvnet], or object
surface keypoint features [castro2023crt.] Such an intermediate
representation encodes useful distribution priors about the object pose.
Thus starting denoising from such an representation shall effectively
assist the diffusion model in recovering accurate object poses. To
achieve this, we propose a novel diffusion-based object pose estimation
framework (#strong[6D-Diff]) that can exploit prior distribution
knowledge from the intermediate representation for better performance.

#figure(image("fig1.png"),
  caption: [
    Overview of our proposed #strong[6D-Diff] framework. As shown, given
    the 3D keypoints from the object 3D CAD model, we aim to detect the
    corresponding 2D keypoints in the image to obtain the 6D object
    pose. Note that when detecting keypoints, there are often challenges
    such as occlusions (including self-occlusions) and cluttered
    backgrounds that can introduce noise and indeterminacy into the
    process, impacting the accuracy of pose prediction.
  ]
)
<fig:intro>

Overall, our framework is a #emph[correspondence-based] framework, in
which to predict an object pose, given the 3D keypoints pre-selected
from the object 3D CAD model, we first predict the coordinates of the 2D
image keypoints corresponding to the pre-selected 3D keypoints. We then
use the 3D keypoints together with the predicted 2D keypoints
coordinates to compute the 6D object pose using a Perspective-n-Point
(PnP) solver [gao2003complete][lepetit2009ep.] As shown in
Fig.~@fig:intro, to predict the 2D keypoints coordinates, we first
extract an intermediate representation (the 2D keypoints heatmaps)
through a keypoints distribution initializer. As discussed before, due
to various factors, there often exists noise and indeterminacy in the
keypoints detection process and the extracted heatmaps can be noisy as
shown in Fig. [fig:demo.] Thus we pass the distribution modeled from
these keypoints heatmaps into a diffusion model to perform the denoising
process to obtain the final keypoints coordinates prediction.

Analogous to non-equilibrium thermodynamics [sohl2015deep], given a 2D
image keypoint, we can consider all its possible locations in the image
as particles in thermodynamics. Under low indeterminacy, the particles
(possible locations) w.r.t. each 2D keypoint gather, and each keypoint
can be determinately and accurately localized. In contrast, under high
indeterminacy, these particles can stochastically spread over the input
image, and it is difficult to localize each keypoint. The process of
converting particles from low indeterminacy to high indeterminacy is
called the #emph[forward process] of the diffusion model. The goal of
the diffusion model is to reverse the above forward process (through a
#emph[reverse process]), i.e., converting the particles from high
indeterminacy to low indeterminacy. Here in our case, we aim to convert
the indeterminate keypoints coordinates distribution modeled from the
heatmaps into the determinate distribution. Below we briefly introduce
the forward process and the reverse process in our diffusion model.

In the forward process, we aim to generate supervision signals that will
be used to optimize the diffusion model during the reverse process.
Specifically, given a set of pre-selected 3D keypoints, we first acquire
ground-truth coordinates of their corresponding 2D keypoints using the
ground-truth object pose. Then these determinate ground-truth 2D
coordinates are gradually diffused towards the indeterminate
distribution modeled from the intermediate representation, and the
distributions generated along the way will be used as supervision
signals. Note that, as the distribution modeled from the intermediate
representation can be complex and irregular, it is difficult to
characterize such a distribution via the Gaussian distribution. This
means that simply applying diffusion models in most existing generation
works [NEURIPS2020_DDPM][song2021denoising][dhariwal2021diffusion], which
start denoising from the random Gaussian noise, can introduce
potentially large error. To tackle this challenge, we draw inspiration
from the fact that the Mixture of Cauchy (MoC) model can characterize
complex and intractable distributions in an effective and robust manner
[sym11091186.] Thus we propose to model the intermediate representation
using a MoC distribution instead of simply treating it as a random
Gaussian noise. In this way, we gradually diffuse the determinate
distribution (ground truth) of keypoints coordinates towards the modeled
MoC distribution during the forward process.

#figure(image("fig_demo.png"),
  caption: [
    Above we show two examples of keypoint heatmaps, which serve as the
    intermediate representation [chen2020end][peng2019pvnet][castro2023crt]
    in our framework. The red dots indicate the ground-truth locations
    of the keypoints. As shown above, due to occlusions and cluttered
    backgrounds, the keypoint heatmaps are noisy, which reflects the
    noise and indeterminacy during the keypoints detection process.
  ]
)
<fig:demo>

Correspondingly, in the reverse process, starting from the MoC
distribution modeled in the forward process, we aim to learn to recover
the ground-truth keypoints coordinates. To achieve this, we leverage the
distributions generated step-by-step during the forward process as the
supervision signals to train the diffusion model to learn the reverse
process. In this way, the diffusion model can learn to convert the
indeterminate MoC distribution of keypoints coordinates into a
determinate one smoothly and effectively. After the reverse process, the
2D keypoints coordinates obtained from the final determinate
distribution are used to compute the 6D object pose with the
pre-selected 3D keypoints. Moreover, we further facilitate the model
learning of such a reverse process by injecting object features as
context information.

Our work makes three main contributions. 1) We propose a novel
#strong[6D-Diff] framework, in which we formulate keypoints detection
for 6D object pose estimation as a reverse diffusion process to
effectively eliminate the noise and indeterminacy in object pose
estimation. 2) To take advantage of the intermediate representation that
encodes useful prior distribution knowledge for handling this task, we
propose a novel MoC-based diffusion process. Besides, we facilitate the
model learning by utilizing object features. 3) Our framework achieves
state-of-the-art performance on the evaluated benchmarks.

= Related Work
<related-work>
#strong[RGB-based 6D Object Pose Estimation] has received a lot of
attention
[xiang2018posecnn][park2019pix2pose][peng2019pvnet][rad2017bb8][tekin2018real][su2022zebrapose][castro2023crt][Iwase_2021_ICCV][li2018deepim][Manhardt_2018_ECCV][Sundermeyer2018Implicit3O][Zakharov2019DPOD6P][xu2022rnnpose][haugaard2022surfemb][li2022dcl][liu2022gdrnpp_bop][yang2023object][guo2023knowledge][hai2023rigidity][hai2023shape.]
Some works [xiang2018posecnn][kehl2017ssd][hu2020single][wang2021gdr]
proposed to directly regress object poses. However, the non-linearity of
the rotation space makes direct regression of object poses difficult
[li2022dcl.] Compared to this type of #emph[direct methods],
#emph[correspondence-based methods]
[chen2020end][hodan2020epos][park2019pix2pose][peng2019pvnet][rad2017bb8][tekin2018real][su2022zebrapose]
often demonstrate better performance, which estimate 6D object poses via
learning 2D-3D correspondences between the observed image and the object
3D model.

Among #emph[correspondence-based methods], several works
[rad2017bb8][peng2019pvnet][tekin2018real][oberweger2018making][ren2022robust]
aim to predict the 2D keypoints coordinates corresponding to specific 3D
keypoints. BB8 [rad2017bb8] proposed to detect the 2D keypoints
corresponding to the 8 corners of the object's 3D bounding box. Later,
PVNet [peng2019pvnet] achieved better performance by estimating 2D
keypoints for sampled points on the surface of the object 3D model via
pixel-wise voting. Moreover, various methods
[park2019pix2pose][Zakharov2019DPOD6P][hodan2020epos][wang2021gdr][su2022zebrapose]
establish 2D-3D correspondences by localizing the 3D model point
corresponding to each observed object pixel. Among these methods, DPOD
[Zakharov2019DPOD6P] explored the use of UV texture maps to facilitate
model training, and ZebraPose [su2022zebrapose] proposed to encode the
surface of the object 3D model efficiently through a hierarchical binary
grouping. Besides, several pose refinement methods
[Iwase_2021_ICCV][li2018deepim][Manhardt_2018_ECCV][xu2022rnnpose] have been
proposed, which conducted pose refinement given an initial pose
estimation.

In this paper, we also regard object pose estimation as a 2D-3D
correspondence estimation problem. Different from previous works, here
by formulating 2D-3D correspondence estimation as a distribution
transformation process (denoising process), we propose a new framework
(#strong[6D-Diff]) that trains a diffusion model to perform progressive
denoising from an indeterminate keypoints distribution to the desired
keypoints distribution with low indeterminacy.

#strong[Diffusion Models]
[NEURIPS2020_DDPM][song2021denoising][dhariwal2021diffusion][sohl2015deep]
are originally introduced for image synthesis. Showing appealing
generation capabilities, diffusion models have also been explored in
various other tasks
[meng2021sdedit][gu2022stochastic][lugmayr2022repaint][gong2023diffpose][urain2022se3dif][lee2023bias][hsiao2023confronting],
such as image editing [meng2021sdedit] and image impainting
[lugmayr2022repaint.] Here we explore a new framework that tackles object
pose estimation with a diffusion model. Different from previous
generation works
[dhariwal2021diffusion][meng2021sdedit][lugmayr2022repaint] that start
denoising from random noise, to aid the denoising process for 6D object
pose estimation, we design a novel MoC-based diffusion mechanism that
enables the diffusion model to start denoising from a distribution
containing useful prior distribution knowledge regarding the object
pose. Moreover, we condition the denoising process on the object
features, to further guide the diffusion model to obtain accurate
predictions.

= Method
<method>
To handle the noise and indeterminacy in RGB-based 6D object pose
estimation, from a novel perspective of distribution transformation with
progressive denoising, we propose a framework (#strong[6D-Diff]) that
represents a new brand of diffusion-based solution for 6D object pose
estimation. Below we first revisit diffusion models in
Sec.~[Sec:revisiting.] Then we discuss our proposed framework in
Sec.~@Sec:training, and introduce its training and testing scheme in
Sec.~[Sec:overall.] We finally detail the model architecture in
Sec.~[Sec:architecture.]

== Revisiting Diffusion Models
<Sec:revisiting>
The diffusion model [NEURIPS2020_DDPM][song2021denoising], which is a kind
of probabilistic generative model, consists of two parts, namely the
forward process and the reverse process. Specifically, given an original
sample $d_0$ (e.g., a clean image), the process of diffusing the sample
$d_0$ iteratively towards the noise (typically Gaussian noise)
$d_K tilde.op cal(N)\(bold("0")\,bold("I")\)$ (i.e.,
$d_0 arrow.r d_1 arrow.r . . . arrow.r d_K$) is called the forward
process. In contrast, the process of denoising the noise $d_K$
iteratively towards the sample $d_0$ (i.e.,
$d_K arrow.r d_(K - 1) arrow.r . . . arrow.r d_0$) is called the reverse
process. Each process is defined as a Markov chain.

#strong[Forward Process.] To obtain supervision signals for training the
diffusion model to learn to perform the reverse process in a stepwise
manner, we need to acquire the intermediate step results
${ d_k }_(k = 1)^(K - 1)$. Thus the forward process is first performed
to generate these intermediate step results for training purpose.
Specifically, the posterior distribution $q\(d_(1 : K)\|d_0\)$ from
$d_1$ to $d_K$ is formulated as: \$\$\\begin{equation}
 \\label{eq:revisiting\_1}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
& q(d\_{1:K}|d\_0) = \\prod^K\_{k=1}q(d\_k|d\_{k-1}) \\\\
& q(d\_k|d\_{k-1}) = \\mathcal{N}(d\_k; \\sqrt{1-\\beta\_k}d\_{k-1}, \\beta\_k\\textbf{I})
\\end{aligned}
\\end{equation}\$\$ where ${ beta_k in\(0\,1\)}_(k = 1)^K$ denotes a set
of fixed variance controllers that control the scale of the injected
noise at different steps. According to Eq.~[eq:revisiting_1], we can
derive $q\(d_k\|d_0\)$ in closed form as: \$\$\\begin{equation}
 \\label{eq:revisiting\_2}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
& q(d\_k|d\_0) = \\mathcal{N}(d\_k; \\sqrt{\\overline{\\alpha}\_k}d\_0, (1-\\overline{\\alpha}\_k)\\textbf{I})
\\end{aligned}
\\end{equation}\$\$ where $alpha_k = 1 - beta_k$ and
$overline(alpha)_k = product_(s = 1)^k alpha_s$. Based on
Eq.~[eq:revisiting_2], $d_k$ can be further expressed as:
\$\$\\begin{equation}
 \\label{eq:revisiting\_3}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
& d\_k = \\sqrt{\\overline{\\alpha}\_k}d\_0 + \\sqrt{1 - \\overline{\\alpha}\_k}\\epsilon
\\end{aligned}
\\end{equation}\$\$ where
$epsilon.alt tilde.op cal(N)\(bold("0")\,bold("I")\)$. From
Eq.~[eq:revisiting_3], we can observe that when the number of diffusion
steps $K$ is sufficiently large and $overline(alpha)_K$ correspondingly
decreases to nearly zero, the distribution of $d_K$ is approximately a
standard Gaussian distribution, i.e.,
$d_K tilde.op cal(N)\(bold("0")\,bold("I")\)$. This means $d_0$ is
gradually corrupted into Gaussian noise, which conforms to the
non-equilibrium thermodynamics phenomenon of the diffusion process
[sohl2015deep.]

#strong[Reverse Process.] With the intermediate step results
${ d_k }_(k = 1)^(K - 1)$ acquired in the forward process, the diffusion
model is trained to learn to perform the reverse process. Specifically,
in the reverse process, each step can be formulated as a function $f$
that takes $d_k$ and the diffusion model $M_(d i f f)$ as inputs and
generate $d_(k - 1)$ as the output, i.e.,
$d_(k - 1) = f\(d_k\,M_(d i f f)\)$.

After training the diffusion model, during inference, we do not need to
conduct the forward process. Instead, we only conduct the reverse
process, which converts a random Gaussian noise
$d_K tilde.op cal(N)\(bold("0")\,bold("I")\)$ into a sample $d_0$ of the
desired distribution using the trained diffusion model.

#figure(image("fig2.png", width: 90.0%),
  caption: [
    Illustration of our framework. During testing, given an input image,
    we first crop the Region of Interest (ROI) from the image through an
    object detector. After that, we feed the cropped ROI to the
    keypoints distribution initializer to obtain the heatmaps that can
    provide useful distribution priors about keypoints, to initialize
    $D_K$. Meanwhile, we can obtain object features $f_(a p p)$. Next,
    we pass $f_(a p p)$ into the encoder, and the output of the encoder
    will serve as conditional information to aid the reverse process in
    the decoder. We sample $M$ sets of 2D keypoints coordinates from
    $D_K$, and feed these $M$ sets of coordinates into the decoder to
    perform the reverse process iteratively together with the step
    embedding $f_D^k$. At the final reverse step ($K$-th step), we
    average ${ d_0^i }_(i = 1)^M$ as the final keypoints coordinates
    prediction $d_0$, and use $d_0$ to compute the 6D pose with the
    pre-selected 3D keypoints via a PnP solver.
  ]
)
<fig:framework>

== Proposed Framework
<Sec:training>
Similar to previous works
[su2022zebrapose][peng2019pvnet][hu2019segmentation], our framework
predicts 6D object poses via a two-stage pipeline. Specifically, (i) we
first select $N$ 3D keypoints on the object CAD model and detect the
corresponding $N$ 2D keypoints in the image; (ii) we then compute the 6D
pose using a PnP solver. Here we mainly focus on the first stage and aim
to produce more accurate keypoint detection results.

When detecting 2D keypoints, factors like occlusions (including
self-occlusions) and cluttered backgrounds can bring noise and
indeterminacy into this process, and affect the accuracy of detection
results [peng2019pvnet][hu2019segmentation.] To handle this problem,
inspired by that diffusion models can iteratively reduce indeterminacy
and noise in the initial distribution (e.g., standard Gaussian
distribution) to generate determinate and high-quality samples of the
desired distribution [gu2022stochastic][gong2023diffpose], we formulate
keypoints detection as generating a determinate distribution of
keypoints coordinates ($D_0$) from an indeterminate initial distribution
($D_K$) via a diffusion model.

Moreover, to effectively adapt to the 6D object pose estimation task,
the diffusion model in our framework does not start the reverse process
from the common initial distribution (i.e., the standard Gaussian
distribution) as in most existing diffusion works
[NEURIPS2020_DDPM][dhariwal2021diffusion][song2021denoising.] Instead,
inspired by recent 6D object pose estimation works
[castro2023crt][wang2021gdr][chen2020end], we first extract an intermediate
representation (e.g., heatmaps), and use this representation to
initialize a keypoints coordinates distribution (i.e., $D_K$), which
will serve as the starting point of the reverse process. Such an
intermediate representation encodes useful prior distribution
information about keypoints coordinates. Thus by starting the reverse
process from this representation, we effectively exploit the
distribution priors in the representation to aid the diffusion model in
recovering accurate keypoints coordinates. Below, we first describe how
we initialize the keypoints distribution $D_K$, and then discuss the
corresponding forward and reverse processes in our new framework.

#strong[Keypoints Distribution Initialization.] We initialize the
keypoints coordinates distribution $D_K$ with extracted heatmaps.
Specifically, similar to [su2022zebrapose][li2019cdpn][labbe2020cosypose],
we first use an off-the-shelf object detector (e.g., Faster RCNN
[ren2015faster]) to detect the bounding box of the target object, and
then crop the detected Region of Interest (ROI) from the input image. We
send the ROI into a sub-network (i.e., the keypoints distribution
initializer) to predict a number of heatmaps where each heatmap
corresponds to one 2D keypoint. We then normalize each heatmap to
convert it to a probability distribution. In this way, each normalized
heatmap naturally represents the distribution of the corresponding
keypoint coordinates, and thus we can use these heatmaps to initialize
$D_K$.

#strong[Forward Process.] After distribution initialization, the next
step is to iteratively reduce the noise and indeterminacy in the
initialized distribution $D_K$ by performing the reverse process
($D_K arrow.r D_(K - 1) arrow.r . . . arrow.r D_0$). To train the
diffusion model to perform such a reverse process, we need to obtain the
distributions generated along the way (i.e., ${ D_k }_(k = 1)^(K - 1)$)
as the supervision signals. Thus, we first need to conduct the forward
process to obtain samples from ${ D_k }_(k = 1)^(K - 1)$. Specifically,
given the ground-truth keypoints coordinates distribution $D_0$, we
define the forward process as:
$D_0 arrow.r D_1 arrow.r . . . arrow.r D_K$, where $K$ is the number of
diffusion steps. In this forward process, we iteratively add noise to
the determinate distribution $D_0$, i.e., increasing the indeterminacy
of generated distributions, to transform it into the initialized
distribution $D_K$ with indeterminacy. Via this process, we can generate
${ D_k }_(k = 1)^(K - 1)$ along the way and use them as supervision
signals to train the diffusion model to perform the reverse process.

However, in our framework, we do not aim to transform the ground-truth
keypoints coordinates distribution $D_0$ towards a standard Gaussian
distribution via the forward process, because our initialized
distribution $D_K$ is not a random noise. Instead, as discussed before,
$D_K$ is initialized with heatmaps (as shown in Fig. @fig:framework),
since the heatmaps can provide rough estimations about the keypoints
coordinates distribution. To effectively utilize such priors in $D_K$ to
facilitate the reverse process, we aim to enable the diffusion model to
start the reverse process (denoising process) from $D_K$ instead of
random Gaussian noise. Thus, the basic forward process (described in
Sec. @Sec:revisiting) in existing generative diffusion models is not
suitable in our framework, which motivates us to design a new forward
process for our task.

However, it is non-trivial to design such a forward process, as the
initialized distribution $D_K$ is based on extracted heatmaps, and thus
$D_K$ can be complex and irregular, as shown in Fig. [fig:denoise.] Hence
modeling $D_K$ as a Gaussian distribution can result in potentially
large error. To handle this challenge, motivated by that the Mixture of
Cauchy (MoC) model can effectively and reliably characterize complex and
intractable distributions [sym11091186], we leverage MoC to characterize
$D_K$. Based on the characterized distribution, we can then perform a
corresponding MoC-based forward process.

Specifically, we denote the number of Cauchy kernels in the MoC
distribution as $U$, and use the Expectation-Maximum-type ($E M$)
algorithm [sym11091186][teimouri2018statistical] to optimize the MoC
parameters $eta^(M o C)$ to characterize the distribution $D_K$ as:
\$\$\\begin{equation}
 \\label{eq:training\_1}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
\\eta\_{\*}^{MoC} = EM \\Big( \\prod^V\_{v=1} \\sum^U\_{u=1} \\pi\_u Cauchy(d^v\_K|\\mu\_u, \\gamma\_u) \\Big)
\\end{aligned}
\\end{equation}\$\$ where ${ d_K^v }_(v = 1)^V$ denotes $V$ sets of
keypoints coordinates sampled from the distribution $D_K$. Note each set
of keypoints coordinates $d_K^v$ contains all the $N$ keypoints
coordinates (i.e., $d_K^v in bb(R)^(N times 2)$). $pi_u$ denotes the
weight of the $u$-th Cauchy kernel ($sum_(u = 1)^U pi_u$ = 1), and
$eta^(M o C) = { mu_1\,gamma_1\,. . .\,mu_U\,gamma_U }$ denotes the MoC
parameters in which $mu_u$ and $gamma_u$ are the location and scale of
the $u$-th Cauchy kernel. Via the above optimization, we can use the
optimized parameters $eta_(*)^(M o C)$ to model $D_K$ as the
characterized distribution ($hat(D)_K$). Given $hat(D)_K$, we aim to
conduct the forward process from the ground-truth keypoints coordinates
distribution $D_0$, so that after $K$ steps of forward diffusion, the
generated distribution reaches $hat(D)_K$. To this end, we modify
Eq.~[eq:revisiting_3] as follows:
$  & hat(d)_k = sqrt(overline(alpha)_k) d_0 +\(1 - sqrt(overline(alpha)_k)\)mu^(M o C) + sqrt(1 - overline(alpha)_k) epsilon.alt^(M o C) $<eq:training_2>
where $hat(d)_k in bb(R)^(N times 2)$ represents a sample (i.e., a set
of $N$ keypoints coordinates) from the generated distribution
$hat(D)_k$, $mu^(M o C) = sum_(u = 1)^U bb(1)_u mu_u$, and
$epsilon.alt^(M o C) tilde.op C a u c h y\(bold("0")\,sum_(u = 1)^U\(bb(1)_u gamma_u\)\)$.
Note that $bb(1)_u$ is a zero-one indicator and
$sum_(u = 1)^U bb(1)_u = 1$ and $P r o b\(bb(1)_u = 1\)= pi_u$.

From Eq.~@eq:training_2, we can observe that when $K$ is sufficiently
large and $overline(alpha)_K$ correspondingly decreases to nearly zero,
the distribution of $hat(d)_K$ reaches the MoC distribution, i.e.,
$hat(d)_K = mu^(M o C) + epsilon.alt^(M o C) tilde.op C a u c h y\(sum_(u = 1)^U\(bb(1)_u mu_u\)\,sum_(u = 1)^U\(bb(1)_u gamma_u\)\)$.
After the above MoC-based forward process, we can use the generated
${ hat(D)_k }_(k = 1)^(K - 1)$ as supervision signals to train the
diffusion model $M_(d i f f)$ to learn the reverse process. More details
about Eq.~@eq:training_2 can be found in Supplementary. Note that such a
forward process is only conducted to generate supervision signals for
training the diffusion model, while we only need to conduct the reverse
process during testing.

#strong[Reverse Process.] In the reverse process, we aim to recover a
desired determinate keypoints distribution $D_0$ from the initial
distribution $D_K$. As discussed above, we characterize $D_K$ via a MoC
model and then generate ${ hat(D)_k }_(k = 1)^(K - 1)$ as supervision
signals to optimize the diffusion model to learn to perform the reverse
process ($hat(D)_K arrow.r hat(D)_(K - 1) arrow.r . . . arrow.r D_0$),
in which the model iteratively reduces the noise and indeterminacy in
$hat(D)_K$ to generate $D_0$.

However, it can still be difficult to generate $D_0$ by directly
performing the reverse process from $hat(D)_K$, because the object
appearance features are lacking in $hat(D)_K$. Such features can help
constrain the model reverse process based on the input image to get
accurate predictions. Thus we further leverage the object appearance
features as context to guide $M_(d i f f)$ in the reverse process.
Specifically, we seek help from the keypoints distribution initializer
to formulate the object features $f_(a p p)$ and feed $f_(a p p)$ into
the diffusion model, as shown in Fig. [fig:framework.]

Our reverse process aims to generate a determinate distribution $D_0$
from the indeterminate distribution $hat(D)_K$ (during training) or
$D_K$ (during testing). Below we describe the reverse process during
testing. We first obtain $f_(a p p)$ from the input image. Then to help
the diffusion model to learn to perform denoising at each reverse step,
following [NEURIPS2020_DDPM][song2021denoising], we generate the unique
step embedding $f_D^k$ to inject the step number ($k$) information into
the model. In this way, given a set of noisy keypoints coordinates
$d_k in bb(R)^(N times 2)$ drawn from $D_k$ at the $k^(t h)$ step, we
use diffusion model $M_(d i f f)$, conditioned on the step embedding
$f_D^k$ and the object features $f_(a p p)$, to recover $d_(k - 1)$ from
$d_k$ as: \$\$\\begin{equation}
 \\label{eq:denoising}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
{d}\_{k-1} = M\_{diff}({d}\_k, f\_{app}, f^k\_D)
\\end{equation}\$\$

== Training and Testing
<Sec:overall>
#strong[Training.] Following [peng2019pvnet], we first select $N$ 3D
keypoints from the surface of the object CAD model using the farthest
point sampling (FPS) algorithm. Then we conduct the training process in
the following two stages.

In the first stage, to initialize the distribution $D_K$, we optimize
the keypoints distribution initializer. Specifically, for each training
sample, given the pre-selected $N$ 3D keypoints, we can obtain the
ground-truth coordinates of the corresponding $N$ 2D keypoints using the
ground-truth 6D object pose. Then for each keypoint, based on the
corresponding ground-truth coordinates, we generate a ground-truth
heatmap following [oberweger2018making] for training the initializer.
Thus for each training sample, we generate $N$ ground-truth heatmaps. In
this way, the loss function $L_(i n i t)$ for optimizing the initializer
can be formulated as: \$\$\\begin{equation}
\\label{eq:loss1}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
L\_{init} = {\\Big\\Vert \\textbf{H}\_{pred} - \\textbf{H}\_{GT} \\Big\\Vert}^2\_2
\\end{aligned}
\\end{equation}\$\$ where $bold("H")_(p r e d)$ and $bold("H")_(G T)$
denote the predicted heatmaps and ground-truth heatmaps, respectively.

In the second stage, we optimize the diffusion model $M_(d i f f)$. For
each training sample, to optimize $M_(d i f f)$, we perform the
following steps. (1) We first send the input image into an off-the-shelf
object detector [tian2019fcos] and then feed the detected ROI into the
trained initializer to obtain $N$ heatmaps. Meanwhile, we can also
obtain $f_(a p p)$. (2) We use the $N$ predicted heatmaps to initialize
$D_K$, and leverage the EM-type algorithm to characterize $D_K$ as a MoC
distribution $hat(D)_K$. (3) Based on $hat(D)_K$, we use the
ground-truth keypoints coordinates $d_0$ to directly generate $M$ sets
of ($hat(d)_1\,. . .\,hat(d)_K$) (i.e.,
${ hat(d)_1^i\,. . .\,hat(d)_K^i }_(i = 1)^M$) via the forward process
(Eq. @eq:training_2). (4) Then, we aim to optimize the diffusion model
$M_(d i f f)$ to recover $hat(d)_(k - 1)^i$ from $hat(d)_k^i$
iteratively. Following previous diffusion works
[NEURIPS2020_DDPM][song2021denoising], we formulate the loss $L_(d i f f)$
for optimizing $M_(d i f f)$ as follows ($hat(d)_0^i = d_0$ for all
$i$): \$\$\\begin{equation}
\\label{eq:loss1}
\\setlength{\\abovedisplayskip}{3pt}
\\setlength{\\belowdisplayskip}{3pt}
\\begin{aligned}
L\_{diff} = \\sum^M\_{i=1}\\sum^K\_{k=1} {\\Big\\Vert M\_{diff}(\\hat{d}^i\_{k}, f\_{app}, f^k\_D) - \\hat{d}^i\_{k-1} \\Big\\Vert}^2\_2
\\end{aligned}
\\end{equation}\$\$

#strong[Testing.] During testing, for each testing sample, by feeding
the input image to the object detector and the keypoints distribution
initializer consecutively, we can initialize $D_K$ and meanwhile obtain
$f_(a p p)$. Then, we perform the reverse process. During the reverse
process, we sample $M$ sets of noisy keypoints coordinates from $D_K$
(i.e., ${ d_K^i }_(i = 1)^M$) and feed them into the trained diffusion
model. Here we sample $M$ sets of keypoints coordinates, because we are
converting from a distribution ($D_K$) towards another distribution
($D_0$). Then the model iteratively performs the reverse steps. After
$K$ reverse diffusion steps, we obtain $M$ sets of predicted keypoints
coordinates (i.e., ${ d_0^i }_(i = 1)^M$). To obtain the final keypoints
coordinates prediction $d_0$, we compute the mean of the $M$
predictions. Finally, we can solve 6D object pose using a PnP solver,
like [peng2019pvnet][su2022zebrapose.]

== Model Architecture
<Sec:architecture>
Our framework mainly consists of the diffusion model ($M_(d i f f)$) and
the keypoints distribution initializer.

#strong[Diffusion Model $M_(d i f f)$.] As illustrated in
Fig.~@fig:framework, our proposed diffusion model $M_(d i f f)$ mainly
consists of a transformer encoder-decoder architecture. The object
features $f_(a p p)$ are sent into the encoder for extracting context
information to aid the reverse process in the decoder. $f_D^k$ and
${ d_k^i }_(i = 1)^M$ (or ${ hat(d)_k^i }_(i = 1)^M$ during training)
are sent into the decoder for the reverse process. Both the encoder and
the decoder contain a stack of three transformer layers.

#figure(image("fig5.png", width: 80.0%),
  caption: [
    Visualization of the denoising process of a sample with our
    framework. In this example, the target object is the yellow duck and
    for clarity, we here show three keypoints only. The red dots
    indicate the ground-truth locations of these three keypoints. The
    noisy heatmap before denoising reflects that factors like occlusions
    and clutter in the scene can introduce noise and indeterminacy when
    detecting keypoints. As shown, our diffusion model can effectively
    and smoothly reduce the noise and indeterminacy in the initial
    distribution step by step, finally recovering a high-quality and
    determinate distribution of keypoints coordinates. (Better viewed in
    color)
  ]
)
<fig:denoise>

#block[
<tab:lmo_results_table_>

]
<tab:ycbv_results_table>

More specifically, as for the encoder part, we first map
$f_(a p p) in bb(R)^(16 times 16 times 512)$ through a 1 × 1 convolution
layer to a latent embedding
$e_(a p p) in bb(R)^(16 times 16 times 128)$. To retain the spatial
information, following [vaswani2017attention], we further incorporate
positional encodings into $e_(a p p)$. Afterwards, we flatten
$e_(a p p)$ into a feature sequence ($bb(R)^(256 times 128)$), and send
into the encoder. The encoder output $f_(e n c)$ containing the
extracted object information will be sent into the decoder to aid the
reverse process. Note that during testing, for each sample, we only need
to conduct the above computation process once to obtain the
corresponding $f_(e n c)$.

The decoder part iteratively performs the reverse process. For notation
simplicity, below we describe the reverse process for a single sample
$d_k$ instead of the $M$ samples (${ d_1^i\,. . .\,d_K^i }_(i = 1)^M$).
Specifically, at the $k$-th reverse step, to inject the current step
number ($k$) information into the decoder, we first generate the step
embedding $f_D^k in bb(R)^(1 times 128)$ using the sinusoidal function
following [NEURIPS2020_DDPM][song2021denoising.] Meanwhile, we use an FC
layer to map the input $d_k in bb(R)^(N times 2)$ to a latent embedding
$e_k in bb(R)^(N times 128)$. Then we concatenate $f_D^k$ and $e_k$
along the first dimension, and send into the decoder. By interacting
with the encoder output $f_(e n c)$ (extracted object information) via
cross-attention at each layer, the decoder produces $f_(d e c)$, which
is further mapped into the keypoints coordinates prediction
$d_(k - 1) in bb(R)^(N times 2)$ via an FC layer. Then we send
$d_(k - 1)$ back to the decoder as the input to perform the next reverse
step.

#strong[Keypoints Distribution Initializer.] The initializer adopts a
ResNet-34 backbone, which is commonly used in 6D pose estimation methods
[wang2021gdr][su2022zebrapose][castro2023crt.] To generate heatmaps to
initialize the distribution $D_K$, we add two deconvolution layers
followed by a 1 × 1 convolution layer after the ResNet-34 backbone, and
then we obtain predicted heatmaps
$bold("H")_(p r e d) in bb(R)^(N times H / 4 times W / 4)$ where $H$ and
$W$ denote the height and width of the input ROI image respectively.
Moreover, the features outputted by the ResNet-34 backbone, combined
with useful features obtained from other methods
[su2022zebrapose][Lian_2023_ICCV], are used as the object features
$f_(a p p)$.

= Experiments
<experiments>
== Datasets & Evaluation Metrics
<datasets-evaluation-metrics>
Given that previous works [di2021so][Zakharov2019DPOD6P][iwase2021repose]
have reported the evaluation accuracy over 95% on the Linemod (LM)
dataset [hinterstoisser2013model], the performance on this dataset has
become saturated. Thus recent works [su2022zebrapose][castro2023crt]
mainly focus on using the LM-O dataset [brachmann2016uncertainty] and the
YCB-V dataset [xiang2018posecnn] that are more challenging, which we
follow.

#strong[LM-O Dataset.] The Linemod Occlusion (LM-O) dataset contains
1214 images and is a challenging subset of the LM dataset. In this
dataset, around 8 objects are annotated on each image and the objects
are often heavily occluded. Following [su2022zebrapose][castro2023crt], we
use both the real images from the LM dataset and the publicly available
physically-based rendering (pbr) images [denninger2019blenderproc] as the
training images for LM-O. Following [wang2021gdr][su2022zebrapose], on
LM-O dataset, we evaluate model performance using the commonly-used
ADD(-S) metric. For this metric, we compute the mean distance between
the model points transformed using the predicted pose and the same model
points transformed using the ground-truth pose. For symmetric objects,
following [xiang2018posecnn], the mean distance is computed based on the
closest point distance. If the mean distance is less than 10% of the
model diameter, the predicted pose is regarded as correct.

#strong[YCB-V Dataset.] The YCB-V dataset is a large-scale dataset
containing 21 objects and over 100k real images. The samples in this
dataset often exhibit occlusions and cluttered backgrounds. Following
[su2022zebrapose][castro2023crt], we use both the real images from the
training set of the YCB-V dataset and the publicly available pbr images
as the training images for YCB-V. Following
[wang2021gdr][su2022zebrapose], we evaluate model performance using the
following metrics: ADD(-S), AUC (Area Under the Curve) of ADD-S, and AUC
of ADD(-S). For calculating AUC, we set the maximum distance threshold
to 10 cm following [xiang2018posecnn.]

== Implementation Details
<implementation-details>
We conduct our experiments on Nvidia V100 GPU. We set the number of
pre-selected 3D keypoints $N$ to 128. During training, following
[su2022zebrapose][li2019cdpn], we utilize the dynamic zoom-in strategy to
produce augmented ROI images. During testing, we use the detected
bounding box with Faster RCNN [ren2015faster] and FCOS [tian2019fcos]
provided by CDPNv2 [li2019cdpn.] The cropped ROI image is resized to the
shape of $3 times 256 times 256$ ($H = W = 256$). We characterize $D_K$
via a MoC model with 9 Cauchy kernels ($U = 9$) for the forward
diffusion process. We optimize the diffusion model $M_(d i f f)$ for
1500 epochs using the Adam optimizer [kingma2014adam] with an initial
learning rate of 4e-5. Moreover, we set the number of sampled sets $M$
to 5, and the number of diffusion steps $K$ to 100. Following
[su2022zebrapose], we use Progressive-X [barath2019progressive] as the PnP
solver. Note that during testing, instead of performing the reverse
process with all the $K$ steps, we accelerate the process with DDIM
[song2021denoising], a recently proposed diffusion acceleration method.
With DDIM acceleration, we only need to perform 10 steps to finish the
reverse process during testing.

== Comparison with State-of-the-art Methods
<comparison-with-state-of-the-art-methods>
#strong[Results on LM-O Dataset.] As shown in
Tab.~@tab:lmo_results_table_, compared to existing methods, our method
achieves the best mean performance, showing the superiority of our
method. We also show qualitative results on the LM-O dataset in Fig.
[fig:visualization.] As shown, even in the presence of large occlusions
(including self-occlusions) and cluttered backgrounds, our method still
produces accurate predictions.

#strong[Results on YCB-V Dataset.] As shown in
Tab.~@tab:ycbv_results_table, our framework achieves the best
performance on both the ADD(-S) and the AUC of ADD(-S) metrics, and is
comparable to the state-of-the-art method on the AUC of ADD-S metric,
showing the effectiveness of our method.

== Ablation Studies
<ablation-studies>
#figure(image("fig3.png"),
  caption: [
    #strong[Qualitative results]. Green bounding boxes represent the
    ground-truth poses and blue bounding boxes represent the predicted
    poses of our method. As shown, even facing severe occlusions,
    clutter in the scene or varying environment, our framework can still
    accurately recover the object poses, showing the effectiveness of
    our method for handling the noise and indeterminacy caused by
    various factors in object pose estimation. More qualitative results
    can refer to Supplementary.
  ]
)
<fig:visualization>

We conduct extensive ablation experiments on the LM-O dataset. In these
experiments, we report the model performance on ADD(-S) metric averaged
over all the objects. #strong[More ablation studies can refer to
Supplementary.]

#block[
r0.4

#figure(
  align(center)[#table(
    columns: 2,
    align: (left,center,),
    table.header([Method], [ADD(-S)],),
    table.hline(),
    [Variant A], [49.2],
    [Variant B], [57.3],
    [Variant C], [61.1],
    [6D-Diff], [79.6],
  )]
  , kind: table
  )

<Tab:ablation_study_1>

]
#strong[Impact of denoising process.] In our framework, we predict
keypoints coordinates via performing the denoising process. To evaluate
the efficacy of this process, we test three variants. In the first
variant (#emph[Variant A]), we remove the diffusion model $M_(d i f f)$
and predict keypoints coordinates directly from the heatmaps produced by
the keypoints distribution initializer. The second variant
(#emph[Variant B]) has the same model architecture as our framework, but
the diffusion model is optimized to directly predict the coordinates
instead of learning the reverse process. Same as #emph[Variant B], the
third variant (#emph[Variant C]) is also optimized to directly predict
coordinates without denoising process. For #emph[Variant C], we stack
our diffusion model structure multiple times to produce a deep network,
which has similar computation complexity with our framework. As shown in
Tab.~@Tab:ablation_study_1, compared to our framework, the performance
of these variants significantly drops, showing that the effectiveness of
our framework mainly lies in the designed denoising process.

#block[
r0.4

#figure(
  align(center)[#table(
    columns: 2,
    align: (left,center,),
    table.header([Method], [ADD(-S)],),
    table.hline(),
    [w/o $f_(a p p)$], [74.4],
    [6D-Diff], [79.6],
  )]
  , kind: table
  )

<Tab:ablation_study_4>

]
#strong[Impact of object features $f_(a p p)$.] In our framework, we
send the object features $f_(a p p)$ into the diffusion model
$M_(d i f f)$ to aid the reverse process. To evaluate its effect, we
test a variant in which we do not send $f_(a p p)$ into $M_(d i f f)$
(#emph[w/o $f_(a p p)$]). As shown in Tab.~@Tab:ablation_study_4, our
framework performs better than this variant, showing that $f_(a p p)$
can aid $M_(d i f f)$ to get more accurate predictions.

#block[
r0.6

#figure(
  align(center)[#table(
    columns: 2,
    align: (left,center,),
    table.header([Method], [ADD(-S)],),
    table.hline(),
    [Standard diffusion w/o MoC], [73.1],
    [Heatmaps as condition], [76.2],
    [6D-Diff], [79.6],
  )]
  , kind: table
  )

<Tab:ablation_study_2>

]
#strong[Impact of MoC design.] During training, we model the
distribution $D_K$ from the intermediate representation (heatmaps) as a
MoC distribution $hat(D)_K$, and train the diffusion model $M_(d i f f)$
to perform the reverse process from $hat(D)_K$. To investigate the
impact of this design, we evaluate two variants that train $M_(d i f f)$
in different ways. In the first variant (#emph[Standard diffusion w/o
MoC]), we train the model to start the reverse process from the standard
Gaussian noise, i.e., following the basic forward process in Eq.
[eq:revisiting_3] for model training. In the second variant
(#emph[Heatmaps as condition]), we still train the model to start
denoising from the random Gaussian noise but we use the heatmaps as the
condition for the reverse process. As shown in
Tab.~@Tab:ablation_study_2, our framework consistently outperforms both
variants, showing effectiveness of the designed MoC-based forward
process.

#strong[Runtime analysis.] We test the runtime of our framework on a
desktop with an AMD 3.90GHz CPU and an Nvidia 4090 GPU. The object
detection with FCOS detector [tian2019fcos] takes 16.4 ms. The runtime of
the keypoints distribution initializer is 20.3 ms. Then performing the
reverse diffusion process takes 102.8 ms. Finally, for computing the
object pose based on the prediction of the diffusion model, we use
Progressive-X [barath2019progressive] as the PnP solver and it takes 58.2
ms. In this way, our framework totally needs around 197.7 ms to obtain
the object pose.

= Conclusion
<conclusion>
In this paper, we have proposed a novel diffusion-based 6D object pose
estimation framework, which effectively handles noise and indeterminacy
in object pose estimation. In our framework, we formulate object
keypoints detection as a carefully-designed reverse diffusion process.
We design a novel MoC-based forward process to effectively utilize the
distribution priors in intermediate representations. Our framework
achieves superior performance on two commonly-used benchmarks.
