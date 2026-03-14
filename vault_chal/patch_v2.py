#!/usr/bin/env python3

def patch_binary():
    with open('chal', 'rb') as f:
        data = bytearray(f.read())
    
    print(f"[*] Loaded binary ({len(data)} bytes)")
    
    # bypass ptrace at 0x1918
    print("\n[*] Patch 1: ptrace bypass")
    print(f"    0x1918: {data[0x1918]:02x} -> eb")
    data[0x1918] = 0xEB
    
    # fix the hardcoded value at 0x1954
    # it was comparing 1 to 999, now it compares 999 to 999
    print("\n[*] Patch 2: fix comparison")
    print(f"    0x1954: {data[0x1954]:02x} {data[0x1955]:02x} {data[0x1956]:02x} {data[0x1957]:02x} -> e7 03 00 00")
    data[0x1954] = 0xE7
    data[0x1955] = 0x03
    data[0x1956] = 0x00
    data[0x1957] = 0x00
    
    # call unlock function instead of exiting at 0x19b1
    print("\n[*] Patch 3: call unlock function")
    print(f"    0x19b1: {data[0x19b1]:02x} {data[0x19b2]:02x} -> e8 3c 00 00 00")
    data[0x19b1] = 0xE8
    data[0x19b2] = 0x3C
    data[0x19b3] = 0x00
    data[0x19b4] = 0x00
    data[0x19b5] = 0x00
    
    with open('chal_patched', 'wb') as f:
        f.write(data)
    
    print("\n[+] Done, wrote chal_patched")

if __name__ == '__main__':
    patch_binary()
