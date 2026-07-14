We perform this test for all three models: original IPA and FlashIPA trained up
to length 512, and FlashIPA on all data. Similar to the original paper we
sampled 50 structures per length from 100 to 500, and sample 8 inverse folded
sequences to forward fold per structure. All models are evaluated on checkpoint
number 200,000. Fig. @fig-foldflowgen A) shows that the sc-RMSD is lower for
FlashIPA compared to the original IPA trained on the same length-restricted
data. Sc-RMSD is further improved when FlashIPA training is extended to the full
dataset, as expected. We could not assess sc-RMSD for larger structures, as the
ESMFold also depends on IPA and ran out of memory. Overall we conclude that
FlashIPA is more performant and more efficient than IPA. Fig. @fig-foldflowgen
B) shows example structures generated with the full data trained FlashIPA
version.

== FlashIPA trains more efficiently and extends to larger RNAs

We retrained the RNA-FrameFlow model using the code provided by the original
authors. We ingested the same BGSU version 3.382 of the RNASolo2 dataset
@adamczyk2022rnasolo, comprising a total of 14,995 structures (see Appendix
@app-data-rna). First we re-trained RNA-FrameFlow with original and FlashIPA on
all structures within 40 to 150 residue (6,030 structures total), as proposed by
the authors. We kept all hyperparameters consistent with the original model. We
matched the authors' training setup and models were trained on 4 GPUs with DDP
and an effective batch size of $4 times 28$. 4 GPUs are necessary for effective
training with IPA, but with FlashIPA it becomes feasible to run a comparable
training on a single GPU instance. To demonstrate the cost efficiency we also
performed an additional FlashIPA training run on the same data with a batch size
of $512$ on single GPU. All models were trained for a fixed compute time of 20
hours, which resulted in approximately 156k iterations with original IPA,
roughly 230k with FlashIPA on 4 GPUs and 194k with FlashIPA on a single GPU.
During training we found models to converge comparably with overlapping loss
curves, see Appendix @app-losses-rnaframe. We validated the models using the
validity, novelty, and diversity metrics as defined in the original paper, which
uses gRNAde @joshi2025grnade for inverse-folding of the generated structure and
RhoFold @shen2022e2efold for forward-folding. For validity, we report the
average self-consistency TM (sc-TM) score. To do so, we generated 50 structures
per length ranging from 40 to 150 residues, in increments of 10. The results
are presented in Table @tab-rna-frameflow-results and Fig. @fig-rna-flow-length.
We observe comparable scores between all models. In particular, the single-GPU
training matches performance at a quarter of the compute cost than the original.

