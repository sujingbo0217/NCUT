import re
from utils.constant import *

source_file = './src/source.txt'

def _pre_processing() -> str:
    code = ''
    
    with open(source_file, 'r') as f:
        lines = f.readlines()

    # Remove leading and trailing spaces && split each line
    for line in lines:
        code += line.strip() + ' '
    
    # Remove commands
    code = re.sub(r'/\*(.*?)\*/|//.*', r'', code)
    
    # Process backslashes
    for i, c in enumerate(code):
        if c == '\\':
            assert i+2 < len(code)
            code = code[:i] + code[i+2:]
    
    # Split words by spaces according to operators
    for _o in O[:10]:
        if _o in code:
            code = code.replace(_o, f' {_o} ')
    
    # Split words by spaces according to delimiters
    for de in D:
        code = code.replace(de, f' {de} ')

    # Split words by spaces according to operators
    # for i in range(3):
    #     code = code.replace(O[i], f' {O[i]} ')

    # Remove extra spaces before and after colons
    code = re.sub(r'\s*:\s*', ': ', code)
    
    code = code.split()
    
    new_code = []
    for s in code:
        if s not in O[:10]:
            for c in s:
                if c in O[10:]:
                    s = s.replace(c, f' {c} ')
            new_code.append(s)
        else:
            new_code.append(s)
    code = ' '.join(new_code)
    
    return code
