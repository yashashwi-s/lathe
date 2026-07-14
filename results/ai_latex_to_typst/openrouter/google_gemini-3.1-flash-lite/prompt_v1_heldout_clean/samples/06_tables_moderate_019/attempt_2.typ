#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Moderate Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.04660_table_3],
  table(
    columns: 9,
    stroke: none,
    align: center + horizon,
    table.hline(y: 0, stroke: 0.8pt),
    table.hline(y: 1, stroke: 0.5pt),
    table.hline(y: 3, stroke: 0.5pt),
    table.hline(y: 4, stroke: 0.5pt),
    table.hline(y: 6, stroke: 0.5pt),
    table.hline(y: 7, stroke: 0.5pt),
    table.hline(y: 9, stroke: 0.5pt),
    table.hline(y: 10, stroke: 0.5pt),
    table.hline(y: 12, stroke: 0.8pt),
    [*Metric (SE)*], [Action-\nState-Change], [Aesthetic-\nQuality], [Blending-\nNaturalness], [Composition-\nInteraction], [Editing-\nArtifacts], [Image-\nQuality], [Instruction-\nFollowing], [Local-\nAttribute],
    [*Ours* ($rho$)], [*0.9839*], [*0.9889*], [*0.8866*], [*0.9997*], [*0.9006*], [*0.9033*], [*0.9960*], [*0.9877*],
    [LMM-Baseline ($rho$)], [0.9769], [-0.0643], [0.8866], [0.9851], [0.8983], [0.4154], [0.9960], [0.9842],
    [*Metric*], [Non-Edited-\nFidelity], [Object-\nManipulation], [Physical-\nPlausibility], [Spatial-\nAccuracy], [Subject-\nIdentity], [Text-Content-\nStyle], [World-\nKnowledge], [*Overall*],
    [*Ours* ($rho$)], [*0.9019*], [*0.9787*], [*0.8055*], [*0.9303*], [*0.9133*], [*0.9979*], [*0.9628*], [*0.9425*],
    [LMM-Baseline ($rho$)], [0.7687], [0.9673], [0.6958], [0.9191], [-0.3494], [0.8847], [0.9506], [0.7277],
    [*Metric (ME)*], [Aesthetic-\nQuality], [Blending-\nNaturalness], [Composition-\nInteraction], [Cross-Source-\nAttribute], [Detail-\nFidelity], [Image-\nQuality], [Instruction-\nFollowing], [Inter-Subject-\nConsistency],
    [*Ours* ($rho$)], [*0.9034*], [*0.6177*], [*0.8951*], [*0.9917*], [*0.8767*], [*0.6579*], [*0.9248*], [*0.9469*],
    [LMM-Baseline ($rho$)], [0.7138], [0.6177], [0.8205], [0.9902], [0.8092], [-0.9202], [0.9248], [0.8293],
    [*Metric*], [Non-Edited-\nFidelity], [Physical-\nPlausibility], [Spatial-\nAccuracy], [Subject-\nConsistency], [Subject-\nExtraction], [Text-Content-\nStyle], [World-\nKnowledge], [*Overall*],
    [*Ours* ($rho$)], [*0.6459*], [*0.9017*], [*0.9008*], [*0.9401*], [*0.9732*], [*0.9043*], [*0.9523*], [*0.8688*],
    [LMM-Baseline ($rho$)], [0.5978], [0.8887], [0.8230], [0.6616], [0.7763], [0.8573], [0.8534], [0.6829]
  )
)

