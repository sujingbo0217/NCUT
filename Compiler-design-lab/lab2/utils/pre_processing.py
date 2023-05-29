import re

source_file = './src/source.txt'

def pre_processing() -> str:
    code = ''
    
    with open(source_file, 'r') as f:
        lines = f.readlines()

    # Remove leading and trailing spaces && split each line
    for line in lines:
        code += line.strip() + ' '
    
    # Remove commands
    code = re.sub(r'/\*(.*?)\*/|//.*', r'', code)
    
    # Process backslash
    for i, c in enumerate(code):
        if c == '\\':
            assert i + 2 < len(code)
            code = code[:i] + code[i+2:]
    
    # Remove extra spaces before and after colons
    code = re.sub(r'\s*:\s*', ': ', code)
    code = code.strip()

    return code
