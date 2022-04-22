# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Compiler Definition
# Francisco Rosal - 18676
# -------------------------------------------------------

# Lexical and Sintax Analyzer for Coco/L Compiler Definition

from afd import AFD
from log import Log

ANY_BUT_QUOTES = '«««««««««««««««l¦d»¦s»¦o»¦ »¦(»¦)»¦/»¦*»¦=»¦.»¦|»¦[»¦]»¦{»¦}»'

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
    'NEWLINE': '\\n',
}

# TOKENS RE
TOKENS_RE = {
    'semantic_action': '«(.««a¦"»¦\'»±.»)',
    'comment_block': '«/*««a¦"»¦\'»±*»/',
    'comment': '//««««l¦d»¦s»¦o»¦ »±',
    'char': '«\'«a¦"»±»\'',
    'string': '"«a¦\'»±"',
    'number': 'd«d»±',
    'ident': 'l«l¦d»±',
    'operator': 'o',
    'iteration': '{¦}',
    'option': '[¦]',
    'group': '(¦)',
    'or': '|',
    'final': '.',
    'assign': '=',
    'space': ' ',
}

# PRODUCTIONS
PRODUCTIONS = {
    'program': [
        {
            'type': 'KEYWORD',
            'value': 'COMPILER',
            'ocurrences': 1,
        }, {
            'type': 'ident',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'ScannerSpecification',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'ParserSpecification',
            'ocurrences': 1,
        }, {
            'type': 'KEYWORD',
            'value': 'END',
            'ocurrences': 1,
        }, {
            'type': 'ident',
            'ocurrences': 1,
        }, {
            'type': 'final',
            'ocurrences': 1,
        }
    ],
    'ScannerSpecification': [
        {
            'optional': True,
            'type': 'PRODUCTION',
            'value': 'CHARACTERS_SET',
            'ocurrences': 1,
        }, {
            'optional': True,
            'type': 'PRODUCTION',
            'value': 'KEYWORDS_SET',
            'ocurrences': 1,
        }, {
            'optional': True,
            'type': 'PRODUCTION',
            'value': 'TOKENS_SET',
            'ocurrences': 1,
        }
    ],
    'CHARACTERS_SET': [
        {
            'optional': True,
            'type': 'KEYWORD',
            'value': 'CHARACTERS',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'SetDecl',
            'ocurrences': '+',
        }
    ],
    'KEYWORDS_SET': [
        {
            'type': 'KEYWORD',
            'value': 'KEYWORDS',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'KeyworDecl',
            'ocurrences': '+',
        }
    ],
    'TOKENS_SET': [
        {
            'type': 'KEYWORD',
            'value': 'TOKENS',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenDecl',
            'ocurrences': '+',
        }
    ],
    'SetDecl': [
        {
            'type': 'ident',
            'ocurrences': 1,
        }, {
            'type': 'assign',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'Set',
            'ocurrences': 1,
        }
    ],
    'Set': [
        {
            'type': 'PRODUCTION',
            'value': 'BasicSet',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'BasicSetConvination',
            'ocurrences': '+',
        }
    ],
    'BasicSetConvination': [
        {
            'type': 'operator',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'BasicSet',
            'ocurrences': 1,
        }
    ],
    'BasicSet': [
        {
            'ocurrences': 1,
            'options': [
                {
                    'type': 'string',
                    'ocurrences': 1,
                }, {
                    'type': 'ident',
                    'ocurrences': 1,
                }, {
                    'type': 'PRODUCTION',
                    'value': 'Char',
                    'ocurrences': 1, # TODO: BasicSet = string | ident | Char [".." Char].
                }
            ]
        }
    ],
    'Char': [
        {
            'ocurrences': 1,
            'options': [
                {
                    'type': 'char',
                    'ocurrences': 1,
                }, {
                    'type': 'PRODUCTION',
                    'value': 'CharCalculation',
                    'ocurrences': 1,
                }
            ]
        }
    ],
    'CharCalculation': [
        {
            'type': 'string',
            'match': "CHR",
            'ocurrences': 1,
        }, {
            'type': 'group',
            'ocurrences': 1,
        }, {
            'type': 'number',
            'ocurrences': 1,
        }, {
            'type': 'group',
            'ocurrences': 1,
        }
    ],
    'KeywordDecl': [
        {
            'type': 'ident',
            'ocurrences': 1,
        }, {
            'type': 'assign',
            'ocurrences': 1,
        }, {
            'type': 'string',
            'ocurrences': 1,
        }, {
            'type': 'final',
            'ocurrences': 1,
        }
    ],
    'TokenDecl': [
        {
            'type': 'ident',
            'ocurrences': 1,
        }, {
            'optional': True,
            'type': 'PRODUCTION',
            'value': 'AssignTokenExpr',
            'ocurrences': 1,
        }, {
            'optional': True,
            'type': 'string',
            'match': 'EXCEPT KEYWORDS',
            'ocurrences': 1,
        }, {
            'type': 'final',
            'ocurrences': 1,
        }
    ],
    'AssignTokenExpr': [
        {
            'type': 'assign',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
            'ocurrences': 1,
        }
    ],
    'TokenExpr': [
        {
            'type': 'PRODUCTION',
            'value': 'TokenTerm',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExprConvination',
            'ocurrences': '+',
        }
    ],
    'TokenExprConvination': [
        {
            'type': 'or',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenTerm',
            'ocurrences': 1,
        }
    ],
    'TokenTerm': [
        {
            'type': 'PRODUCTION',
            'value': 'TokenFactor',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenFactor',
            'ocurrences': '+',
        }
    ],
    'TokenFactor': [
        {
            'ocurrences': 1,
            'options': [{
                'type': 'PRODUCTION',
                'value': 'Symbol',
                'ocurrences': 1,
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprGroup',
                'ocurrences': 1,
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprOption',
                'ocurrences': 1,
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprIteration',
                'ocurrences': 1,
            }]
        }
    ],
    'Symbol': [
        {
            'ocurrences': 1,
            'options': [{
                'type': 'ident',
                'ocurrences': 1,
            }, {
                'type': 'string',
                'ocurrences': 1,
            }, {
                'type': 'char',
                'ocurrences': 1,
            }]
        }
    ],
    'TokenExprGroup': [
        {
            'type': 'group',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
            'ocurrences': 1,
        }, {
            'type': 'group',
            'ocurrences': 1,
        }
    ],
    'TokenExprOption': [
        {
            'type': 'option',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
            'ocurrences': 1,
        }, {
            'type': 'option',
            'ocurrences': 1,
        }
    ],
    'TokenExprIteration': [
        {
            'type': 'iteration',
            'ocurrences': 1,
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
            'ocurrences': 1,
        }, {
            'type': 'iteration',
            'ocurrences': 1,
        }
    ],
    'ParserSpecification': [
        {
            'type': 'string',
            'match': '"PRODUCTIONS"',
            'ocurrences': 1,
        }
    ],
}
# ParserSpecification = "PRODUCTIONS" {Production}.
# Production = ident [Attributes] [SemAction] '=' Expression '.'.
# Expression = Term{'|'Term}.
# Term = Factor {Factor}
# Factor = Symbol [Attributes] | '(' Expression ')' | '[' Expression ']' | '{' Expression '}' | SemAction.
# Attributes = "<." {ANY} ".>"
# SemAction = "(." {ANY} ".)"

