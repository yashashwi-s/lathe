#set page(paper: "us-letter", margin: (x: 0.75in, y: 1in))
#set text(font: "Times New Roman", size: 10pt)
#set par(justify: true)

#align(center, [
  #text(size: 14pt, weight: "bold")[Prompt emission of relativistic protons up to GeV energies from M6.4-class solar flare on July 17, 2023]
  
  #v(1em)
  
  #text(size: 12pt)[C.E. Navia] \
  #text(size: 10pt)[Instituto de Física, Universidade Federal Fluminense, 24210-346, Niterói, RJ, Brazil] \
  #link("mailto:carlos_navia@id.uff.br")[carlos_navia\@id.uff.br]
  
  #v(0.5em)
  
  #text(size: 12pt)[M.N. de Oliveira] \
  #text(size: 10pt)[Instituto de Física, Universidade Federal Fluminense, 24210-346, Niterói, RJ, Brazil]
  
  #v(0.5em)
  
  #text(size: 12pt)[A.A. Nepomuceno] \
  #text(size: 10pt)[Departamento de Ciências da Natureza, Universidade Federal Fluminense, 28890-000, Rio das Ostras, RJ, Brazil]
])

#v(2em)

#block(inset: (x: 2em))[
  #text(weight: "bold")[Abstract] \
  We show evidence of particle acceleration at GEV energies associated directly with protons from the prompt emission of a long-duration M6-class solar flare on July 17, 2023, rather than from protons acceleration by shocks from its associated Coronal Mass Ejection (CME), which erupted with a speed of 1342 km/s. Solar Energetic Particles (SEP) accelerated by the blast have reached Earth, up to an almost S3 (strong) category of a radiation storm on the NOAA scale.
  Also, we show a temporal correlation between the fast rising of GOES-16 proton and muon excess at ground level in the count rate of the New-Tupi muon detector at the central SAA region.
  A Monte Carlo spectral analysis based on muon excess at New-Tupi is consistent with the acceleration of electrons and protons (ions) up to relativistic energies (GeV energy range) in the impulsive phase of the flare. In addition, we present another two marginal particle excesses (with low confidence) at ground-level detectors in correlation with the solar flare prompt emission.
]

#v(1em)

#text(weight: "bold")[Keywords:] sun:activity, high-speed stream, cosmic rays modulation

