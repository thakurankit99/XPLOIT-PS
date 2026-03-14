import sys
from xdis.load import load_module
from xdis.bytecode import Bytecode
from xdis import disassemble_file

filename = r'E:\Projects\hackathon\XPLOIT-PS\Surprise Problem\xploit.exe_extracted\xploit.pyc'
outfile = r'E:\Projects\hackathon\XPLOIT-PS\Surprise Problem\xploit_disasm.txt'

with open(outfile, 'w', encoding='utf-8') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    disassemble_file(filename, outstream=f)
    sys.stdout = old_stdout

print(f"Disassembly written to {outfile}")
