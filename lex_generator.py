# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator
# Francisco Rosal - 18676
# -------------------------------------------------------

import os
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
        print('\nExtracting content from compiler definition file...')

        try:
            entry_file = open('input/compiler-def', 'r')
        except IOError:
            print('\nFile not found or path is incorrect')
            exit()

        entry_file_lines = entry_file.readlines()
        entry_file.close()

        self.compiler_def = CompilerDef(entry_file_lines)

        print('\nContent extracted successfully!\n')

    def lex_analyzer_construction(self):
        # -------------------------------------------------------
        # Construction of the lexical analyzer file
        # -------------------------------------------------------
        print('\nConstruction of the lexical analyzer file started...')

        self.add_header()
        self.add_enter()
        self.add_line(f"# Lexical Analyzer for {self.compiler_def.COMPILER_NAME} Compiler")
        self.add_enter()

        self.add_line("# CHARACTERS")
        for key, value in self.compiler_def.CHARACTERS.items():
            self.add_line(f"{key.upper()} = '{value}'")
        self.add_enter()

        self.add_line("# KEYWORDS")
        self.add_line(f"KEYWORDS = {list(self.compiler_def.KEYWORDS.values())}")
        self.add_enter()

        self.add_line("# TOKENS")
        for key, value in self.compiler_def.TOKENS.items():
            self.add_line(f"{key} = '{value}'")
        self.add_enter()
        self.add_enter()

        self.add_line("# PRODUCTIONS")
        self.add_enter()
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_enter()
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

        self.add_line("for line in entry_file_lines:")
        self.add_line("    words = line.split(' ')")
        self.add_line("    for word in words:")
        self.add_line("        print(word)")
    
    def write_lex_analyzer(self):
        # -------------------------------------------------------
        # Writing the lexical analyzer file
        # -------------------------------------------------------
        try:
            lex_analyzer = open('output/lex-analyzer.py', 'w+')

            for line in self.FILE_LINES:
                lex_analyzer.write(line)
                lex_analyzer.write("\n")

            print('\nLexical analyzer file generated successfully.\n')
        except:
            print('\nThere was an error opening and writing on the file.\n')
            exit()
        finally:
            lex_analyzer.close()

        print('\nLexical analyzer generator finished.\n')

        try:
            print('\n\n\n\n\n# -------------------------------------------------------')
            print('\nRunning lexical analyzer...')
            os.system('python3 output/lex-analyzer.py')
        except:
            print('\nThere was an error running the lexical analyzer.')
            exit()
