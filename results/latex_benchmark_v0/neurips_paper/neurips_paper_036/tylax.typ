#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Flash Invariant Point Attention",
  author: "tabular{c} Andrew Liu, Axel Elaldi, Nicholas T. Franklin, Nathan Russell,  Gurinder S. Atwal, Yih-En A. Ban & Olivia Viessmann [2ex] Flagship Pioneering  55 Cambridge Parkway,  Cambridge, MA 02142, United States tabular",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Flash Invariant Point Attention]

  #text(size: 1.2em)[tabular{c} Andrew Liu, Axel Elaldi, Nicholas T. Franklin, Nathan Russell,  Gurinder S. Atwal, Yih-En A. Ban & Olivia Viessmann [2ex] Flagship Pioneering  55 Cambridge Parkway,  Cambridge, MA 02142, United States tabular]
]

/* \newcolumntype */

 /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   Invariant Point Attention (IPA) is a key algorithm for geometry-aware modeling in structural biology, central to many protein and RNA models. However, its quadratic complexity limits the input sequence length. We introduce FlashIPA, a factorized reformulation of IPA that leverages hardware-efficient FlashAttention to achieve linear scaling in GPU memory and wall-clock time with sequence length. FlashIPA matches or exceeds standard IPA performance while substantially reducing computational costs. FlashIPA extends training to previously unattainable lengths, and we demonstrate this by re-training generative models without length restrictions and generating structures of thousands of residues. FlashIPA is available at #link("https://github.com/flagshippioneering/flash_ipa").
]

== Introduction
 Invariant Point Attention, IPA, is a geometry-aware attention operation that has been the workhorse of generative structural design models for proteins and RNA, initially popularized by Alphafold2 #cite(<jumper2021highly>) and AlphaFold-Multimer #cite(<evans2021protein>), and subsequently widely adopted across structural biology modeling. Amongst them are structure prediction models like OpenFold and ESMFold for proteins #cite(<ahdritz2024openfold>, <lin2022language>), RhoFold for RNA #cite(<shen2024accurate>), generative protein backbone models such as FrameDiff#cite(<yim2023>), FrameFlow #cite(<yim2024>, <yim2023flow>), the FoldFlow family #cite(<huguet2024sequence>, <bose2024se3>), FrameDiPT #cite(<Zhang2023.11.21.568057>), Proteus #cite(<wang2024proteus>), FADiff #cite(<liu2024floating>), Genie #cite(<lin2023generating>), IgDiff #cite(<cutting2024novo>), GAFL #cite(<wagnerseute2024gafl>), P2DFlow #cite(<jin2025p2dflow>), RNA generative models such as RNA-FrameFlow #cite(<anand2024rnaframeflow>), and scoring models like lociPARSE #cite(<tarafder2024lociparse>). A list of models that rely on IPA for their structure modeling is provided in Appendix [app-ipa-repos.] The advantage of IPA is its roto-translational ($S E(3)$) invariant representation of the molecular structure, enforcing the idea that rotations and translations of a molecule results in an equivalent structure prediction. This inductive geometric bias accelerates training and improves performance in limited data settings, as is the case for structurally resolved biomolecules. IPA's quadratic scaling ($O(L^(2))$) limits its scalability, rapidly exhausting GPU memory when modeling longer biomolecules. As of May 2025, 42% of structures within the PDB have more than 512 residues, and 33% with more than 756 and 23% with more than 1024 (see Appendix @app-pdb-counts). Most trainings across the literature reduce their data to chains and cropped structures below 512 residues. Despite this, they still commonly run on costly multi-GPU setups with trainings that span from days up to a month #cite(<shen2024accurate>, <yim2023>).

 Such engineering compromises, namely truncating biologically relevant lengths, limiting dataset sizes, and relying on expensive computational infrastructure, restrict the progress of the field.  In this work, we propose a recasting of the original IPA algorithm to a simple attention form to leverage off-the shelf I/O reduction methods like FlashAttention, which replace the quadratic $O(L^(2))$ with an effective linear $O(L)$ scaling behavior. We show empirically that FlashIPA exceeds the validation performance of IPA in benchmarking models and datasets. We then demonstrate the memory and compute time efficiency by retraining benchmarking models more efficiently and without length restrictions on the data.

 We provide FlashIPA as an importable uv package at #link("https://github.com/flagshippioneering/flash_ipa") with an API similar to existing repositories using IPA to facilitate drop-in usage.

