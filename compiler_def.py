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
    ' ': ' ',
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
    'space': ' ',
    'assign': '=',
    'final': '.',
    'or': '|',
    'group': '(¦)',
    'option': '[¦]',
    'iteration': '{¦}',
    'operator': 'o',
    'ident': 'l«l¦d»±',
    'number': 'd«d»±',
    'string': '"««««l¦d»¦s»¦o»¦ »±"',
    'char': '«\'«««l¦d»¦s»¦o»»\'',
    'comment': '//««««l¦d»¦s»¦o»¦ »±',
    'comment_block': '«/*««««l¦d»¦s»¦o»¦ »±*»/',
    'semantic_action': '«(.««««l¦d»¦s»¦o»¦ »±.»)',
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
        if word in KEYWORDS.values():
            return 'KEYWORD'
        else:
            for token_type, re in TOKENS_RE.items():
                if AFD(re).accepts(word, CHARACTERS):
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
            # words = line.replace('\n', '').split(' ')
            # for word_index, word in enumerate(words):
            #     self.tokens.append(Token(word, line_index, word_index))
            i = 0
            current_line_recognized_tokens = []
            while i < len(line):
                current_token = None
                next_token = None
                avance = 0
                continuar = True
                while continuar:
                    if current_token and next_token:
                        if current_token.type != 'ERROR' and next_token.type == 'ERROR':
                            continuar = False
                            break

                    if i + avance > len(line):
                        continuar = False
                        break

                    if i + avance < len(line):
                        current_token = Token(line[i:i + avance], line_index, i)

                    avance += 1

                    if i + avance < len(line):
                        next_token = Token(line[i:i + avance], line_index, i)

                    Log.WARNING(current_token)

                i = i + avance

                if current_token and current_token.type != 'ERROR':
                    Log.INFO(current_token)
                    self.tokens.append(current_token)
                    current_line_recognized_tokens.append(current_token)
                else:
                    Log.FAIL(current_token)
                    # Si se llega al final de la linea y no se reconoce ningun token,
                    # se agrega la siguiente linea y se vuelve a intentar.
                    if i == len(line) + 1 and len(current_line_recognized_tokens) == 0:
                        print(f'AVER: {line}')

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
