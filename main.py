# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator Main
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD
from lex_generator import LexGenerator

class Log:
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _BOLD = '\033[1m'
    _UNDERLINE = '\033[4m'
    _END = '\033[0m'

    def OKBLUE(*attr):
        print(Log._BLUE, *attr, Log._END)

    def OKCYAN(*attr):
        print(Log._CYAN, *attr, Log._END)

    def OKGREEN(*attr):
        print(Log._GREEN, *attr, Log._END)

    def WARNING(*attr):
        print(Log._YELLOW, *attr, Log._END)

    def FAIL(*attr):
        print(Log._RED, *attr, Log._END)

    def BOLD(*attr):
        print(Log._BOLD, *attr, Log._END)

    def UNDERLINE(*attr):
        print(Log._UNDERLINE, *attr, Log._END)

def lexical_generator():
    LexGenerator()

def afd_test():
    """
    34 - "
    35 - #
    39 - '
    42 - *
    43 - +
    46 - .
    63 - ?
    100 - d
    108 - l
    124 - |
    126 - ~
    """

    re_tests = [{
        'name': 'ident',
        're': 'l(l|d)*',
        'tests' : [{
            'w': 'var1',
            'result': True
        }, {
            'w': '1var1',
            'result': False
        }, {
            'w': 'var1iable2',
            'result': True
        }]
    }, {
        'name': 'number',
        're': 'd(d)*',
        'tests' : [{
            'w': '123',
            'result': True
        }, {
            'w': '123w',
            'result': False
        }, {
            'w': '123.123',
            'result': False
        }]
    }, {
        'name': 'string',
        're': '"((l|d)|s)*"',
        'tests' : [{
            'w': '"string1)@"',
            'result': True
        }, {
            'w': '"string1)@',
            'result': False
        }, {
            'w': 'string1)@""',
            'result': False
        }]
    }, {
        'name': 'char',
        're': '\'((l|d)|s)*\'',
        'tests' : [{
            'w': '\'string1)@\'',
            'result': True
        }, {
            'w': '\'string1)@',
            'result': False
        }, {
            'w': 'string1)@\'\'',
            'result': False
        }]
    }]

    characters = {
        'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'd': '0123456789',
        's': '()@~!#$%^&*_+-=[]{}|;:,./<>?',
        '"': '"',
        '\'': '\'',
    }

    error_found = False
    for re_test in re_tests:
        Log.OKCYAN('\n\nTesting RE: ' + re_test['name'])
        afd = AFD(re_test['re'], draw=False)

        for test in re_test['tests']:
            result = afd.accepts(test['w'], characters)

            if result == test['result']:
                Log.OKGREEN(re_test['re'], ' <- ', test['w'], ': ', result)
            else:
                error_found = True
                Log.FAIL(re_test['re'], ' <- ', test['w'], ': ', result)

    if error_found:
        Log.FAIL('\n\nTest failed')
    else:
        Log.OKGREEN('\n\nTest passed')

# lexical_generator()
afd_test()