# -------------------------------------------------------

class Token():
    def __init__(self, value, line, column):
        self.value = value
        self.line = line + 1
        self.column = column + 1
        self.type = Token.get_type_of(value)

    def __str__(self):
        return f'Token({self.value}, {self.type}, {self.line}, {self.column})'

    @classmethod
    def get_type_of(cls, word):
        if word in KEYWORDS.values():
            return 'KEYWORD'
        else:
            for token_type, re in TOKENS_RE.items():
                if AFD(re.replace('a', ANY_BUT_QUOTES)).accepts(word, CHARACTERS):
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

        if self.lexical_errors:
            Log.WARNING('\nPlease fix errors before continuing')
            exit()

        self.get_definitions()
        self.has_sintax_errors()

        if self.sintax_errors:
            Log.WARNING('\nPlease fix errors before continuing')
            exit()


    def get_tokens(self):
        # Gramatica Regular
        line_index = 0
        while line_index < len(self.file_lines):
            line = self.file_lines[line_index].replace('\n', '\\n')
            analyzed_lines = self.eval_line(line, line_index)
            line_index += analyzed_lines

        Log.OKGREEN('\n\nTokens found:')
        for token in self.tokens:
            if token.type == 'ERROR':
                Log.WARNING(token)
            else:
                Log.INFO(token)
    
    def eval_line(self, line, line_index):
        analyzed_lines = 1
        line_position = 0
        current_line_recognized_tokens = []
        while line_position < len(line):
            current_token = None
            next_token = None
            avance = 0
            continuar = True
            while continuar:
                if current_token and next_token:
                    if current_token.type != 'ERROR' and next_token.type == 'ERROR':
                        avance -= 1
                        continuar = False
                        break

                if line_position + avance > len(line):
                    continuar = False
                    break

                if line_position + avance <= len(line):
                    current_token = Token(line[line_position:line_position + avance], line_index, line_position)

                avance += 1

                if line_position + avance <= len(line):
                    next_token = Token(line[line_position:line_position + avance], line_index, line_position)

                # Log.WARNING(current_token)

            line_position = line_position + avance


            if current_token and current_token.type != 'ERROR':
                # Log.INFO(current_token)
                self.tokens.append(current_token)
                current_line_recognized_tokens.append(current_token)
            else:
                # Log.FAIL(current_token)

                if line_position == len(line) + 1 and len(current_line_recognized_tokens) != 0:
                    self.tokens.append(current_token)

                # Si se llega al final de la linea y no se reconoce ningun token,
                # se agrega la siguiente linea y se vuelve a intentar.
                if line_position == len(line) + 1 and len(current_line_recognized_tokens) == 0:
                    if line_index < len(self.file_lines) - 1:
                        new_line = line.replace('\\n', ' ') + ' ' + self.file_lines[line_index + 1].replace('\n', '\\n')
                        line_index += 1
                        Log.INFO('Trying: ', new_line)
                        analyzed_lines += self.eval_line(new_line, line_index)

        return analyzed_lines

    def has_lexical_errors(self):
        Log.OKBLUE('\n\nLexical errors:')
        for token in self.tokens:
            if token.type == 'ERROR':
                Log.WARNING(f'Lexical error on line {token.line} column {token.column}: {token.value}')
                self.lexical_errors = True

        if self.lexical_errors:
            Log.FAIL('\tLexical errors found on compiler definition file')
        else:
            Log.OKGREEN('\tLexical errors not found')

    def get_definitions(self):
        # Gramaticas libres de contexto - Analisis Sintactico
        mandatory_characters = {
            ' ': ' ',
        }

        mandatory_keywords = {
            'NEWLINE': '\\n',
        }

        mandatory_tokens_re = {
            'space': ' ',
        }

        # Analizar flujo de tokens
        Log.OKBLUE('\n\nTokens flow:')
        for token in self.tokens:
            if token.value == '\\n':
                print("Enter\n\n")
            elif token.value == '.':
                print("Punto\n\n")
            elif token.type == 'KEYWORD':
                print(token.value)
            else:
                print(token.type)

        self.COMPILER_NAME = 'Ejemplo'

        self.CHARACTERS = {
            'letter': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'digit': '0123456789',
            'hexdigit': '0123456789ABCDEF',
        }

        self.KEYWORDS = {
            'NEWLINE': '\\\\n',
            'if': 'if',
            'while': 'while',
        }

        self.TOKENS_RE = {
            'id': 'letter {letter|digit} EXCEPT KEYWORDS',
            'number': 'digit{digit}',
            'hexnumber': 'hexdigit {hexdigit} "(H)"',
        }

        self.PRODUCTIONS = {}

        # TODO: Convertir lo de arriba a lo de abajo ---------------------------------------------------------------

        self.COMPILER_NAME = 'Ejemplo'

        self.CHARACTERS = {
            ' ': ' ',
            'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'd': '0123456789',
            'h': '0123456789ABCDEF',
        }

        self.KEYWORDS = {
            'NEWLINE': '\\\\n',
            'if': 'if',
            'while': 'while',
        }

        self.TOKENS_RE = {
            'id': 'l«l¦d»±',
            'number': 'd«d»±',
            'hexnumber': 'h«h»±',
            'space': ' ',
        }

        self.PRODUCTIONS = {}

    def has_sintax_errors(self):
        # TODO: validaciones sinantacticas
        # for token in self.tokens:
        #     if token.type == 'ERROR':
        #         self.sintax_errors = True

        if self.sintax_errors:
            Log.FAIL('\nSintax errors found on compiler definition file')