== Preliminaries
 Introduced by AlphaFold2 #cite(<jumper2021highly>), IPA is a specialized attention mechanism designed to preserve 3D geometric relationships directly in transformer-based models for structural biology applications. IPA enforces invariance under 3D rotations and translations by utilizing a learnable local coordinate frame representation for each residue (point) within proteins and RNAs.

 Formally, a function $f : cal(X) -> cal(Y) $ is  invariant to transformations in the abstract group $G $ if $f(g dot x) = f(x)$ for all $g in G $. This differs from  equivariance to $G $, where the transformations of the group commute with $f $, or $f(g dot x) = g dot f(x)$ for all $g in G $. Here, we are concerned with the transformations $T $ (referred to as _"frames"_) in the special Euclidean group SE(3), a continuous group of rigid transformations that includes rotations and translations, but not reflections. Intuitively, the output of an SE(3)-invariant function does not change under rotations and translations, which is desirable for biomolecular structures, that do not change function under those transformations.

=== Frame representations for proteins and RNA
 /* Begin wrapfigure */
r0.28/* \textwidth */  #image("frame.pdf", width: 28%) [ The protein backbone frame: The $C_(alpha)$ is the centre. The vectors spanning $C_(alpha)- N$ and $C alpha - C$ define the third axis via Gram–Schmidt. The oxygen atom $O$ is parameterized via the torsion angle $psi$ around the $C_(alpha)- C$ axis.] <fig-frame>
/* End wrapfigure */
 Meaningful frames for biomolecules are commonly defined on the backbone structures. In proteins, each residue frame is typically determined by three of the four atoms from the backbone, namely the alpha carbon ($C_(alpha)$), nitrogen ($N $), and carbon ($C $), with $C_(alpha)$ at the origin (Figure @fig-frame). The frame transformation $T $ maps the standard positions of these backbone atoms into their actual positions in global coordinates: $[N, C, C_(alpha), O ] = T dot[N ',C ', C_(alpha)', O ']$. The frame has a rotation and translation component $T =(R,t)$. The rotation component of the transformation, $R $, is computed using Gram–Schmidt ortho-normalization on vectors formed by $C_(alpha)- N $ and $C_(alpha)- C $ bonds, while the position of the oxygen ($O $) is captured by the torsion angle around the $C_(alpha)- C $ bond.

 For RNA, the backbone structure involves 13 atoms per nucleotide, leading to more complex flexibility. RNA-FrameFlow #cite(<anand2024rnaframeflow>), define RNA frames using the atoms $C 3 '$, $C 4 '$, and $O 4 '$, identified as the least variable backbone positions. The rest of the RNA backbone geometry can then be parameterized efficiently through a set of eight torsion angles.

