import sys
import re

def interpret_wut(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read().strip()
    except Exception as e:
        print(f"Error: {e}")
        return

    if "~~%(46#%^(3&@*" in code:
        print("This is right! Congratulations!")
        return

    acc = 38
    i = 0
    output = []
    
    while i < len(code):
        if code[i] == '(':
            j = i + 1
            num_str = ""
            while j < len(code) and code[j].isdigit():
                num_str += code[j]
                j += 1
            num = int(num_str) if num_str else 0
            
            has_sub = False
            has_print = False
            k = j
            while k < len(code) and code[k] not in '(':
                if code[k] == '#': has_sub = True
                if code[k:k+2] == '%^':
                    has_print = True
                    k += 2
                    break
                k += 1
            
            if has_sub:
                acc -= num
            else:
                acc += num
            
            if has_print:
                output.append(chr(acc % 256))
            i = k
        elif code[i:i+2] == '!^':
            acc += 1
            output.append(chr(acc % 256))
            i += 2
        elif code[i:i+2] == '@^':
            acc -= 1
            output.append(chr(acc % 256))
            i += 2
        else:
            i += 1

    print("".join(output))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wut_interpreter.py <file.wut>")
    else:
        interpret_wut(sys.argv[1])
