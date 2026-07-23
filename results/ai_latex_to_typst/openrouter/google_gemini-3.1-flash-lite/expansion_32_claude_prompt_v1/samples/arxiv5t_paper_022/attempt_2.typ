#set page(paper: "us-letter", margin: (x: 0.75in, y: 1in))
#set text(font: "Times New Roman", size: 10pt)
#set par(justify: true)

#align(center)[
  #text(size: 16pt, weight: "bold")[6D-Diff: A Keypoint Diffusion Framework for 6D Object Pose Estimation] \
  \
  Li Xu#super[1#text(size: 0.7em)[$\dagger$]]#footnote[#text(size: 0.8em)[$\dagger$ Equal contribution; $\ddagger$ Corresponding author]]
  ~~~ Haoxuan Qu#super[1#text(size: 0.7em)[$\dagger$]]
  ~~~ Yujun Cai#super[2]
  ~ Jun Liu#super[1#text(size: 0.7em)[$\ddagger$]] \
  #super[1] Singapore University of Technology and Design \
  #super[2] Nanyang Technological University \
  #text(font: "monospace", size: 9pt)[{li_xu, haoxuan_qu}@mymail.sutd.edu.sg, yujun001@e.ntu.edu.sg, jun_liu@sutd.edu.sg]
]

#block(inset: (x: 2em))[
  #text(weight: "bold")[Abstract] \
  Estimating the 6D object pose from a single RGB image often involves noise and indeterminacy due to challenges such as occlusions and cluttered backgrounds. Meanwhile, diffusion models have shown appealing performance in generating high-quality images from random noise with high indeterminacy through step-by-step denoising. Inspired by their denoising capability, we propose a novel diffusion-based framework (#text(weight: "bold")[6D-Diff]) to handle the noise and indeterminacy in object pose estimation for better performance. In our framework, to establish accurate 2D-3D correspondence, we formulate 2D keypoints detection as a reverse diffusion (denoising) process. To facilitate such a denoising process, we design a Mixture-of-Cauchy-based forward diffusion process and condition the reverse process on the object features. Extensive experiments on the LM-O and YCB-V datasets demonstrate the effectiveness of our framework.
]

#heading(level: 1)[Introduction]
6D object pose estimation aims to estimate the 6D pose of an object including its location and orientation, which has a wide range of applications, such as augmented reality, robotic manipulation, and automatic driving. Recently, various methods have been proposed to conduct RGB-based 6D object pose estimation since RGB images are easy to obtain. Despite the increased efforts, a variety of challenges persist in RGB-based 6D object pose estimation, including occlusions, cluttered backgrounds, and changeable environment. These challenges can introduce significant noise and indeterminacy into the pose estimation process, leading to error-prone predictions.

Meanwhile, diffusion models have achieved appealing results in various generation tasks such as image synthesis and image editing. Specifically, diffusion models are able to recover high-quality determinate samples from a noisy and indeterminate input data distribution via a step-by-step denoising process. Motivated by such a strong denoising capability, we aim to leverage diffusion models to handle the RGB-based 6D object pose estimation task, since this task also involves tackling noise and indeterminacy. However, it can be difficult to directly use diffusion models to estimate the object pose, because diffusion models often start denoising from random Gaussian noise. Meanwhile, in RGB-based 6D object pose estimation, the object pose is often extracted from an intermediate representation, such as keypoint heatmaps, pixel-wise voting vectors, or object surface keypoint features. Such an intermediate representation encodes useful distribution priors about the object pose. Thus starting denoising from such an representation shall effectively assist the diffusion model in recovering accurate object poses. To achieve this, we propose a novel diffusion-based object pose estimation framework (#text(weight: "bold")[6D-Diff]) that can exploit prior distribution knowledge from the intermediate representation for better performance.

#figure(
  image("fig1.png", width: 100%),
  caption: [Overview of our proposed 6D-Diff framework. As shown, given the 3D keypoints from the object 3D CAD model, we aim to detect the corresponding 2D keypoints in the image to obtain the 6D object pose. Note that when detecting keypoints, there are often challenges such as occlusions (including self-occlusions) and cluttered backgrounds that can introduce noise and indeterminacy into the process, impacting the accuracy of pose prediction.]
)

Overall, our framework is a correspondence-based framework, in which to predict an object pose, given the 3D keypoints pre-selected from the object 3D CAD model, we first predict the coordinates of the 2D image keypoints corresponding to the pre-selected 3D keypoints. We then use the 3D keypoints together with the predicted 2D keypoints coordinates to compute the 6D object pose using a Perspective-n-Point (PnP) solver. To predict the 2D keypoints coordinates, we first extract an intermediate representation (the 2D keypoints heatmaps) through a keypoints distribution initializer. As discussed before, due to various factors, there often exists noise and indeterminacy in the keypoints detection process and the extracted heatmaps can be noisy. Thus we pass the distribution modeled from these keypoints heatmaps into a diffusion model to perform the denoising process to obtain the final keypoints coordinates prediction.

#figure(
  image("fig_demo.png", width: 80%),
  caption: [Above we show two examples of keypoint heatmaps, which serve as the intermediate representation in our framework. The red dots indicate the ground-truth locations of the keypoints. As shown above, due to occlusions and cluttered backgrounds, the keypoint heatmaps are noisy, which reflects the noise and indeterminacy during the keypoints detection process.]
)

#figure(
  image("fig2.png", width: 100%),
  caption: [Illustration of our framework. During testing, given an input image, we first crop the Region of Interest (ROI) from the image through an object detector. After that, we feed the cropped ROI to the keypoints distribution initializer to obtain the heatmaps that can provide useful distribution priors about keypoints, to initialize D_K. Meanwhile, we can obtain object features f_app. Next, we pass f_app into the encoder, and the output of the encoder will serve as conditional information to aid the reverse process in the decoder. We sample M sets of 2D keypoints coordinates from D_K, and feed these M sets of coordinates into the decoder to perform the reverse process iteratively together with the step embedding f_D^k. At the final reverse step (K-th step), we average the predictions as the final keypoints coordinates prediction d_0, and use d_0 to compute the 6D pose with the pre-selected 3D keypoints via a PnP solver.]
)

#figure(
  image("fig5.png", width: 90%),
  caption: [Visualization of the denoising process of a sample with our framework. In this example, the target object is the yellow duck and for clarity, we here show three keypoints only. The red dots indicate the ground-truth locations of these three keypoints. The noisy heatmap before denoising reflects that factors like occlusions and clutter in the scene can introduce noise and indeterminacy when detecting keypoints. As shown, our diffusion model can effectively and smoothly reduce the noise and indeterminacy in the initial distribution step by step, finally recovering a high-quality and determinate distribution of keypoints coordinates.]
)

#figure(
  caption: [Comparisons with RGB-based 6D object pose estimation methods on the LM-O dataset. (*) denotes symmetric objects.],
  table(
    columns: 10,
    stroke: none,
    table.header(
      [Method], [ape], [can], [cat], [driller], [duck], [eggbox], [glue], [holepuncher], [Mean],
      table.hline()
    ),
    [Ours], [60.6], [97.9], [63.2], [96.6], [67.2], [73.5], [92.0], [85.5], [79.6]
  )
)

#figure(
  caption: [Comparisons with RGB-based 6D object pose estimation methods on the YCB-V dataset.],
  table(
    columns: 4,
    stroke: none,
    table.header([Method], [ADD(-S)], [AUC of ADD-S], [AUC of ADD(-S)], table.hline()),
    [Ours], [83.8], [91.5], [87.0]
  )
)