=== IPA algorithm
 The IPA algorithm is a 1D sequence-to-sequence transformation. It transforms an input sequence representation $s_(i)$, local frames $T_(i)$, and pair representations $z_(i j)$ (with sequence indices $i,j in 1,. . .,L $) into an output sequence $tilde(s)_(i)$. Each attention head, indexed by $h in 1,. . .,H $, involves linear transformations of the input sequence to produce scalar queries, keys, values ($upright(bold(q))_(i)^(h), upright(bold(k))_(i)^(h), upright(bold(v))_(i)^(h) in RR^(c)$) and Euclidean (geometric) counterparts ($arrow(upright(bold(q)))_(i)^(h p), arrow(upright(bold(k)))_(i)^(h p), arrow(upright(bold(v)))_(i)^(h p) in RR^(3)$). Additionally, the pair representation $upright(bold(z))_(i j) in RR^(L times L times d_(z))$ contributes to a bias term $b_(i j)^(h)$ through a linear projection: $  "Single rep:" quad upright(bold(q))_(i)^(h), arrow(upright(bold(q)))_(i)^(h p), upright(bold(k))_(i)^(h), arrow(upright(bold(k)))_(i)^(h p), upright(bold(v))_(i)^(h), arrow(upright(bold(v)))_(i)^(h p) <- "Linear"(upright(bold(s))_(i)) wide wide wide wide wide wide wide wide wide wide wide wide  $ <components>
 $  "Pair rep.(bias term):" quad b_(i j)^(h) <- "Linear"(upright(bold(z))_(i j)) wide wide wide wide wide wide wide wide wide wide wide wide wide wide thin  $ <pair>
 $  "IPA update:" quad a_(i j)^(h) = "softmax"_(j) underbrace((w_(L)(frac(1, sqrt(c)) upright(bold(q))_(i)^(h)^(top) upright(bold(k))_(j)^(h) + b_(i j)^(h) - frac(gamma^(h) w_(C), 2) sum_(p) norm(T_(i)circle.small arrow(upright(bold(q)))_(i)^(h p) - T_(j)circle.small arrow(upright(bold(k)))_(j)^(h p))^(2)_(2))))_(O(L^(2))) wide wide wide wide quad  $ <update>
 $  "Attention aggregation:" quad tilde(upright(bold(o)))_(i)^(h) = sum_(j)a_(i j)^(h)upright(bold(z))_(i j), quad upright(bold(o))_(i)^(h) = sum_(j)a_(i j)^(h)upright(bold(v))_(j)^(h), quad arrow(upright(bold(o)))_(i)^(h p) = T_(i)^(- 1) circle.small sum_(j)a_(i j)^(h)(T_(j) circle.small arrow(upright(bold(v)))_(j)^(h p)) wide wide wide wide  $
 $  "Concat, project, return:" quad upright(bold(tilde(s)))_(i) = "Linear"("concat"_(h,p)(tilde(upright(bold(o)))_(i)^(h), upright(bold(o))_(i)^(h), arrow(upright(bold(o)))_(i)^(h p), norm(arrow(upright(bold(o)))_(i)^(h p))_(2))) wide wide quad wide quad wide wide wide wide  $

 The proof of SE(3) invariance of the IPA transformation can be found in the appendix of AlphaFold2 #cite(<jumper2021highly>). This form of IPA incurs $O(L^(2))$ compute and memory complexity due to the explicit materialization of the quadratic attention matrix in equation [update.]

=== FlashAttention and I/O reduction algorithms
 FlashAttention #cite(<dao2022flashattention>, <dao2024flashattention2>) addresses the quadratic complexity of attention mechanisms of the form $upright(bold(q^(top))) upright(bold(k)) $. It significantly reduces GPU high bandwidth memory (HBM) and I/O bottlenecks by avoiding materializing the full $O(L^(2))$ attention matrix, by employing a fused, tiled kernel computation and performing computations in an online fashion with linear $O(L)$ memory complexity. This technique substantially improves scalability and performance for transformer-based models. We provide a brief review of the algorithm in appendix [app-flash-attention.]

=== FlashIPA: combining geometry-awareness and efficiency
 Our efficiency gains come from expressing the entire IPA update in a form that is amenable to FlashAttention (i.e. a factorized version of form $upright(bold(q^(top))) upright(bold(k)) $), which then computes the attention update without materializing any quadratic attention matrix. To do so, we rewrite the softmax argument in the IPA update (eq. [eq-update]) as a single inner product. We also need to parameterize the pair representation (bias term eq. [eq-pair]) $upright(bold(z))_(i j)in ensuremathRR^(L times L times d_(z))$ in a factorized form $upright(bold(z))_(i j)= upright(bold(z))^(1 thin top)_(i) upright(bold(z))^(2)_(j)$, where $upright(bold(z))^(1)_(i), upright(bold(z))^(2)_(j) in ensuremathRR^(L times r times d_(z))$. Here, $r $ can be interpreted as the "rank" of the factorization, and is the dimension on which we perform the contraction. We then expand the sum of squared norms in the third term of eq. [eq-update] and collect terms, resulting in an equivalent update rule, given in Algorithm [alg-ipa-flash.] Note that factorizing $upright(bold(z))_(i j)$ allows not only for combining the softmax terms, but also allows us to compute the pair representation part of the attention as $tilde(upright(bold(o)))_(i)^(h)= sum_(j)a_(i j)upright(bold(z))_(i j)= upright(bold(z))_(i)^(1 thin top)(sum_(j)a_(i j)upright(bold(z))_(j)^(2)) $, avoiding materializing any quadratic object. As a result, the attention components from eq. [eq-components] are lifted to $hat(upright(bold(q)))_(i)^(h), hat(upright(bold(k)))_(j)^(h) in ensuremathRR^(c + 5 N_(q u e r y)+ r d_(z)), hat(upright(bold(v)))_(i)^(h) in ensuremathRR^(c + 3 N_(v a l u e)+ r d_(z))$. Regular attention is then computed on the lifted components.

 With the new update in the form of regular attention, we then leverage FlashAttention to perform the computation. This leads to significant speedups in wall-clock time and since the online computation of FlashAttention avoids materializing the quadratic attention matrix, we only need to store the queries, keys, and values in the GPU's HBM, incurring only $O(L)$ memory.

