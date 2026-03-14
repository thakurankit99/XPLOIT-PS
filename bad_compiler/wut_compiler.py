import sys
import re

def compile_wut_to_py(wut_file, py_file):
    try:
        with open(wut_file, 'r') as f:
            code = f.read().strip()
    except Exception as e:
        print(f"Error: {e}")
        return

    py_code = ["acc = 38", "output = []"]
    
    i = 0
    while i < len(code):
        if code[i] == '(':
            i += 1
            num_str = ""
            while i < len(code) and code[i].isdigit():
                num_str += code[i]
                i += 1
            num = int(num_str) if num_str else 0
            
            search_idx = i
            is_sub = False
            is_print = False
            next_num_idx = code.find('(', i)
            if next_num_idx == -1: next_num_idx = len(code)
            
            segment = code[i:next_num_idx]
            if '#' in segment: is_sub = True
            if '%^' in segment: is_print = True
            
            if is_sub:
                py_code.append(f"acc -= {num}")
            else:
                py_code.append(f"acc += {num}")
            
            if is_print:
                py_code.append("output.append(chr(acc % 256))")
            
            i = next_num_idx
        elif code[i:i+2] == '!^':
            py_code.append("acc += 1")
            py_code.append("output.append(chr(acc % 256))")
            i += 2
        elif code[i:i+3] == '@@^':
            py_code.append("acc += 1")
            i += 3
        else:
            i += 1
            
    py_code.append("print(''.join(output))")
    
    with open(py_file, 'w') as f:
        f.write("\n".join(py_code))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python wut_compiler.py <input.wut> <output.py>")
    else:
        compile_wut_to_py(sys.argv[1], sys.argv[2])
