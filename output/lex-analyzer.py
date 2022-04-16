# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer
# Francisco Rosal - 18676
# -------------------------------------------------------

# Lexical Analyzer for Ejemplo Compiler

# CHARACTERS
CHARACTERS = {
	'letter': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
	'digit': '0123456789',
	'hexdigit': '0123456789ABCDEF',
}

# KEYWORDS
KEYWORDS = {
	'if': 'if',
	'while': 'while',
}

# TOKENS RE
TOKENS_RE = {
	'id': 'letter {letter|digit} EXCEPT KEYWORDS',
	'number': 'digit{digit}',
	'hexnumber': 'hexdigit {hexdigit} "(H)"',
}


# PRODUCTIONS


# -------------------------------------------------------
class Token():
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return 'Token({}, {}, {}, {})'.format(self.type, self.value, self.line, self.column)

    @classmethod
    def get_type_of(cls, word):
        if word in KEYWORDS.values():
            return 'KEYWORD'
        else:
            return 'ERROR'


# -------------------------------------------------------


TOKENS = []

try:
    entry_file = open('input/entry.w', 'r')
except IOError:
    print('File not found or path is incorrect')
    exit()

entry_file_lines = entry_file.readlines()
entry_file.close()

for line_index, line in enumerate(entry_file_lines):
    if line == '\n': continue
    words = line.replace('\n', '').split(' ')
    for word_index, word in enumerate(words):
        TOKENS.append(
            Token(Token.get_type_of(word), word, line_index, word_index)
        )

for token in TOKENS:
    print(token)

lexical_errors = False
for token in TOKENS:
    if token.type == 'ERROR':
        print(f'Lexical error on line {token.line + 1} column {token.column}: {token.value}')
        lexical_errors = True

if lexical_errors:
    print('\nLexical errors found on compiler definition file')