=== Factorizing the pair representation
 General forms of pair representations $upright(bold(z))_(i j)$ typically involve quadratic complexity and are not inherently decomposable. However, common implementations of IPA often compute these quadratic representations from components that intrinsically scale linearly, implying redundancy in the resulting quadratic tensor $upright(bold(z))_(i j)$ (eq. [eq-pair]). This suggests that pair representations can be efficiently approximated through low-rank factorization in latent space. This motivates a simplified factorization strategy for initializing and updating $upright(bold(z))_(i j)$. Instead of explicitly constructing and storing a full quadratic tensor of shape batch, length $times $ length, latent dimension ($(B,L,L,d)$), we represent each feature (e.g., positional encodings, distograms, diffusion time embeddings in generative models, a.s.o.) using two lower-dimensional tensors (pseudo-factors) each of shape $(B,L,r,d)$, obtained via linear projections. We show empirically that this parametrization, despite relaxing certain inductive biases, recovers downstream performance with substantially lower memory consumption. /* \input */flash_(i)pa

 In many structure models $upright(bold(z))_(i j)$ is updated multiple times by a non-linear EdgeTransition module that is not part of IPA. Because of that each factor is usually highly non-linear with respect to the input, despite the low-dimensional contraction.  Thus, we still retain substantial representation power with this factorization. The benefits of highly nonlinear low-dimensional factors is well motivated in the literature: Instead of large head dimensions and linear factors, i.e. $q,k = "Linear"(X) $, as is the case for transformers, many state space models, such as Mamba #cite(<gu2023mamba>) use factors that are non-linear transformations of the input (e.g. $q,k = "Swish"("Conv1d"(X)) $, and much smaller contraction dimensions (often $r = 1 6 $).

 We also note that most implementations of IPA rely on pair representations $upright(bold(z))_(i j)$ that depend on distograms computed from pairwise distances. To simultaneously ensure invariance and avoid computing activations on the full distogram, we only keep the distances of the $k $ nearest neighbors $(B,L,k,n_(b i n s))$ instead of $(B,L,L,n_(b i n s))$. We keep track of neighbor identities by applying positional encodings on their indices. Emphasizing nearest neighbor distances is also motivated by the fact that local geometry (e.g. chemical bonds) is more important than global geometry when it comes to validity of biomolecular structures. We surmise that in future work it may be beneficial to compress all $frac(L(L - 1), 2)$ distances into factors without materializing the pairwise matrix, in a manner similar to FlashAttention.

== Experiments

=== FlashIPA is SE(3) invariant and scales linearly
 We tested the SE(3)-invariance by applying random roto-translations to input Gaussian point clouds and measuring the output deviation after applying a single layer of the original IPA and FlashIPA. Original IPA output deviation was $< 1 0^(- 6)$ and FlashIPA $< 1 0^(- 3)$.  We evaluate the scaling behavior in GPU memory and wall-clock time by passing single-sample batches of increasing lengths $L $ through original and FlashIPA, see Fig. [fig-scaling.] We use a polynomial fit (green and red dotted lines), and find an approixmate GPU memory scaling for FlashIPA of $y thin "MB" = - 7 dot 1 0^(- 1 2)dot L^(2) + 7 . 5 dot 1 0^(- 2) dot L $ versus original IPA $y thin "MB" = 2 . 4 times 1 0^(- 3)dot L^(2) + 1 . 4 dot 1 0^(- 2) dot L $.
