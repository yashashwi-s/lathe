#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.04660_table_3],
  table(
    columns: 9,
    [*Metric (SE)*], [*Action-State-Change*], [*Aesthetic-Quality*], [*Blending-Naturalness*], [*Composition-Interaction*], [*Editing-Artifacts*], [*Image-Quality*], [*Instruction-Following*], [*Local-Attribute*],
    [*Ours (rho)*], [*0.9839*], [*0.9889*], [*0.8866*], [*0.9997*], [*0.9006*], [*0.9033*], [*0.9960*], [*0.9877*],
    [LMM-Baseline (rho)], [0.9769], [-0.0643], [0.8866], [0.9851], [0.8983], [0.4154], [0.9960], [0.9842],
    [*Metric*], [*Non-Edited-Fidelity*], [*Object-Manipulation*], [*Physical-Plausibility*], [*Spatial-Accuracy*], [*Subject-Identity*], [*Text-Content-Style*], [*World-Knowledge*], [*Overall*],
    [*Ours (rho)*], [*0.9019*], [*0.9787*], [*0.8055*], [*0.9303*], [*0.9133*], [*0.9979*], [*0.9628*], [*0.9425*],
    [LMM-Baseline (rho)], [0.7687], [0.9673], [0.6958], [0.9191], [-0.3494], [0.8847], [0.9506], [0.7277],
    [*Metric (ME)*], [*Aesthetic-Quality*], [*Blending-Naturalness*], [*Composition-Interaction*], [*Cross-Source-Attribute*], [*Detail-Fidelity*], [*Image-Quality*], [*Instruction-Following*], [*Inter-Subject-Consistency*],
    [*Ours (rho)*], [*0.9034*], [*0.6177*], [*0.8951*], [*0.9917*], [*0.8767*], [*0.6579*], [*0.9248*], [*0.9469*],
    [LMM-Baseline (rho)], [0.7138], [0.6177], [0.8205], [0.9902], [0.8092], [-0.9202], [0.9248], [0.8293],
    [*Metric*], [*Non-Edited-Fidelity*], [*Physical-Plausibility*], [*Spatial-Accuracy*], [*Subject-Consistency*], [*Subject-Extraction*], [*Text-Content-Style*], [*World-Knowledge*], [*Overall*],
    [*Ours (rho)*], [*0.6459*], [*0.9017*], [*0.9008*], [*0.9401*], [*0.9732*], [*0.9043*], [*0.9523*], [*0.8688*],
    [LMM-Baseline (rho)], [0.5978], [0.8887], [0.8230], [0.6616], [0.7763], [0.8573], [0.8534], [0.6829]
  )
)

#figure(
  caption: [Source table 2: 2512.01096_table_1],
  table(
    columns: 4,
    [*Description*], [*Symbol*], [*Value*], [*Unit*],
    [Bulk Density], [rho], [1.30], [gm/cm3],
    [Viscosity], [eta], [1019], [Pas],
    [Shear Modulus], [G], [2.4], [MPa],
    [Auxin degradation rate], [mu_a], [0.5], [min-1],
    [auxin-TIR1 dissociation rate], [gamma_a], [5], [min-1],
    [auxin-TIR1 binding rate], [beta_a], [0.5], [uM-1 min-1],
    [Maximum mRNA transcription rate], [alpha_m], [0.5], [uM min-1],
    [Ratio of ARF-dependent to ARF2- and double ARF-dependent mRNA transcription rates], [phi_m], [0.1], [-],
    [ARF-DNA binding threshold], [theta_f], [1], [uM],
    [ARF2 binding threshold], [theta_w], [10], [uM],
    [ARF + Aux/IAA-DNA binding threshold], [theta_g], [1], [uM],
    [Double ARF-DNA binding threshold], [psi_f], [0.1], [uM2],
    [ARF-Aux/IAA-DNA binding threshold], [psi_g], [0.1], [uM2],
    [Aux/IAA translation rate], [alpha_r], [5], [min-1],
    [Aux/IAA-auxin-TIR1 binding rate], [beta_r], [5], [uM-1 min-1],
    [Aux/IAA-auxin-TIR1 dissociation rate], [gamma_r], [5], [min-1],
    [ARF-Aux/IAA binding rate], [beta_g], [0.5], [uM-1 min-1],
    [ARF-Aux/IAA dissociation rate], [gamma_g], [5], [min-1],
    [PIN2 translation rate], [alpha_p], [5], [min-1],
    [PIN2-auxin-TIR1 binding rate], [beta_p], [100], [uM-1 min-1],
    [PIN-auxin-TIR1 dissociation rate], [gamma_p], [5], [min-1],
    [PIN decay rate], [mu_p], [5], [min-1],
    [ARF dimerisation rate], [beta_f], [0.5], [uM-1 min-1],
    [ARF2 splitting rate], [gamma_f], [5], [min-1],
    [Aux/IAA decay rate], [mu_r], [5], [min-1],
    [Auxin biosynthesis rate], [alpha_a], [0.5], [uM min-1],
    [AUX1 biosynthesis rate], [alpha_u], [5], [uM min-1],
    [AUX1 degradation rate], [mu_u], [5], [min-1],
    [Rate of AUX1 localisation to membrane], [omega_u], [0.5], [um min-1],
    [Rate of AUX1 dissociation from membrane], [delta_u], [0.05], [min-1],
    [Maximum rate of PIN2 localisation to membrane], [omega_p], [0.5], [um min-1],
    [Rate of PIN2 dissociation from membrane], [delta_p], [0.05], [min-1],
    [Fraction of protonated auxin in cell], [kappa_a_ef], [0.004], [-],
    [Fraction of protonated auxin in wall], [kappa_a_in], [0.24], [-],
    [Effective PIN2-induced auxin efflux], [kappa_p_ef], [4.67], [-],
    [Effective AUX1-induced auxin influx], [kappa_u_in], [3.56], [-],
    [Auxin membrane permeability], [phi_a], [0.55], [um min-1],
    [PIN2-induced auxin membrane permeability], [tilde_phi_p], [0.27], [um uM-1 min-1],
    [AUX1-induced auxin membrane permeability], [tilde_phi_u], [0.55], [um uM-1 min-1],
    [Rate of auxin diffusion in apoplast], [phi_A], [67], [um min-1],
    [Sensitivity of PIN2 localisation to auxin flux], [h], [50], [-],
    [Auxin flux threshold], [theta], [2], [-]
  )
)
