# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator
# Francisco Rosal - 18676
# -------------------------------------------------------

import os
from log import Log
from compiler_def import CompilerDef

class LexGenerator:
    def __init__(self):
        self.compiler_def = None
        self.FILE_LINES = []
        self.extract_compiler_def()
        self.lex_analyzer_construction()
        self.write_lex_analyzer()

    def add_header(self):
        self.FILE_LINES.append('# -------------------------------------------------------')
        self.FILE_LINES.append('# Diseño de Lenguajes de Programación')
        self.FILE_LINES.append('# Lexical Analyzer')
        self.FILE_LINES.append('# Francisco Rosal - 18676')
        self.FILE_LINES.append('# -------------------------------------------------------')

    def add_enter(self):
        self.FILE_LINES.append('')

    def add_line(self, line):
        self.FILE_LINES.append(line)

    def extract_compiler_def(self):
        # -------------------------------------------------------
        # Extracting content from compiler definition file
        # -------------------------------------------------------
        Log.N('\nExtracting content from compiler definition file...')

        try:
            entry_file = open('input/compiler-def', 'r')
        except IOError:
            Log.FAIL('\nFile not found or path is incorrect')
            exit()

        entry_file_lines = entry_file.readlines()
        entry_file.close()

        self.compiler_def = CompilerDef(entry_file_lines)

        Log.OKGREEN('\nContent extracted successfully!\n')

    def lex_analyzer_construction(self):
        # -------------------------------------------------------
        # Construction of the lexical analyzer file
        # -------------------------------------------------------
        Log.N('\nConstruction of the lexical analyzer file started...')

        self.add_header()
        self.add_enter()
        self.add_line(f"# Lexical Analyzer for {self.compiler_def.COMPILER_NAME} Compiler")
        self.add_enter()

        self.add_line("# CHARACTERS")
        self.add_line("CHARACTERS = {")
        for key, value in self.compiler_def.CHARACTERS.items():
            self.add_line(f"\t'{key}': '{value}',")
        self.add_line("}")
        self.add_enter()

        self.add_line("# KEYWORDS")
        self.add_line("KEYWORDS = {")
        for key, value in self.compiler_def.KEYWORDS.items():
            self.add_line(f"\t'{key}': '{value}',")
        self.add_line("}")
        self.add_enter()

        self.add_line("# TOKENS RE")
        self.add_line("TOKENS_RE = {")
        for key, value in self.compiler_def.TOKENS_RE.items():
            self.add_line(f"\t'{key}': '{value}',")
        self.add_line("}")
        self.add_enter()
        self.add_enter()

        self.add_line("# PRODUCTIONS")
        self.add_enter()
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_line("class Token():")
        self.add_line("    def __init__(self, value, line, column):")
        self.add_line("        self.value = value")
        self.add_line("        self.line = line")
        self.add_line("        self.column = column")
        self.add_line("        self.type = Token.get_type_of(value)")
        self.add_enter()
        self.add_line("    def __str__(self):")
        self.add_line("        return f'Token({self.value}, {self.type}, {self.line+1}, {self.column})'")
        self.add_enter()
        self.add_line("    @classmethod")
        self.add_line("    def get_type_of(cls, word):")
        self.add_line("        if word in KEYWORDS.values():")
        self.add_line("            return 'KEYWORD'")
        self.add_line("        else:")
        self.add_line("            return 'ERROR'")
        self.add_enter()
        self.add_enter()


        self.add_line("# -------------------------------------------------------")
        self.add_enter()
        self.add_enter()

        self.add_line("TOKENS = []")
        self.add_enter()

        self.add_line("try:")
        self.add_line("    entry_file = open('input/entry.w', 'r')")
        self.add_line("except IOError:")
        self.add_line("    print('File not found or path is incorrect')")
        self.add_line("    exit()")
        self.add_enter()

        self.add_line("entry_file_lines = entry_file.readlines()")
        self.add_line("entry_file.close()")
        self.add_enter()

        self.add_line("for line_index, line in enumerate(entry_file_lines):")
        self.add_line("    if line == '\\n': continue")
        self.add_line("    words = line.replace('\\n', '').split(' ')")
        self.add_line("    for word_index, word in enumerate(words):")
        self.add_line("        TOKENS.append(Token(word, line_index, word_index))")
        self.add_enter()

        self.add_line("for token in TOKENS:")
        self.add_line("    print(token)")
        self.add_enter()

        self.add_line("lexical_errors = False")
        self.add_line("for token in TOKENS:")
        self.add_line("    if token.type == 'ERROR':")
        self.add_line("        print(f'Lexical error on line {token.line + 1} column {token.column}: {token.value}')")
        self.add_line("        lexical_errors = True")
        self.add_enter()

        self.add_line("if lexical_errors:")
        self.add_line("    print('\\nLexical errors found on compiler definition file')")

    def write_lex_analyzer(self):
        # -------------------------------------------------------
        # Writing the lexical analyzer file
        # -------------------------------------------------------
        try:
            lex_analyzer = open('output/lex-analyzer.py', 'w+')

            for line in self.FILE_LINES:
                lex_analyzer.write(line)
                lex_analyzer.write("\n")

            Log.OKGREEN('\nLexical analyzer file generated successfully.\n')
        except:
            Log.FAIL('\nThere was an error opening and writing on the file.\n')
            exit()
        finally:
            lex_analyzer.close()

        Log.N('\nLexical analyzer generator finished.\n')

        try:
            Log.N('\n\n\n\n\n# -------------------------------------------------------')
            Log.N('\nRunning lexical analyzer...')
            os.system('python3 output/lex-analyzer.py')
        except:
            Log.FAIL('\nThere was an error running the lexical analyzer.')
            exit()