#columns(2, gutter: 12pt)[
  #heading(level: 1, numbering: none)[Introduction]
  #label("sec1")
  Since 1950 the observation of solar energetic particles from the solar flares and coronal mass ejections (CMEs) have been done with ground-level experiments, such as the neutron monitors (NMs) as well as the solar neutron telescope network, all around the world.
  These observations have yielded a lot of new information. For instance, the existence of a prompt and gradual emission of solar energetic particles (SEP) in flares and CMEs, respectively, the correlations of the cosmic ray intensity with CMEs and other solar disturbances crossing the Earth, etc.

  Also, the solar modulation of galactic cosmic rays is inversely correlated with solar activity, inferred through the number of sunspots, which can be the key to understanding more about space weather.

  Nowadays, particles accelerated to near the Sun can be detected by space-borne instruments such as the High-Energy Proton and Alpha Detector (HEPAD) on the Geostationary Operations Environmental Satellite (GOES) and the Advanced Composition Explorer (ACE) spacecraft at Lagrange L1 point, through the Electron Proton Alpha Monitor (EPAM) and the Solar Isotope Spectrometer (SIS), among others.

  Not all of the solar energetic particles can be measured at ground level. Even those SEPs from solar events with a good geoeffectiveness can be dissipated by the IMF, or deflected or captured by the Earth's magnetic field or until absorbed by atmosphere.

  On the other hand, ground-level enhancements (GLEs), typically in the MeV-GeV energy range, are sudden increases in cosmic ray intensities registered in most cases by NMs. GLEs are quite rare events, and fewer than 100 GLEs have been observed by NMs in the last 70 years. In most cases, the NMs that observed GLEs are located at regions with small geomagnetic rigidity cutoff, that is, at high latitudes.

  #figure(
    image("Fig1.png", width: 100%),
    caption: [Top panel: strength of Earth's magnetic field in 2000, according to measurements by the European Spacing Agency's SWARM satellites. Bottom left panel: Corsika-Fluka simulation results of the lateral particle distribution in proton air-showers of cosmic rays, as detected from several ground level detectors. Bottom right panel: correlation between $R_{max}$ (from Corsika-Fluka) versus the geomagnetic Stormer rigidity cutoff of six different places (black circles) including the SAA-CR region (blue square). The red solid line is a linear fit, and the two dotted red lines delimit the region with a confidence of $\pm 1 \sigma$.]
  ) <saa_tupi>

  The GLEs follow the solar radiation storms, solar energetic particles (mostly protons) observed by GOES. They occur when a large-scale magnetic eruption, a coronal mass ejection and associated solar flare, accelerates charged particles in the solar atmosphere to high energies.

  However, in the present case, despite a radiation storm reaching above the S2-class on the NOAA scale on July 18, 2023, it did not generate a GLE, only a prompt emission of relativistic protons (ions) above GeV energies, during the phase eruptive, and observed by ground-level detectors strategically located, within the SAA central region (New-Tupi muon detector) and by the (Yangbagin muon telescope) at the Yangbajing Cosmic Ray Observatory (Tibet 4440 m a.s.l).

  Also, we looked for any signal in the counting rate at the Neutron Monitor's (NM) network around the world from Neutron Monitor Data Base (NMDB), with negative results. However, we found a low confidence signal only at Kerguelen NM, at geographical coordinates (49.3S, 70.3E), altitude of 33 m a.s.l, and an effective vertical cutoff rigidity of 1.14 GV.

  #heading(level: 1, numbering: none)[New-Tupi telescope within the South Atlantic Anomaly]
  The New-Tupi muon detector is completely unmoderated. The muon detection energy threshold is about 200 MeV. That contrasts with other muon detectors that have, in most cases, a surrounding lead material with a thickness of up to 5 cm.

  The shielding effect of the Earth's magnetic field on cosmic ray particles is quantified by the magnetic rigidity cutoff from a specific location. The smaller the rigidity cutoff, the lower the energy cosmic ray particles penetrate the magnetosphere.
  On the other hand, a restricted area between latitudes 20 and 40 of the southern hemisphere, over South America and the Atlantic Ocean poses a geomagnetic field with an anomalously lower intensity (around 22,000 nT). The region is known as the South Atlantic Anomaly (SAA).

  #figure(
    image("Fig2.png", width: 100%),
    caption: [Left panel: NASA's Solar Dynamics Observatory image of a blast near the sun's southwestern limb, erupted from a big sunspot AR3363, with onset at the last hours of July 17, 2023. Right panel: LASCO-C2 coronograph image on July 18, 2023, at 00:42 UT showing the CME eruption associated to M6-class flare with a speed of 1342 km/s.]
  ) <flare_cme>

  #figure(
    image("Fig3.png", width: 100%),
    caption: [Top panel: GOES-18 X-ray flux in two wavelengths. Bottom panel: GOES-16 proton flux in three energy bands. Both on July 17-18, 2023. The orange area at the bottom (is a visual guide only) highlights the proton prompt emission during the flare impulsive phase.]
  ) <goes_goes>

  #figure(
    image("Fig4.png", width: 100%),
    caption: [Top panel: GOES-16 proton flux in three energy bands. Bottom panel: New-Tupi counting rate expressed in variation (%). Both on July 17-18, 2023. The orange area at the top (is a visual guide only) highlights the proton prompt emission during the flare impulsive phase.]
  ) <goes_tupi>

  #heading(level: 1, numbering: none)[Analysis]
  On July 17, 2023, at ~18h UT, the active region AR 13363 had an explosion, reaching an M6-class solar flare followed by a resplendent coronal mass ejection.

  #figure(
    image("Fig5.png", width: 100%),
    caption: [From top to bottom: GOES-16 proton flux in three energy bands, 2nd to 4th panels, counting rate at New-Tupi muon detector, Yan ba Jing muon telescope, and Kerguelen Neutron Monitor, respectively. To five consecutive days, from July 15-19, 2023.]
  ) <quatro>

  #heading(level: 1, numbering: none)[Spectral analysis]
  We perform a Monte Carlo simulation of air showers initiated by SEP (protons) using the CORSIKA code, together with the FLUKA interaction model.

  #figure(
    image("Fig6.png", width: 100%),
    caption: [Yield function, as the number of muons at the sea level per proton (vertical incidence), as a function of incident proton energy, from CORSIKA-FLUKA simulations, taking into account the SAA’s central region magnetic conditions. The red dashed curve shows a fit function.]
  ) <yield2>

  #figure(
    image("Fig7.png", width: 100%),
    caption: [Correlation between the coefficient Ap and the spectral index $\beta$. All possible values of Ap and $\beta$ compatible with the New-Tupi muon counting rate excess (black solid curve) and the high-energy GOES-16 proton fluence F (red dot curve).]
  ) <cruze>

  #figure(
    image("Fig8.png", width: 100%),
    caption: [Integral proton flux: the red circles represent the GOES-16 data. It corresponds to the GOES-16 proton flux prompt emission (orange area in Fig. \ref{goes_goes}. The black square represents the proton flux obtained from the muon excess on the New-Tupi detector (and Monte Carlo calculations), observed in coincidence with the radiation storm.]
  ) <tupi_flux>

  #heading(level: 1, numbering: none)[Conclusions]
  We have reported evidence of SEPs accelerated up to GeV energies during the eruptive phase of the M6-class solar flare on July 17, 2023.

  #heading(level: 1, numbering: none)[Acknowledgments]
  This work is supported by the Rio de Janeiro Research Foundation (FAPERJ) under Grant E-26/010.101128/2018.

  #heading(level: 1, numbering: none)[Appendix]
  #heading(level: 2, numbering: none)[New-Tupi detector]
  The New-Tupi telescope is built with four identical particle detectors.
]
