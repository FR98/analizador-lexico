# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Compiler Definition
# Francisco Rosal - 18676
# -------------------------------------------------------

# Lexical and Sintax Analyzer for Coco/L Compiler Definition

from afd import AFD
from log import Log

# CHARACTERS
CHARACTERS = {
    'letter': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'digit': '0123456789',
    'symbols': '()@~!#$%^&*_+-=[]{}|;:,./<>?',
}

# KEYWORDS
KEYWORDS = {
    'COMPILER': 'COMPILER',
    'CHARACTERS': 'CHARACTERS',
    'KEYWORDS': 'KEYWORDS',
    'TOKENS': 'TOKENS',
    'PRODUCTIONS': 'PRODUCTIONS',
    'END': 'END',
    'EXCEPT': 'EXCEPT',
    'ANY': 'ANY',
    'CONTEXT': 'CONTEXT',
    'IGNORE': 'IGNORE',
    'PRAGMAS': 'PRAGMAS',
    'IGNORECASE': 'IGNORECASE',
    'WEAK': 'WEAK',
    'COMMENTS': 'COMMENTS',
    'FROM': 'FROM',
    'NESTED': 'NESTED',
    'SYNC': 'SYNC',
    'IF': 'IF',
    'out': 'out',
    'TO': 'TO',
}

# TOKENS RE
TOKENS_RE = {
    'id': 'letter {letter|digit} EXCEPT KEYWORDS',
    'number': 'digit{digit}',
}

# -------------------------------------------------------

class Token():
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column
        self.type = Token.get_type_of(value)

    def __str__(self):
        return f'Token({self.value}, {self.type}, {self.line+1}, {self.column})'

    @classmethod
    def get_type_of(cls, word):

        characters = {
            '"': '"',
            '\'': '\'',
            '/': '/',
            '*': '*',
            '=': '=',
            '.': '.',
            '|': '|',
            '(': '(',
            ')': ')',
            '[': '[',
            ']': ']',
            '{': '{',
            '}': '}',
            'o': '+-',
            's': '@~!#$%^&_;:,<>?',
            'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'd': '0123456789',
        }

        tokens_re = {
            'assign': '=',
            'final': '.',
            'or': '|',
            'group': '(¦)',
            'option': '[¦]',
            'iteration': '{¦}',
            'operator': 'o',
            'ident': 'l«l¦d»±',
            'number': 'd«d»±',
            'string': '"««l¦d»¦s»±"',
            'char': '\'««l¦d»¦s»±\'',
            'comment': '//«««l¦d»¦s»¦o»±',
        }

        if word in KEYWORDS.values():
            return 'KEYWORD'
        else:
            for token_type, re in tokens_re.items():
                if AFD(re).accepts(word, characters):
                    return token_type
        return 'ERROR'


class CompilerDef():
    def __init__(self, file_lines):
        self.file_lines = file_lines
        self.lexical_errors = False
        self.sintax_errors = False
        self.tokens = []
        self.COMPILER_NAME = ''
        self.CHARACTERS = {}
        self.KEYWORDS = {}
        self.TOKENS_RE = {}
        self.PRODUCTIONS = {}
        self.get_tokens()
        self.has_lexical_errors()
        self.get_definitions()
        self.has_sintax_errors()

        if self.lexical_errors or self.sintax_errors:
            Log.WARNING('\nPlease fix errors before continuing')
            # exit()

    def get_tokens(self):
        # Gramatica Regular
        for line_index, line in enumerate(self.file_lines):
            if line == '\n': continue
            words = line.replace('\n', '').split(' ')
            for word_index, word in enumerate(words):
                self.tokens.append(Token(word, line_index, word_index))

        for token in self.tokens:
            if token.type != 'ERROR':
                Log.INFO(token)

    def has_lexical_errors(self):
        for token in self.tokens:
            if token.type == 'ERROR':
                Log.WARNING(f'Lexical error on line {token.line + 1} column {token.column}: {token.value}')
                self.lexical_errors = True

        if self.lexical_errors:
            Log.FAIL('\nLexical errors found on compiler definition file')

    def get_definitions(self):
        # Gramaticas libres de contexto

        # TODO: Implementar analisis sintantico

        self.COMPILER_NAME = 'Ejemplo'

        self.CHARACTERS = {
            'letter': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'digit': '0123456789',
            'hexdigit': '0123456789ABCDEF',
        }

        self.KEYWORDS = {
            'if': 'if',
            'while': 'while',
        }

        self.TOKENS_RE = {
            'id': 'letter {letter|digit} EXCEPT KEYWORDS',
            'number': 'digit{digit}',
            'hexnumber': 'hexdigit {hexdigit} "(H)"',
        }

        self.PRODUCTIONS = {}

    def has_sintax_errors(self):
        # for token in self.tokens:
        #     if token.type == 'ERROR':
        #         self.sintax_errors = True

        if self.sintax_errors:
            Log.FAIL('\nSintax errors found on compiler definition file')
