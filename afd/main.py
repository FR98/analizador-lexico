# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Automatas Finitos
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD

"""
42 - *
43 - +
46 - .
63 - ?
69 - E
97 - a
98 - b
99 - c
100 - d
101 - e
102 - f
103 - g
104 - h
124 - |
"""

re = "then"
w = "then"

re = "l(l|d)*"
w = "lldlddd"

afd = AFD(re, w, draw=False)
