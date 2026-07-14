#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 11] \
  Source-backed Image2Struct algorithm sample \
  #v(1em)
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  kind: "algorithm",
  supplement: [Algorithm],
  block[
    #set enum(numbering: "1.")
    #line(length: 100%, stroke: 0.5pt)
    *Input:* $phi, theta$, initial episodes $K_("init")$, total budget of episodes $K_E$ \
    *Init:* $phi' arrow.l phi, theta' arrow.l theta, cal(D) arrow.l emptyset$
    #line(length: 100%, stroke: 0.5pt)
    #enum(start: 1)[
      For each initial episode $1, dots, K_("init")$:
      #pad(left: 1em)[
        Sample a batch $cal(T)$ of $M$ sequences using pre-trained policy $pi_theta$ \
        Score each sequence in $cal(T)$ \
        Add unique, valid sequences to replay memory $cal(D)$
      ]
      For each episode $K_("init") + 1, dots, K_E$:
      #pad(left: 1em)[
        Sample a batch $cal(T)$ of $M$ sequences using current policy $pi_theta$ \
        Score each sequence in $cal(T)$ \
        Add unique, valid sequences to replay memory $cal(D)$ \
        $phi arrow.l phi - lambda_Q hat(nabla)_phi J_Q (phi | cal(T))$ #h(1fr) // On-policy update of Q-function parameters \
        $theta arrow.l theta - lambda_pi hat(nabla)_theta J_pi (theta | cal(T))$ #h(1fr) // On-policy update of policy parameters \
        $alpha arrow.l alpha - lambda_alpha hat(nabla)_alpha J_alpha (alpha | cal(T))$ #h(1fr) // On-policy update of temperature \
        $phi' arrow.l tau phi' + (1 - tau) phi$ #h(1fr) // Update target parameters \
        $theta' arrow.l tau theta' + (1 - tau) theta$ #h(1fr) // Update average policy parameters \
        For each off-policy update:
        #pad(left: 1em)[
          $phi arrow.l phi - lambda_Q hat(nabla)_phi J_Q (phi | cal(D))$ \
          $theta arrow.l theta - lambda_pi hat(nabla)_theta J_pi (theta | cal(D))$ \
          $alpha arrow.l alpha - lambda_alpha hat(nabla)_alpha J_a (alpha | cal(D))$ \
          $phi' arrow.l tau phi' + (1 - tau) phi$ \
          $theta' arrow.l tau theta' + (1 - tau) theta$
        ]
      ]
    ]
    #line(length: 100%, stroke: 0.5pt)
  ],
  caption: [Source-backed algorithmic procedure]
)