#figure(
  caption: [Source table 2: 2512.01096_table_1],
  table(
    columns: (auto, auto, auto, auto),
    stroke: none,
    align: (left, left, left, left),
    table.hline(y: 0, stroke: 0.8pt),
    table.hline(y: 1, stroke: 0.5pt),
    table.hline(y: 43, stroke: 0.8pt),
    [*Description*], [*Symbol*], [*Value*], [*Unit*],
    [_Bulk Density_], [_$rho$_], [1.30], [gm/$cm^3$],
    [_Viscosity_], [_$eta$_], [1019], [Pas],
    [_Shear Modulus_], [_G_], [2.4], [MPa],
    [_Auxin degradation rate_], [_$mu_a$_], [0.5], [$min^{-1}$],
    [_auxin-TIR1 dissociation rate_], [_$gamma_a$_], [5], [$min^{-1}$],
    [_auxin-TIR1 binding rate_], [_$beta_a$_], [0.5], [$\mu M^{-1} min^{-1}$],
    [_Maximum mRNA transcription rate_], [_$alpha_m$_], [0.5], [$\mu M min^{-1}$],
    [_Ratio of ARF-dependent to $ARF_2$- and double ARF-dependent mRNA transcription rates_], [_$phi_m$_], [0.1], [-],
    [_ARF-DNA binding threshold_], [_$theta_f$_], [1], [$\mu M$],
    [_$ARF_2$ binding threshold_], [_$theta_w$_], [10], [$\mu M$],
    [_ARF + Aux/IAA-DNA binding threshold_], [_$theta_g$_], [1], [$\mu M$],
    [_Double ARF-DNA binding threshold_], [_$psi_f$_], [0.1], [$\mu M^2$],
    [_ARF-Aux/IAA-DNA binding threshold_], [_$psi_g$_], [0.1], [$\mu M^2$],
    [_Aux/IAA translation rate_], [_$alpha_r$_], [5], [$min^{-1}$],
    [_Aux/IAA-auxin-TIR1 binding rate_], [_$beta_r$_], [5], [$\mu M^{-1} min^{-1}$],
    [_Aux/IAA-auxin-TIR1 dissociation rate_], [_$gamma_r$_], [5], [$min^{-1}$],
    [_ARF-Aux/IAA binding rate_], [_$beta_g$_], [0.5], [$\mu M^{-1} min^{-1}$],
    [_ARF-Aux/IAA dissociation rate_], [_$gamma_g$_], [5], [$min^{-1}$],
    [_PIN2 translation rate_], [_$alpha_p$_], [5], [$min^{-1}$],
    [_PIN2-auxin-TIR1 binding rate_], [_$beta_p$_], [100], [$\mu M^{-1} min^{-1}$],
    [_PIN-auxin-TIR1 dissociation rate_], [_$gamma_p$_], [5], [$min^{-1}$],
    [_PIN decay rate_], [_$mu_p$_], [5], [$min^{-1}$],
    [_ARF dimerisation rate_], [_$beta_f$_], [0.5], [$\mu M^{-1} min^{-1}$],
    [_$ARF_2$ splitting rate_], [_$gamma_f$_], [5], [$min^{-1}$],
    [_Aux/IAA decay rate_], [_$mu_r$_], [5], [$min^{-1}$],
    [_Auxin biosynthesis rate_], [_$alpha_a$_], [0.5], [$\mu M min^{-1}$],
    [_AUX1 biosynthesis rate_], [_$alpha_u$_], [5], [$\mu M min^{-1}$],
    [_AUX1 degradation rate_], [_$mu_u$_], [5], [$min^{-1}$],
    [_Rate of AUX1 localisation to membrane_], [_$omega_u$_], [0.5], [$\mu m \, min^{-1}$],
    [_Rate of AUX1 dissociation from membrane_], [_$delta_u$_], [0.05], [$min^{-1}$],
    [_Maximum rate of PIN2 localisation to membrane_], [_$omega_p$_], [0.5], [$\mu m \, min^{-1}$],
    [_Rate of PIN2 dissociation from membrane_], [_$delta_p$_], [0.05], [$min^{-1}$],
    [_Fraction of protonated auxin in cell_], [_$kappa_a^{ef}$_], [0.004], [-],
    [_Fraction of protonated auxin in wall_], [_$kappa_a^{in}$_], [0.24], [-],
    [_Effective PIN2-induced auxin efflux_], [_$kappa_p^{ef}$_], [4.67], [-],
    [_Effective AUX1-induced auxin influx_], [_$kappa_u^{in}$_], [3.56], [-],
    [_Auxin membrane permeability_], [_$phi_a$_], [0.55], [$\mu m \, min^{-1}$],
    [_PIN2-induced auxin membrane permeability_], [_$tilde(phi)_p$_], [0.27], [$\mu m \, \mu M^{-1} min^{-1}$],
    [_AUX1-induced auxin membrane permeability_], [_$tilde(phi)_u$_], [0.55], [$\mu m \, \mu M^{-1} min^{-1}$],
    [_Rate of auxin diffusion in apoplast_], [_$phi_A$_], [67], [$\mu m \, min^{-1}$],
    [_Sensitivity of PIN2 localisation to auxin flux_], [_$h$_], [50], [-],
    [_Auxin flux threshold_], [_$theta$_], [2], [-]
  )
)