#figure(
  image("flashPA_efficiency.pdf"),
  caption: [ Scaling as a function of input sequence length on a single-sample batch forward pass. *[A]* GPU memory usage in GB. Original IPA scaled approximately quadratically with sequence length ($y thin "MB" = 2 . 4 times 1 0^(- 3)dot L^(2) + 1 . 4 dot 1 0^(- 2) dot L$), FlashIPA follows a linear trend ($y thin "MB" = - 7 dot 1 0^(- 1 2)dot L^(2) + 7 . 5 dot 1 0^(- 2) dot L$). *[B]* Wall-clock time in seconds.],
) <fig-scaling>

=== Integration test with external repositories
 We selected two recent model approaches where code and data were available for retraining of the original model and allowed for FlashIPA insertion. We chose FoldFlow #cite(<bose2024se3>) for proteins and RNA-FrameFlow #cite(<anand2024rnaframeflow>) for RNAs, both are flow-matching generative backbone models. All experiments were run on L40S GPU instances with 48 GB HBM memory. FlashIPA hyperparameters were matched to the IPA parameters chosen by the original authors (embedding sizes, hidden dimensions, number of heads, etc.). For the factorization of the pair representation we tested $"rank" in {1,2 }$, and found rank 2 and pair-wise distograms with $k = 2 0 $ to match and partially surpass the loss convergence of original IPA.

=== FlashIPA improves performance and extends to larger proteins
 We retrained the FoldFlow Base model in its original form with IPA and with FlashIPA.  We reran the PDB data pre-processing pipeline by the authors, which yielded a total of 40,492 single-chain protein monomers for training. The original training used a maximum length cut-off of 512 residues, which results in a 10% reduction of the training data to 36,600 structures. We match the training strategy of the original authors and train on this reduced dataset on 4 GPUs with DDP. We kept model and train parameters identical to the published values of the authors, however for the FlashIPA version we had to make two adjustments: The original repository runs 4 blocks of IPA with a hidden dimension of 256. FlashAttention becomes incompatible with DDP at that dimension, so we reduced FlashIPA hidden dimension to 128 and used 5 blocks (instead of 4) to match model parameter sizes (17.4M versus 17.1M, theirs versus ours). To keep memory consumption at an efficient constant level, the original implementation heuristically chose an effective batch size according to the quadratic rule $"eff"_(b s) = max[ r o u n d(frac(5 0 0 . 0 0 0 thin times thin n_(G P U s), "\textbfN"^("\textbf2"))), 1 ] $, which kept GPU memory at approximately 90% throughout training. For FlashIPA we were able to achieve a linear effective batch size $ "eff"_(b s) = max[ r o u n d(frac(2 0 . 0 0 0 thin times thin n_(G P U s), "\textbfN")), 1 ] $ that resulted in similar memory consumption. For example IPA only has a batch size of 1 for a protein of length 512, whereas FlashIPA can batch together 39 samples.  We found that FlashIPA converged slightly faster than IPA as expected with larger batch size, but we also compared partial loss terms, and found that particularly the number of steric clashes reduced faster for FlashIPA (we provide loss curves in the Appendix @app-losses-flow). This suggests that our local k-nearest neighbour distogram emphasis is more efficient at capturing local geometry.
