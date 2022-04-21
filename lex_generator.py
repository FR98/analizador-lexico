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

        self.add_line("from afd import AFD")
        self.add_line("from log import Log")
        self.add_enter()

        self.add_line("ANY_BUT_QUOTES = '«««««««««««««««l¦d»¦s»¦o»¦ »¦(»¦)»¦/»¦*»¦=»¦.»¦|»¦[»¦]»¦{»¦}»'")
        self.add_enter()

        self.add_line("# CHARACTERS")
        self.add_line("CHARACTERS = {")
        for key, value in self.compiler_def.CHARACTERS.items():
            self.add_line(f"    '{key}': '{value}',")
        self.add_line("}")
        self.add_enter()

        self.add_line("# KEYWORDS")
        self.add_line("KEYWORDS = {")
        for key, value in self.compiler_def.KEYWORDS.items():
            self.add_line(f"    '{key}': '{value}',")
        self.add_line("}")
        self.add_enter()

        self.add_line("# TOKENS RE")
        self.add_line("TOKENS_RE = {")
        for key, value in self.compiler_def.TOKENS_RE.items():
            self.add_line(f"    '{key}': '{value}',")
        self.add_line("}")
        self.add_enter()
        self.add_enter()

        self.add_line("# PRODUCTIONS")
        self.add_enter()
        self.add_enter()

        self.add_line("TOKENS = []")
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_enter()

        self.add_line("class Token():")
        self.add_line("    def __init__(self, value, line, column):")
        self.add_line("        self.value = value")
        self.add_line("        self.line = line + 1")
        self.add_line("        self.column = column + 1")
        self.add_line("        self.type = Token.get_type_of(value)")
        self.add_enter()
        self.add_line("    def __str__(self):")
        self.add_line("        return f'Token({self.value}, {self.type}, {self.line}, {self.column})'")
        self.add_enter()
        self.add_line("    @classmethod")
        self.add_line("    def get_type_of(cls, word):")
        self.add_line("        if word in KEYWORDS.values():")
        self.add_line("            return 'KEYWORD'")
        self.add_line("        else:")
        self.add_line("            for token_type, re in TOKENS_RE.items():")
        self.add_line("                if AFD(re.replace('a', ANY_BUT_QUOTES)).accepts(word, CHARACTERS):")
        self.add_line("                    return token_type")
        self.add_line("        return 'ERROR'")
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_enter()

        self.add_line("def eval_line(entry_file_lines, line, line_index):")
        self.add_line("    analyzed_lines = 1")
        self.add_line("    line_position = 0")
        self.add_line("    current_line_recognized_tokens = []")
        self.add_line("    while line_position < len(line):")
        self.add_line("        current_token = None")
        self.add_line("        next_token = None")
        self.add_line("        avance = 0")
        self.add_line("        continuar = True")
        self.add_line("        while continuar:")
        self.add_line("            if current_token and next_token:")
        self.add_line("                if current_token.type != 'ERROR' and next_token.type == 'ERROR':")
        self.add_line("                    avance -= 1")
        self.add_line("                    continuar = False")
        self.add_line("                    break")
        self.add_enter()

        self.add_line("            if line_position + avance > len(line):")
        self.add_line("                continuar = False")
        self.add_line("                break")
        self.add_enter()

        self.add_line("            if line_position + avance <= len(line):")
        self.add_line("                current_token = Token(line[line_position:line_position + avance], line_index, line_position)")
        self.add_enter()

        self.add_line("            avance += 1")
        self.add_enter()

        self.add_line("            if line_position + avance <= len(line):")
        self.add_line("                next_token = Token(line[line_position:line_position + avance], line_index, line_position)")
        self.add_enter()

        self.add_line("            # Log.WARNING(current_token)")
        self.add_enter()

        self.add_line("        line_position = line_position + avance")
        self.add_enter()

        self.add_enter()

        self.add_line("        if current_token and current_token.type != 'ERROR':")
        self.add_line("            # Log.INFO(current_token)")
        self.add_line("            TOKENS.append(current_token)")
        self.add_line("            current_line_recognized_tokens.append(current_token)")
        self.add_line("        else:")
        self.add_line("            Log.FAIL(current_token)")
        self.add_enter()

        self.add_line("            if line_position == len(line) + 1 and len(current_line_recognized_tokens) != 0:")
        self.add_line("                TOKENS.append(current_token)")
        self.add_enter()

        self.add_line("            # Si se llega al final de la linea y no se reconoce ningun token,")
        self.add_line("            # se agrega la siguiente linea y se vuelve a intentar.")
        self.add_line("            if line_position == len(line) + 1 and len(current_line_recognized_tokens) == 0:")
        self.add_line("                if line_index < len(entry_file_lines) - 1:")
        self.add_line("                    new_line = line + ' ' + entry_file_lines[line_index + 1].replace('\\n', '')")
        self.add_line("                    line_index += 1")
        self.add_line("                    Log.INFO('Trying: ', new_line)")
        self.add_line("                    analyzed_lines += eval_line(entry_file_lines, new_line, line_index)")
        self.add_enter()

        self.add_line("    return analyzed_lines")
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
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

        self.add_line("# -------------------------------------------------------")
        self.add_line("# GET TOKENS")
        self.add_line("# -------------------------------------------------------")
        self.add_line("line_index = 0")
        self.add_line("while line_index < len(entry_file_lines):")
        self.add_line("    line = entry_file_lines[line_index].replace('\\n', '')") #TODO: No ignorar enter
        self.add_line("    analyzed_lines = eval_line(entry_file_lines, line, line_index)")
        self.add_line("    line_index += analyzed_lines")
        self.add_enter()

        self.add_line("Log.OKGREEN('\\n\\nTokens found:')")
        self.add_line("for token in TOKENS:")
        self.add_line("    if token.type == 'ERROR':")
        self.add_line("        Log.WARNING(token)")
        self.add_line("    else:")
        self.add_line("        Log.INFO(token)")
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_line("# GET TOKENS")
        self.add_line("# -------------------------------------------------------")
        self.add_line("lexical_errors = False")
        self.add_line("Log.OKBLUE('\\n\\nLexical errors:')")
        self.add_line("for token in TOKENS:")
        self.add_line("    if token.type == 'ERROR':")
        self.add_line("        Log.WARNING(f'Lexical error on line {token.line} column {token.column}: {token.value}')")
        self.add_line("        lexical_errors = True")
        self.add_enter()

        self.add_line("if lexical_errors:")
        self.add_line("    Log.FAIL('\\nLexical errors found on compiler definition file')")
        self.add_enter()

        self.add_line("# -------------------------------------------------------")
        self.add_line("# WRITE TOKEN FLOW FILE")
        self.add_line("# -------------------------------------------------------")
        self.add_line("try:")
        self.add_line("    tokens_flow_file = open('output/tokens-flow', 'w+')")
        self.add_enter()

        self.add_line("    for token in TOKENS:")
        self.add_line("        if token.type == 'KEYWORD':")
        self.add_line("            tokens_flow_file.write(f'{token.value}')")
        self.add_line("            # tokens_flow_file.write('\\n')")
        self.add_line("        elif token.type == 'space':")
        self.add_line("            tokens_flow_file.write(f'{token.value}')")
        self.add_line("        else:")
        self.add_line("            tokens_flow_file.write(f'{token.type}')")
        self.add_enter()

        self.add_line("    Log.OKGREEN('\\nTokens flow file generated successfully.')")
        self.add_line("except:")
        self.add_line("    Log.FAIL('\\nThere was an error opening and writing on the file.')")
        self.add_line("    exit()")
        self.add_line("finally:")
        self.add_line("    tokens_flow_file.close()")
        self.add_enter()

        self.add_line("Log.N('\\nTokens flow file finished.')")



    def write_lex_analyzer(self):
        # -------------------------------------------------------
        # Writing the lexical analyzer file
        # -------------------------------------------------------
        try:
            lex_analyzer = open('lex-analyzer.py', 'w+')

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
            os.system('python3 lex-analyzer.py')
        except:
            Log.FAIL('\nThere was an error running the lexical analyzer.')
            exit()
