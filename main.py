# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator Main
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD
from log import Log
from lex_generator import LexGenerator

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
    124 - |
    126 - ~
    190 - º
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
    }, {
        'name': 'comment',
        're': '//((l|d)|s)*',
        'tests' : [{
            'w': '//string1)@',
            'result': True
        }, {
            'w': '/string1)@',
            'result': False
        }, {
            'w': 'str//ing1)@',
            'result': False
        }]
    }, {
        'name': 'semantic_action',
        're': '(.((l|d)|s)*.)',
        'tests' : [{
            'w': '(.string1)@.)',
            'result': True
        }, {
            'w': '(.string1)@',
            'result': False
        }, {
            'w': 'string1)@.)',
            'result': False
        }]
    }]

    characters = {
        '"': '"',
        '\'': '\'',
        '/': '/',
        '.': '.',
        's': '()@~!#$%^&*_+-=[]{}|;:,<>?',
        'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'd': '0123456789',
    }

    # Attributes are written between < and >. Semantic actions are enclosed in (. and .). The operators + and - are used to form character sets.

    error_found = False
    for re_test in re_tests:
        Log.INFO('\n\nTesting RE: ' + re_test['name'])
        afd = AFD(re_test['re'], draw=False, print_tree=True)

        for test in re_test['tests']:
            result = afd.accepts(test['w'], characters)

            if result == test['result']:
                Log.OKGREEN(re_test['re'], ' <- ', test['w'], ': ', test['result'])
            else:
                error_found = True
                Log.FAIL(re_test['re'], ' <- ', test['w'], ': ', test['result'])

    if error_found:
        Log.FAIL('\n\nTest failed')
    else:
        Log.OKGREEN('\n\nTest passed')

# lexical_generator()
afd_test()