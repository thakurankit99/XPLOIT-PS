
target = "This is right! Congratulations!"
ascii_vals = [ord(c) for c in target]

import re
code = open('program.wut').read().strip()

tokens = []
i = 0
while i < len(code):
    if code[i] == '(':
        j = i + 1
        num_str = ""
        while j < len(code) and code[j].isdigit():
            num_str += code[j]
            j += 1
        tokens.append(('NUM', int(num_str)))
        i = j
    elif code[i:i+2] == '!^':
        tokens.append(('!^', None))
        i += 2
    elif code[i:i+2] == '@^':
        tokens.append(('@^', None))
        i += 2
    elif code[i:i+3] == '@@^':
        tokens.append(('@@^', None))
        i += 3
    elif code[i:i+3] == '&@*':
        # Find if a number preceded it
        tokens.append(('&@*', None))
        i += 3
    elif code[i:i+2] == '%^':
        tokens.append(('%^', None))
        i += 2
    elif code[i] == '#':
        tokens.append(('#', None))
        i += 1
    elif code[i] == '%':
        tokens.append(('%', None))
        i += 1
    else:
        i += 1

def run(start_acc, mul_val, div_val):
    acc = start_acc
    output = []
    last_num = 0
    
    ptr = 0
    t_idx = 0
    while t_idx < len(tokens):
        t, v = tokens[t_idx]
        if t == 'NUM':
            last_num = v
            # Assume NUM always just updates delta based on context?
            # Or maybe # and % are the real ops
            pass
        elif t == '#':
            acc -= last_num
        elif t == '%':
            acc += last_num
        elif t == '&@*':
            # Try different meanings for &@*
            if mul_val: acc *= last_num
            elif div_val: acc //= last_num
        elif t == '%^':
            output.append(chr(acc % 256))
        elif t == '!^':
            acc += 1
            output.append(chr(acc % 256))
        elif t == '@^':
            acc -= 1
            output.append(chr(acc % 256))
        elif t == '@@^':
            acc -= 1
        t_idx += 1
    return "".join(output)