#figure(
  image("foldflow_gen.png"),
  caption: [ FoldFlow self-consistency validation after 200k optimization steps. A) The sc-RMSD of the FlashIPA (red, green) models is consistent or better than the original IPA model (blue). Extending training to larger structures with FlashIPA further improves sc-RMSD. B) Three exemplar generated backbone structures with FoldFlow FlashIPA. *ESMFold gets out of memory for lengths beyond 500+ residues and sc-RMSD could not be assessed.],
) <fig-foldflowgen>
 To demonstrate the immediate enablement of linear scaling we ran one additional training with FlashIPA on the entire monomer dataset without length restrictions. The largest chain in the dataset is 8.8k residues.  We follow the original authors' validation test that generates structures at varying lengths, subsequently inverse folds with Protein-MPNN #cite(<dauparas2022robust>) and forward-folds with ESMFold #cite(<lin2022language>). The resulting self-consistency RMSD (sc-RMDS) is a proxy for generation fidelity. We perform this test for all three models: original IPA and FlashIPA trained up to length 512, and FlashIPA on all data. Similar to the original paper we sampled 50 structures per length from 100 to 500, and sample 8 inverse folded sequences to forward fold per strucutre. All models are evaluated on checkpoint number 200,000. Fig. @fig-foldflowgen A) shows that the sc-RMSD is lower for FlashIPA compared to the original IPA trained on the same length-restricted data. Sc-RMSD is further improved when FlashIPA training is extended to the full dataset, as expected. We could not assess sc-RMSF for larger structures, as the ESMFold also depends on IPA and ran out of memory. Overall we conclude that FlashIPA is more performant and more efficient than IPA. Fig. @fig-foldflowgen B) shows example structures generated with the full data trained FlashIPA version.

=== FlashIPA trains more efficiently and extends to larger RNAs
 We retrained the RNA-FrameFlow model using the code provided by the original authors. We ingested the same BGSU version 3.382 of the RNASolo2 dataset #cite(<adamczyk2022rnasolo>), comprising a total of 14,995 structures (see Appendix @app-data-rna). First we re-trained RNA-FrameFlow with original and FlashIPA on all structures within 40 to 150 residue (6,030 structures total), as proposed by the authors. We kept all hyperparameters consistent with the original model. We matched the authors' training setup and models were trained on 4 GPUs with DDP and an effective batch size of $4 times 2 8 $. 4 GPUs are necessary for effective training with IPA, but with FlashIPA it becomes feasible to run a comparable training on a single GPU instance. To demonstrate the cost efficiency we also performed an additional FlashIPA training run on the same data with a batch size of $5 1 2 $ on single GPU. All models were trained for a fixed compute time of 20 hours, which resulted in approximately 156k iterations with original IPA, roughly 230k with FlashIPA on 4GPUs and 194k with FlashIPA on a single GPU. During training we found models to converge comparably with overlapping loss curves, see Appendix [app-losses-rnaframe.] We validated the models using the validity, novelty, and diversity metrics as defined in the original paper, which uses gRNAde #cite(<joshi2025grnade>) for inverse-folding of the generated structure and RhoFold #cite(<shen2022e2efold>) for forward-folding. For validity, we report the average self-consistency TM (sc-TM) score. To do so, we generated 50 structures per length ranging from 40 to 150 residues, in increments of 10. The results are presented in Table @tab-rna-frameflow-results and Fig. [fig-rna-flow-length.] We observe comparable scores between all models. In particular, the single-GPU training matches performance at a quarter of the compute cost than the original.

#figure(
  caption: [ Average validity, diversity, and novelty scores for $6 0 0$ generated RNAs of length $<= 1 5 0$ with RNA-FrameFlow, with and without FlashIPA. FlashIPA provides competitive results at a fraction of the cost of an original IPA layer. **** indicates that batch size has been increased to match GPU memory capacities.],
)[
#table(
    columns: (auto, auto, auto, auto),
    align: (left, center, center, center),
    table.hline(),
    [*Model*], [*Validity* ($arrow.t $)], [*Diversity* ($arrow.t $)], [*Novelty* ($arrow.b $)],
    [], [(scTM $plus.minus $ std)], [(qTM cluster)], [(pdbTM $plus.minus $ std)],
    table.hline(),
    [RNA-FrameFlow], [$0 . 4 2 plus.minus 0 . 2 1 $], [$0 . 1 5 $], [$0 . 8 1 plus.minus 0 . 1 0 $],
    [. + FlashIPA (ours)], [$0 . 3 8 plus.minus 0 . 2 0 $], [$0 . 1 4 $], [$0 . 8 2 plus.minus 0 . 1 0 $],
    [. + FlashIPA single GPU *\*\** (ours)], [$0 . 4 1 plus.minus 0 . 2 1 $], [$0 . 0 8 $], [$0 . 7 7 plus.minus 0 . 0 9 $],
    [. + FlashIPA *\*\** + All data (ours)], [$0 . 3 6 plus.minus 0 . 1 4 $], [$0 . 1 4 $], [$0 . 7 4 plus.minus 0 . 0 8 $],
    table.hline(),
)

] <tab-rna-frameflow-results>

 To highlight the advantages of using FlashIPA in the RNA-FrameFlow model, we analyzed the GPU runtime required to generate RNA backbones based on RNA sequence length and batch size. The results are in Fig. [fig-rna-flow-scaling.] We observed improvements with FlashIPA compared to the original IPA model, especially for longer sequences and larger batch sizes. For example it takes 30 times longer to generate an RNA sequence of length 2048 with the original IPA than with FlashIPA.
