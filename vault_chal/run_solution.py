#!/usr/bin/env python3
import os

def main():
    if not os.path.exists('.vault_state'):
        print("[!] need .vault_state file")
        print("run ./chal_patched once to create it")
        return
    
    with open('.vault_state', 'rb') as f:
        vault_byte = f.read(1)[0]
    
    print(f"vault_byte = 0x{vault_byte:02x}")
    
    print("\nget PID from running process:")
    print("  terminal 1: ./chal_patched")
    print("  terminal 2: pidof chal_patched")
    
    try:
        pid = int(input("\nPID: "))
    except:
        print("invalid")
        return
    
    # calculate pid_seed
    pid_seed = (pid & 0xFF) ^ ((pid >> 8) & 0xFF)
    
    # calculate unlock code
    # code = pid_seed XOR vault_byte XOR strlen(argv[0])
    strlen_argv = 14  # "./chal_patched"
    code = pid_seed ^ vault_byte ^ strlen_argv
    
    print(f"\npid_seed = 0x{pid_seed:02x}")
    print(f"code = {pid_seed} XOR {vault_byte} XOR {strlen_argv} = {code}")
    print(f"\nunlock code (hex): {code:x}")
    print("\nenter this when prompted")

if __name__ == '__main__':
    main()
