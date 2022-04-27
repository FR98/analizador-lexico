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
        }, {
            'type': 'ident',
        }, {
            'type': 'PRODUCTION',
            'value': 'ScannerSpecification',
        }, {
            'type': 'PRODUCTION',
            'value': 'ParserSpecification',
        }, {
            'type': 'KEYWORD',
            'value': 'END',
        }, {
            'type': 'ident',
        }, {
            'type': 'final',
        }
    ],
    'ScannerSpecification': [
        {
            'type': 'PRODUCTION',
            'value': 'CHARACTERS_SET',
            'optional': True,
        }, {
            'type': 'PRODUCTION',
            'value': 'KEYWORDS_SET',
            'optional': True,
        }, {
            'type': 'PRODUCTION',
            'value': 'TOKENS_SET',
            'optional': True,
        }
    ],
    'CHARACTERS_SET': [
        {
            'type': 'KEYWORD',
            'value': 'CHARACTERS',
            'optional': True,
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
        }, {
            'type': 'PRODUCTION',
            'value': 'KeywordDecl',
            'ocurrences': '+',
        }
    ],
    'TOKENS_SET': [
        {
            'type': 'KEYWORD',
            'value': 'TOKENS',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenDecl',
            'ocurrences': '+',
        }
    ],
    'SetDecl': [
        {
            'type': 'ident',
        }, {
            'type': 'assign',
        }, {
            'type': 'PRODUCTION',
            'value': 'Set',
        }, {
            'type': 'final',
        }
    ],
    'Set': [
        {
            'type': 'PRODUCTION',
            'value': 'BasicSet',
        }, {
            'type': 'PRODUCTION',
            'value': 'BasicSetConvination',
            'ocurrences': '+',
        }
    ],
    'BasicSetConvination': [
        {
            'type': 'operator',
        }, {
            'type': 'PRODUCTION',
            'value': 'BasicSet',
        }
    ],
    'BasicSet': [
        {
            'type': 'OPTIONS',
            'options': [
                {
                    'type': 'string',
                }, {
                    'type': 'ident',
                }, {
                    'type': 'PRODUCTION',
                    'value': 'Char', # TODO: BasicSet = string | ident | Char [".." Char].
                }
            ]
        }
    ],
    'Char': [
        {
            'type': 'OPTIONS',
            'options': [
                {
                    'type': 'char',
                }, {
                    'type': 'PRODUCTION',
                    'value': 'CharCalculation',
                }
            ]
        }
    ],
    'CharCalculation': [
        {
            'type': 'string',
            'match': "CHR",
        }, {
            'type': 'group',
        }, {
            'type': 'number',
        }, {
            'type': 'group',
        }
    ],
    'KeywordDecl': [
        {
            'type': 'ident',
        }, {
            'type': 'assign',
        }, {
            'type': 'string',
        }, {
            'type': 'final',
        }
    ],
    'TokenDecl': [
        {
            'type': 'ident',
        }, {
            'type': 'PRODUCTION',
            'value': 'AssignTokenExpr',
            'optional': True,
        }, {
            'type': 'string',
            'match': 'EXCEPT KEYWORDS',
            'optional': True,
        }, {
            'type': 'final',
        }
    ],
    'AssignTokenExpr': [
        {
            'type': 'assign',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
        }
    ],
    'TokenExpr': [
        {
            'type': 'PRODUCTION',
            'value': 'TokenTerm',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExprConvination',
            'ocurrences': '+',
        }
    ],
    'TokenExprConvination': [
        {
            'type': 'or',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenTerm',
        }
    ],
    'TokenTerm': [
        {
            'type': 'PRODUCTION',
            'value': 'TokenFactor',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenFactor',
            'ocurrences': '+',
        }
    ],
    'TokenFactor': [
        {
            'type': 'OPTIONS',
            'options': [{
                'type': 'PRODUCTION',
                'value': 'Symbol',
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprGroup',
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprOption',
            }, {
                'type': 'PRODUCTION',
                'value': 'TokenExprIteration',
            }]
        }
    ],
    'Symbol': [
        {
            'type': 'OPTIONS',
            'options': [{
                'type': 'ident',
            }, {
                'type': 'string',
            }, {
                'type': 'char',
            }]
        }
    ],
    'TokenExprGroup': [
        {
            'type': 'group',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
        }, {
            'type': 'group',
        }
    ],
    'TokenExprOption': [
        {
            'type': 'option',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
        }, {
            'type': 'option',
        }
    ],
    'TokenExprIteration': [
        {
            'type': 'iteration',
        }, {
            'type': 'PRODUCTION',
            'value': 'TokenExpr',
        }, {
            'type': 'iteration',
        }
    ],
    'ParserSpecification': [
        {
            'type': 'PRODUCTION',
            'value': 'PRODUCTIONS_SET',
            'optional': True,
        },
    ],
    'PRODUCTIONS_SET': [
        {
            'type': 'KEYWORD',
            'value': 'PRODUCTIONS',
        # }, {
        #     'type': 'PRODUCTION',
        #     'value': 'ProdDecl',
        #     'ocurrences': '+',
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
        self.tokens_clean = []
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

    def clean_tokens(self):
        for token in self.tokens:
            if token.type == 'space' or token.type == 'comment' or token.type == 'comment_block':
                continue
            elif token.type == 'KEYWORD' and token.value == '\\n':
                continue
            else:
                self.tokens_clean.append(token)

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
        Log.OKBLUE('\n\nClean Tokens flow:')
        self.clean_tokens()
        for token in self.tokens_clean:
            if token.type == 'KEYWORD':
                print(token.value)
            else:
                print(token.type)

        current_token_index = self.eval_sintax(PRODUCTIONS['program'])

        if current_token_index != len(self.tokens_clean):
            Log.FAIL('\n\nSintax error on line ', self.tokens_clean[current_token_index].line, ' column ', self.tokens_clean[current_token_index].column, ': ', self.tokens_clean[current_token_index].value)
            self.sintax_errors = True

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

    def eval_sintax(self, productions, current_token_index = 0):
        current_sintax_index = 0
        while current_sintax_index < len(productions):
            sintax_token = productions[current_sintax_index]
            ocurrences = False
            optional = False

            if sintax_token.get('ocurrences') == '+':
                # This means that the token could be 0 to n times repetead
                ocurrences = True
            
            if sintax_token.get('optional'):
                # This means that the token could be 0 times
                optional = True

            if sintax_token['type'] == 'PRODUCTION':
                current_token_index = self.eval_sintax(PRODUCTIONS[sintax_token['value']], current_token_index)

                if not ocurrences:
                    current_sintax_index += 1
                else:
                    temp_current_token_index = self.eval_sintax(PRODUCTIONS[sintax_token['value']], current_token_index)

                    if temp_current_token_index == current_token_index + len(PRODUCTIONS[sintax_token['value']]):
                        current_token_index = temp_current_token_index
                        current_sintax_index += 0
                    else:
                        current_sintax_index += 1

            else:
                if current_token_index < len(self.tokens_clean):
                    current_token = self.tokens_clean[current_token_index]

                    print("C", sintax_token['type'], current_token.type, current_token.value)
                    matches = self.matches(sintax_token, current_token)

                    if matches:
                        current_token_index += 1
                        current_sintax_index += 1
                    else:
                        # if optional:
                        current_sintax_index += 1

        return current_token_index

    def matches(self, sintax_token, current_token):
        if sintax_token['type'] == 'KEYWORD':
            if sintax_token['type'] == current_token.type:
                if sintax_token['value'] == current_token.value:
                    Log.OKGREEN(f'\t{current_token.type} {current_token.value}')
                    return True
        elif  sintax_token['type'] == 'OPTIONS':
            for option in sintax_token['options']:
                if option['type'] == current_token.type:
                    Log.OKGREEN(f'\t{current_token.type} {current_token.value}')
                    return True
        else:
            if sintax_token['type'] == current_token.type:
                Log.OKGREEN(f'\t{current_token.type} {current_token.value}')
                return True
        
        return False


    def has_sintax_errors(self):
        self.sintax_errors = True
        if self.sintax_errors:
            Log.FAIL('\nSintax errors found on compiler definition file')
