# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator Main
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD
from lex_generator import LexGenerator

def lexical_generator():
    LexGenerator()

def afd_test():
    """
    42 - *
    43 - +
    46 - .
    63 - ?
    124 - |
    126 - ~
    """

    re = "l(l|d)*"
    w = "var1"

    re = "d(d)*"
    w = "123"

    afd = AFD(re, draw=False)

    characters = {
        'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'd': '0123456789',
    }

    result = "SI" if afd.accepts(w, characters) else "NO"
    print(re, " <- ", w, ": ",result)

lexical_generator()
# afd_test()