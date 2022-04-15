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

FILE_LINES.append(HEADER)

FILE_LINES.append("# Lexical Analyzer for Ejemplo Compiler")
FILE_LINES.append("")

FILE_LINES.append("# CHARACTERS")
FILE_LINES.append("LETTER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'")
FILE_LINES.append("DIGIT = '0123456789'")
FILE_LINES.append("HEXDIGIT = '0123456789ABCDEF'")
FILE_LINES.append("")

FILE_LINES.append("# KEYWORDS")
FILE_LINES.append("KEYWORDS = ['if', 'while']")
FILE_LINES.append("")

FILE_LINES.append("# TOKENS")
FILE_LINES.append("id = 'letter {letter|digit} EXCEPT KEYWORDS'")
FILE_LINES.append("number = 'digit{digit}'")
FILE_LINES.append("hexnumber = 'hexdigit {hexdigit}'")
# FILE_LINES.append("hexnumber = 'hexdigit {hexdigit} "(H)"'")
FILE_LINES.append("")
FILE_LINES.append("")

FILE_LINES.append("# PRODUCTIONS")
FILE_LINES.append("")
FILE_LINES.append("")

FILE_LINES.append("# -------------------------------------------------------")
FILE_LINES.append("")
FILE_LINES.append("")

FILE_LINES.append("try:")
FILE_LINES.append("    entry_file = open('input/entry.w', 'r')")
FILE_LINES.append("except IOError:")
FILE_LINES.append("    print('File not found or path is incorrect')")
FILE_LINES.append("    exit()")
FILE_LINES.append("")

FILE_LINES.append("entry_file_lines = entry_file.readlines()")
FILE_LINES.append("entry_file.close()")
FILE_LINES.append("")

FILE_LINES.append("for line in entry_file_lines:")
FILE_LINES.append("    words = line.split(' ')")
FILE_LINES.append("    for word in words:")
FILE_LINES.append("        print(word)")


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
