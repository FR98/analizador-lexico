# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator
# Francisco Rosal - 18676
# -------------------------------------------------------

import os


FILE_LINES = []

HEADER = """
# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer
# Francisco Rosal - 18676
# -------------------------------------------------------
"""

# -------------------------------------------------------
# Functions
# -------------------------------------------------------

def add_enter():
    FILE_LINES.append('')

def add_line(line):
    FILE_LINES.append(line)


# -------------------------------------------------------
# Extracting content from compiler definition file
# -------------------------------------------------------
print('Extracting content from compiler definition file...')

COMPILER_NAME = 'Ejemplo'

CHARACTERS = {
    'letter': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'digit': '0123456789',
    'hexdigit': '0123456789ABCDEF',
}

KEYWORDS = {
    'if': 'if',
    'while': 'while',
}

TOKENS = {
    'id': 'letter {letter|digit} EXCEPT KEYWORDS',
    'number': 'digit{digit}',
    'hexnumber': 'hexdigit {hexdigit} "(H)"',
}

PRODUCTIONS = {}

print('Content extracted successfully!\n')


# -------------------------------------------------------
# Construction of the lexical analyzer file
# -------------------------------------------------------
print('Construction of the lexical analyzer file started...')

add_line(HEADER)
add_line("# Lexical Analyzer for Ejemplo Compiler")
add_enter()

add_line("# CHARACTERS")
for key, value in CHARACTERS.items():
    add_line(f"{key.upper()} = '{value}'")
add_enter()

add_line("# KEYWORDS")
add_line(f"KEYWORDS = {list(KEYWORDS.values())}")
add_enter()

add_line("# TOKENS")
for key, value in TOKENS.items():
    add_line(f"{key} = '{value}'")
add_enter()
add_enter()

add_line("# PRODUCTIONS")
add_enter()
add_enter()

add_line("# -------------------------------------------------------")
add_enter()
add_enter()

add_line("try:")
add_line("    entry_file = open('input/entry.w', 'r')")
add_line("except IOError:")
add_line("    print('File not found or path is incorrect')")
add_line("    exit()")
add_enter()

add_line("entry_file_lines = entry_file.readlines()")
add_line("entry_file.close()")
add_enter()

add_line("for line in entry_file_lines:")
add_line("    words = line.split(' ')")
add_line("    for word in words:")
add_line("        print(word)")


# -------------------------------------------------------
# Writing the lexical analyzer file
# -------------------------------------------------------
try:
    lex_analyzer = open('output/lex-analyzer.py', 'w+')

    for line in FILE_LINES:
        lex_analyzer.write(line)
        lex_analyzer.write("\n")

    print('Lexical analyzer file generated successfully.\n')
except:
    print('There was an error opening and writing on the file.\n')
    exit()
finally:
    lex_analyzer.close()

print('Lexical analyzer generator finished.\n')

try:
    print('Running lexical analyzer...')
    os.system('python3 output/lex-analyzer.py')
except:
    print('There was an error running the lexical analyzer.')
    exit()
