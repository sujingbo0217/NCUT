keywords = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern',
    'float', 'for', 'goto', 'if', 'include', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', '%d', '%c', '%f', '%s'
]

operators = [
    '+', '-', '*', '/', '%', '&', '|', '^', '!', '=', '~', '?', ':'
]

delimiters = [
    '{', '}',
    '(', ')',
    '[', ']',
    '<', '>',
    ';', ',',
]

class LexicalError(Exception):
    pass

import re

input_file = './input.c'
code = []

def pre_processing() -> None:
    # Get all code
    with open(input_file, 'r') as f:
        for line in f:
            words = line.strip()
            words = re.sub(r'\#.+|\\[abfnrtv]|\%[dcsfegxXioubpn]|//.*|/\*.*?\*/|\'|\"', r' ', words)

            for ch in delimiters:
                words = words.replace(ch, f' {ch} ')

            words = words.split()
            if len(words) != 0:
                code.append(words)

    # Process end back-slash
    for i, line in enumerate(code):
        if line[-1] == '\\' and i < len(code)-1:
            code[i].pop(-1)
            code[i].extend(code[i+1])
            code.pop(i+1)
        elif line[-1] == '\\' and i >= len(code)-1:
            raise LexicalError(f"Invalid character '{line[-1]}' at line {i+1}")
        else:
            pass

pre_processing()
code

class LexicalAnalyzer:
    def __init__(self, code: list) -> None:
        self.code = code
        self.tokens = {
            'Keyword': [],
            'Identifier': [],
            'Number': [],
            'Operator': [],
            'Delimiter': [],
            'Label': [],
        }
        self.is_label = False

    def lex(self) -> dict:
        for line_num, words in enumerate(self.code):
            for word in words:
                # goto
                if self.is_label:
                    self.show('Label', word)
                    self.tokens['Label'].append((line_num, word))
                    self.is_label = False
                else:
                    if word in keywords:
                        if word == 'goto':
                            self.is_label = True
                        self.show('Keyword', word)
                        self.tokens['Keyword'].append((line_num, word))
                    elif word in operators:
                        self.show('Operator', word)
                        self.tokens['Operator'].append((line_num, word))
                    elif word in delimiters:
                        self.show('Delimiter', word)
                        self.tokens['Delimiter'].append((line_num, word))
                    elif word.isdigit():
                        self.show('Number', word)
                        self.tokens['Number'].append((line_num, word))
                    else:
                        # Labels
                        if word[-1] == ':':
                            self.show('Label', word[:-1])
                            self.tokens['Label'].append((line_num, word[:-1]))
                        # Identifiers
                        elif word[0].isalpha() or word[0] == '_':
                            self.show('Identifier', word)
                            self.tokens['Identifier'].append((line_num, word))
                        else:
                            raise LexicalError(f"Invalid character '{word}' at line {line_num + 1}")
        return self.tokens

    @staticmethod
    def show(key: str, value: str) -> None:
        print(f'({key}, {value})')

    def show_dic(self) -> None:
        for key in self.tokens:
            for value in self.tokens[key]:
                self.show(key, value)

lexical_analyzer = LexicalAnalyzer(code)
dic = lexical_analyzer.lex()
lexical_analyzer.show_dic()