#figure(
  placement: top,
  table(
    columns: (2.8fr, 1.4fr, 1.4fr, 1.4fr),
    stroke: none,
    inset: (x: 6pt, y: 5pt),
    align: (left, center, center, center),
    table.hline(stroke: 1.5pt),
    [*Model*],
    [*Validity* ($arrow.t$) \ #text(size: 9pt)[(scTM $plus.minus$ std)]],
    [*Diversity* ($arrow.t$) \ #text(size: 9pt)[(qTM cluster)]],
    [*Novelty* ($arrow.b$) \ #text(size: 9pt)[(pdbTM $plus.minus$ std)]],
    table.hline(stroke: 0.5pt),
    [RNA-FrameFlow],
    [$0.42 plus.minus 0.21$], [$0.15$], [$0.81 plus.minus 0.10$],
    [. + FlashIPA (ours)],
    [$0.38 plus.minus 0.20$], [$0.14$], [$0.82 plus.minus 0.10$],
    [. + FlashIPA single GPU \*\* (ours)],
    [$0.41 plus.minus 0.21$], [$0.08$], [$0.77 plus.minus 0.09$],
    [. + FlashIPA \*\* + All data (ours)],
    [$0.36 plus.minus 0.14$], [$0.14$], [$0.74 plus.minus 0.08$],
    table.hline(stroke: 1.5pt),
  ),
  caption: text(size: 9pt)[
    Average validity, diversity, and novelty scores for $600$ generated RNAs of
    length $<= 150$ with RNA-FrameFlow, with and without FlashIPA. FlashIPA
    provides competitive results at a fraction of the cost of an original IPA
    layer. *\*\** indicates that batch size has been increased to match GPU
    memory capacities.
  ],
  kind: table,
) <tab-rna-frameflow-results>

To highlight the advantages of using FlashIPA in the RNA-FrameFlow model, we
analyzed the GPU runtime required to generate RNA backbones based on RNA
sequence length and batch size. The results are in Fig. @fig-rna-flow-scaling.
We observed improvements with FlashIPA compared to the original IPA model,
especially for longer sequences and larger batch sizes. For example it takes 30
times longer to generate an RNA sequence of length 2048 with the original IPA
than with FlashIPA.

#figure(
  placement: top,
  image("flashIPA_RNAflow_efficiency.pdf", width: 100%),
  caption: text(size: 9pt)[
    Scaling of FlashIPA versus IPA for RNA generation using RNA-FrameFlow model,
    with a number of diffusion timestep $N_T = 50$. *[A]* Impact of the
    generated sequence length on the generation runtime, using a batch size of
    $1$. *[B]* Impact of the generated batch size on the generation runtime, for
    generated sequence of length $128$.
  ],
) <fig-rna-flow-scaling>

We also re-trained RNA-FrameFlow with FlashIPA on the full RNASolo dataset
without maximum length restrictions (the longest structures being 4,417
nucleotides) and filtering out structures shorter than $40$ nucleotides. We
trained the model on 4 GPUs for 48 hours, with batch size of $4 times 28$,
resulting in approximately $310$k iterations. In Figure @fig-rna-flow-length, we
present samples of large generated RNA structures with lengths of 2000 and 4000
nucleotides. In comparison, the original RNA-FrameFlow can not be trained or
generate such long sequences. The inverse-forward-folding consistency test cannot
be run for structures of thousands of residues as the validation models (gRNAde
@joshi2025grnade for inverse-folding and RhoFold @shen2022e2efold for
forward-folding) run out of memory at such lengths. However, we qualitatively
observe that the generated structures resemble RNA, we don't necessary suspect
those to be valid, as the amount of training data at such length is still
comparably small.

#figure(
  placement: top,
  image("scTM_length.pdf", width: 100%),
  caption: text(size: 9pt)[
    RNA-FrameFlow generated RNAs results. *[A]* Comparison of the scTM score
    depending on the generated RNA sequence length and the IPA module used. The
    RNA-FrameFlow and RNA-FrameFlow + FlashIPA models are both trained on only
    short sequences $<= 150$, while the All data model has been trained without
    maximum sequence length limit. We don't observe a significant difference
    between the different trained RNA-FrameFlow models. *[B]* Example of short
    generated RNA structures with our FlashIPA RNA-FrameFlow model trained on
    short sequences. *[C]* Example of long generated RNA structures with our
    FlashIPA RNA-FrameFlow model trained on the full dataset.
  ],
) <fig-rna-flow-length>

// ── Section 4 ────────────────────────────────────────────────────────────────
= Discussion

FlashIPA provides memory and wall-clock efficient $op("SE")(3)$ invariant
training on biomolecules and allows for training on structures of thousands of
residues. This approach opens up the possibility of multi-chain complex modeling
in situations constrained by the original IPA module. Our work permit usage of
IPA in contexts where it may have been ruled out due to its scaling limitations,
including representations beyond polymeric backbone that include more atomic
detail.

Efficiency and scalability to long contexts has often been a neglected aspect of
geometric deep learning research and many modules have quadratic to cubic
complexity. An example is triangular attention used in popular models like
AF-3 @abramson2024accurate, Chai-1 @chai2024chai and Boltz-1
@wohlwend2024boltz. Recently, TriFast @trifast was released, which uses fused
triangular attention kernels to reduce IO complexity from cubic to quadratic. We
assume that a factorized version might even achieve a linear scaling.

Most efficient, sub-quadratic models tend not to incorporate geometric inductive
biases. Our work can be seen as a first step at bridging this divide, enabling
models that respect invariances, are cost-effective, and can scale to larger or
more fine-grained biomolecular systems.

== Limitations

FlashIPA relies on factorization of the pair representation, which ultimately is
an approximation. Here we did not find a decrease in performance, but this may
not be guaranteed for more general applications to other forms of more dense pair
representations. Exploring alternative schemes specialized for certain pair
representations (e.g. cross-concatenations, distograms, pair index differences)
may further improve downstream performance.

Despite substantial memory and I/O savings, there are several limitations of
using FlashAttention. First, most current implementations of FlashAttention only
allow for a maximum head dimension of 256. Since our method relies on augmenting
the attention components, this means that we must have
$max(c + 5 N_"query" + r d_z, c + 3 N_"value" + r d_z) <= 256$. However, the
Triton implementation of FlashAttention2 based on AMD CDNA (MI200, MI300) and
RDNA GPUs allows for extending the head dimension to arbitrary size. We expect
these improvements to apply more broadly to a wider class of GPU architectures
in the months to come. Unlocking larger head dimension would allow us to
increase our factorization rank, thereby better approximating dense pair
representations and closing potential gaps against quadratic IPA.

