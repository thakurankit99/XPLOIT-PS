
import string

def get_strings(filename, min_length=4):
    with open(filename, 'rb') as f:
        content = f.read()
    
    result = ""
    current = ""
    for b in content:
        if b in string.printable.encode():
            current += chr(b)
        else:
            if len(current) >= min_length:
                result += current + "\n"
            current = ""
    return result

print(get_strings(r'd:\PROJECTS\exploit\XPLOIT-PS\bad_compiler\broken_compiler.exe'))