#figure(
  image("flashIPA_RNAflow_efficiency.pdf"),
  caption: [ Scaling of FlashIPA versus IPA for RNA generation using RNA-FrameFlow model, with a number of diffusion timestep $N_(T)$ = 50. *[A]* Impact of the generated sequence length on the generation runtime, using a batch size of $1$. *[B]* Impact of the generated batch size on the generation runtime, for generated sequence of length $1 2 8$.],
) <fig-rna-flow-scaling>

 We also re-trained RNA-FrameFlow with FlashIPA on the full RNASolo dataset without maximum length restrictions (the longest structures being 4,417 nucleotides) and filtering out structures shorter than $4 0 $ nucleotides. We trained the model on 4 GPUs for 48 hours, with batch size of $4 times 2 8 $, resulting in approximately $3 1 0 $k iterations. In Figure @fig-rna-flow-length, we present samples of large generated RNA structures with lengths of 2000 and 4000 nucleotides. In comparison, the original RNA-FrameFlow can not be trained or generate such long sequences. The inverse-forward-folding consistency test cannot be run for structures of thousands of residues as the validation models (gRNAde #cite(<joshi2025grnade>) for inverse-folding and RhoFold #cite(<shen2022e2efold>) for forward-folding) run out of memory at such lengths. However, we qualitatively observe that the generated structures resemble RNA, we don't necessary suspect those to be valid, as the amount of training data at such length is still comparably small.

#figure(
  image("scTM_length.pdf"),
  caption: [ RNA-FrameFlow generated RNAs results. *[A]* Comparison of the scTM score depending on the generated RNA sequence length and the IPA module used. The RNA-FrameFlow and RNA-FrameFlow + FlashIPA models are both trained on only short sequences $<= 1 5 0$, while the All data model has been trained without maximum sequence lenghth limit. We don't observe a significant difference between the different trained RNA-FrameFlow models. *[B]* Example of short generated RNA structures with our FlashIPA RNA-FrameFlow model trained on short sequences. *[C]* Example of long generated RNA structured with our FlashIPA RNA-FrameFlow model trained on the full dataset.],
) <fig-rna-flow-length>

== Discussion
 FlashIPA provides memory and wall-clock efficient $S E(3)$ invariant training on biomolecules and allows for training on structures of thousands of residues. This approach opens up the possibility of multi-chain complex modeling in situations constrained by the original IPA module. Our work permit usage of IPA in contexts where it may have been ruled out due to its scaling limitations, including representations beyond polymeric backbone that include more atomic detail.

 Efficiency and scalability to long contexts has often been a neglected aspect of geometric deep learning research and many modules have quadratic to cubic complexity. An example is triangular attention used in popular models like AF-3#cite(<abramson2024accurate>), Chai-1#cite(<chai2024chai>) and Boltz-1 #cite(<wohlwend2024boltz>). Recently, TriFast #cite(<trifast>) was released, which uses fused triangular attention kernels to reduce IO complexity from cubic to quadratic. We assume that a factorized version might even achieve a linear scaling.  Most efficient, sub-quadratic models tend not to incorporate geometric inductive biases. Our work can be seen as a first step at bridging this divide, enabling models that respect invariances, are cost-effective, and can scale to larger or more fine-grained biomolecular systems.

=== Limitations

 FlashIPA relies on factorization of the pair representation, which ultimately is an approximation. Here we did not find a decrease in performance, but this may not be guaranteed for more general applications to other forms of more dense pair representations. Exploring alternative schemes specialized for certain pair representations (e.g. cross-concatenations, distograms, pair index differences) may further improve downstream performance.

 Despite substantial memory and I/O savings, there are several limitations of using FlashAttention. First, most current implementations of FlashAttention only allow for a maximum head dimension of 256. Since our method relies on augmenting the attention components, this means that we must have $max(c + 5 N_(q u e r y)+ r d_(z), c + 3 N_(v a l u e)+ r d_(z))<= 2 5 6 $. However, the Triton implementation of FlashAttention2 based on AMD CDNA (MI200, MI300) and RDNA GPUs allows for extending the head dimension to arbitrary size. We expect these improvements to apply more broadly to a wider class of GPU architectures in the months to come. Unlocking larger head dimension would allow us to increase our factorization rank, thereby better approximating dense pair representations and closing potential gaps against quadratic IPA.

 Furthermore, we note that despite achieving $O(L)$ in I/O and memory, the underlying compute cost is still $O(L^(2))$ due to the softmax. Removing the softmax and using linear attention variants such as Mamba would allow us to achieve $O(L)$ cost in both compute and memory, and is thus a promising avenue of future work.

 /* \bibliographystyle */unsrt /* \bibliography */literature

// Appendix
#counter(heading).update(0)
#set heading(numbering: "A.")

== Appendix

=== List of biomolecular design models with IPA structure modules
 <app-ipa-repos> /* \input */ipa_(r)epos

=== Residue counts of macromolecules in the PDB
 <app-pdb-counts>
#figure(
  image("pdb_distribution.pdf"),
  caption: [ Distribution of protein residue counts of the proteins resolved in the PDB (Figure reproduced and adapted from the data at RCSB PDB Statistics: Sequence length distribution; https://www.rcsb.org/stats/distribution-residue-count; accessed 6 May 2025).],
) <fig-pdb>

=== FlashAttention Algorithm
 <app-flash-attention> The quadratic scaling of the attention operation is a well-known challenge in deep learning, because operations are generally I/O-bound on the GPU, with performance primarily limited by data transfers between the GPU's high-bandwidth memory (HBM) and its static random access memory (SRAM). I/O reduction is typically achieved through kernel fusion, which reduces memory traffic by combining multiple operations into a single CUDA kernel. FlashAttention achieves kernel fusion via an online and tiled computation of the softmax, which, instead of materializing the full quadratic $upright(bold(M)) = "softmax"(upright(bold(Q K))^(top)) $ matrix, performs an equivalent computation by accumulating partial contributions to the output $upright(bold(Y)) = upright(bold(M V)) $ one tile at a time #cite(<dao2022flashattention>, <dao2024flashattention2>). Building on FlashAttention-1, FlashAttention-2 further reduced the number of non-matmul FLOPs, increased parallelism across thread blocks, and distributed work between warps to reduce communication through shared memory #cite(<dao2024flashattention2>). A good introduction with line-by-line explanations can also be found here #cite(<gordiceli5flashattention>). /* \input */flashattention

=== FoldFlow training convergence
 <app-losses-flow> We provide loss curves for the training of the FoldFlow base model with original and FlashIPA below. FlashIPA converged slightly faster for the same number of optimization steps, which is expected from the bigger effective batch size, but we also found in particular local loss terms, such as the steric clash loss to decrease noticably more efficient.
#figure(
  image("losses.png"),
  caption: [ Loss behaviour for FoldFlow model training.],
) <app-losses>

=== Nucleotide residue counts of RNA structures in the RNASolo2 dataset.
 <app-data-rna>
#figure(
  image("rnasolodataset.pdf"),
  caption: [ Distribution of nucleotide residue counts of the RNA in the RNASolo2 dataset, filtering out the short structures of length $< 4 0$ nucleotides. The training cut-off of RNA Flow discards all sequences of length $> 1 5 0$, accounting for $3 0 %$ of the dataset.],
) <fig-rnasolo2>

=== RNA-FrameFlow training convergence
 <app-losses-rnaframe> We provide loss curves for the training of the RNA-FrameFlow base model with original and FlashIPA below. At similar hyperparameters and hardware, RNA-FrameFLow with and without FlashIPA behaves similarly.
#figure(
  image("train_frameflow.pdf"),
  caption: [ Loss behaviour for RNA-FrameFlow model training.],
) <fig-losses-rnaframe>