Furthermore, we note that despite achieving $O(L)$ in I/O and memory, the
underlying compute cost is still $O(L^2)$ due to the softmax. Removing the
softmax and using linear attention variants such as Mamba would allow us to
achieve $O(L)$ cost in both compute and memory, and is thus a promising avenue
of future work.

// ── Bibliography ─────────────────────────────────────────────────────────────
#bibliography("literature.bib", style: "ieee", title: "References")

// ── Appendix ─────────────────────────────────────────────────────────────────
#counter(heading).update(0)
#set heading(numbering: "A.1", supplement: none)

= Appendix

== List of biomolecular design models with IPA structure modules <app-ipa-repos>

#block(
  width: 100%,
  stroke: 0.5pt,
  inset: 10pt,
  radius: 2pt,
)[
  #text(size: 9pt)[
    _[Content from ipa\_repos.tex — table of biomolecular design models using
    IPA structure modules]_
  ]
]

== Residue counts of macromolecules in the PDB <app-pdb-counts>

#figure(
  placement: none,
  image("pdb_distribution.pdf", width: 100%),
  caption: text(size: 9pt)[
    Distribution of protein residue counts of the proteins resolved in the PDB
    (Figure reproduced and adapted from the data at RCSB PDB Statistics:
    Sequence length distribution;
    https://www.rcsb.org/stats/distribution-residue-count; accessed 6 May
    2025).
  ],
) <fig-pdb>

== FlashAttention Algorithm <app-flash-attention>

The quadratic scaling of the attention operation is a well-known challenge in
deep learning, because operations are generally I/O-bound on the GPU, with
performance primarily limited by data transfers between the GPU's high-bandwidth
memory (HBM) and its static random access memory (SRAM). I/O reduction is
typically achieved through kernel fusion, which reduces memory traffic by
combining multiple operations into a single CUDA kernel. FlashAttention achieves
kernel fusion via an online and tiled computation of the softmax, which, instead
of materializing the full quadratic $bold(M) = op("softmax")(bold(Q K)^top)$
matrix, performs an equivalent computation by accumulating partial contributions
to the output $bold(Y) = bold(M V)$ one tile at a time
@dao2022flashattention @dao2024flashattention2.

Building on FlashAttention-1, FlashAttention-2 further reduced the number of
non-matmul FLOPs, increased parallelism across thread blocks, and distributed
work between warps to reduce communication through shared memory
@dao2024flashattention2. A good introduction with line-by-line explanations can
also be found here @gordiceli5flashattention.

#block(
  width: 100%,
  stroke: 0.5pt,
  inset: 10pt,
  radius: 2pt,
)[
  #text(size: 9pt)[
    _[Content from flashattention.tex — FlashAttention algorithm pseudocode]_
  ]
]

== FoldFlow training convergence <app-losses-flow>

We provide loss curves for the training of the FoldFlow base model with original
and FlashIPA below. FlashIPA converged slightly faster for the same number of
optimization steps, which is expected from the bigger effective batch size, but
we also found in particular local loss terms, such as the steric clash loss to
decrease noticeably more efficient.

#figure(
  placement: none,
  image("losses.png", width: 100%),
  caption: text(size: 9pt)[Loss behaviour for FoldFlow model training.],
) <app-losses>

== Nucleotide residue counts of RNA structures in the RNASolo2 dataset <app-data-rna>

#figure(
  placement: none,
  image("rnasolodataset.pdf", width: 100%),
  caption: text(size: 9pt)[
    Distribution of nucleotide residue counts of the RNA in the RNASolo2
    dataset, filtering out the short structures of length $< 40$ nucleotides.
    The training cut-off of RNA Flow discards all sequences of length $> 150$,
    accounting for $30%$ of the dataset.
  ],
) <fig-rnasolo2>

== RNA-FrameFlow training convergence <app-losses-rnaframe>

We provide loss curves for the training of the RNA-FrameFlow base model with
original and FlashIPA below. At similar hyperparameters and hardware,
RNA-FrameFlow with and without FlashIPA behaves similarly.

#figure(
  placement: none,
  image("train_frameflow.pdf", width: 70%),
  caption: text(size: 9pt)[Loss behaviour for RNA-FrameFlow model training.],
) <fig-losses-rnaframe>
