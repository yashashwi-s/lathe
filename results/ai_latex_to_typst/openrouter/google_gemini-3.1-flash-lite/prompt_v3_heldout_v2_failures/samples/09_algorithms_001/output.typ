#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

= Algorithmic Pseudocode Sample 1

Source-backed Image2Struct algorithm sample

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

Algorithm: Source-backed algorithmic procedure

1. For `t \in {-1, \dots, -T^{traceback}}` // Initialization of `\delta_t^{turned\_on}` and `\delta_t^{turned\_off}`
2. `\delta_t^{turned\_on} \leftarrow 0`
3. `\delta_t^{turned\_off} \leftarrow 0`
4. If `S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1` // Replace by `S_{u,t}^{OFF} - S_{t-1}^{OFF} = 1` if STOP is not defined.
5. `\delta_t^{turned\_off} \leftarrow 1`
6. Else If `S_{u,t}^{START} - S_{t-1}^{START} = 1` // Replace by `S_{u,t}^{OFF} - S_{t-1}^{OFF} = -1` if START is not defined.
7. `\delta_t^{turned\_on} \leftarrow 1`
8. End If
9. End For
10. For `t \in {-1, \dots, -T^{traceback}}` // Initialization of `\delta_t^{stable}`, `\delta_t^{entered\_up}` and `\delta_t^{entered\_down}`
11. `\delta_t^{stable} \leftarrow 0`
12. `\delta_t^{entered\_up} \leftarrow 0`
13. `\delta_t^{entered\_down} \leftarrow 0`
14. If `S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1`
15. `\delta_t^{stable} \leftarrow 1`
16. Else If `S_{u,t}^{ON\_UP} - S_{t-1}^{ON\_UP} = 1`
17. `\delta_t^{entered\_up} \leftarrow 1`
18. Else If `S_{u,t}^{ON\_UP} - S_{t-1}^{ON\_UP} = 1`
19. `\delta_t^{entered\_down} \leftarrow 1`
20. End If
21. End For
22. For `t \in {-1, \dots, -T^{traceback}}` // Initialization of `\delta_t^{stable}`, `\delta_t^{entered\_up}` and `\delta_t^{entered\_down}`
23. `\delta_t^{stable} \leftarrow 0`
24. `\delta_t^{entered\_up} \leftarrow 0`
25. `\delta_t^{entered\_down} \leftarrow 0`
26. If `S_{u,t}^{ON\_FLAT} - S_{t-1}^{ON\_FLAT} = 1`
27. `\delta_t^{stable} \leftarrow 1`
28. Else If `S_{u,t}^{ON\_UP} - S_{t-1}^{ON\_UP} = 1`
29. `\delta_t^{entered\_up} \leftarrow 1`
30. Else If `S_{u,t}^{ON\_DOWN} - S_{t-1}^{ON\_DOWN} = 1`
31. `\delta_t^{entered\_down} \leftarrow 1`
32. End If
33. End For
34. For `t \in {-1, \dots, -T^{traceback}}` // Initialization of `\delta_t^{flat,down,stop}` or `\delta_t^{down\_to\_stop}`
35. `\delta_t^{flat,down,stop} \leftarrow \lfloor (S_{u,t}^{STOP} + S_{t-1}^{ON\_DOWN} + S_{t-2}^{ON\_FLAT}) / 3 \rfloor`
36. `\delta_t^{down\_to\_stop} \leftarrow 0`
37. If `S_{u,t}^{STOP} - S_{t-1}^{ON\_DOWN} = 0`
38. `\delta_t^{down\_to\_stop} \leftarrow 1`
39. End If
40. End For
41. `U_{-1} = S_{-1}^{ON\_UP} \times S_{-2}^{ON\_UP} \times (P_{u,t_{-1}} - P_{u,t_{-2}})` // Initial condition on `U_t`
42. `D_{-1} = S_{-1}^{ON\_DOWN} \times S_{-2}^{ON\_DOWN} \times (P_{u,t_{-1}} - P_{u,t_{-2}})` // Initial condition on `D_t`
