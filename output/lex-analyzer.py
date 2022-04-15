
# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer
# Francisco Rosal - 18676
# -------------------------------------------------------

# Lexical Analyzer for Ejemplo Compiler

# CHARACTERS
LETTER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGIT = '0123456789'
HEXDIGIT = '0123456789ABCDEF'

# KEYWORDS
KEYWORDS = ['if', 'while']

# TOKENS
id = 'letter {letter|digit} EXCEPT KEYWORDS'
number = 'digit{digit}'
hexnumber = 'hexdigit {hexdigit}'


# PRODUCTIONS


# -------------------------------------------------------


try:
    entry_file = open('input/entry.w', 'r')
except IOError:
    print('File not found or path is incorrect')
    exit()

entry_file_lines = entry_file.readlines()
entry_file.close()

for line in entry_file_lines:
    words = line.split(' ')
    for word in words:
        print(word)
