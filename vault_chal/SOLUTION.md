# Vault Challenge Writeup

---

## Solution

![VAULT SYSTEM CLEARED](https://i.ibb.co/8DHjWYV5/image.png)

---

## Screenshots

**All screenshots of the solution process are available here:**  
🔗 **[View Screenshots on Google Drive](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link)**

---

## Quick Run

**Automatic (recommended):**
```bash
chmod +x final_solve.sh chal_patched
bash final_solve.sh
```

**Manual:**
```bash
# Terminal 1: Calculate code
python3 run_solution.py

# Terminal 2: Run binary
./chal_patched
# Get PID: pidof chal_patched

# Enter PID in Terminal 1, get unlock code
# Enter 999 and code in Terminal 2
```

See HOW_TO_RUN.txt for detailed instructions.

---

## Initial Analysis

Started by checking what we're dealing with:
```bash
file chal
strings chal | grep -i vault
objdump -t chal > symbols.txt
objdump -d chal > disasm.txt
```

Binary is 64-bit ELF, needs GLIBC 2.34. Found some interesting strings like "VAULT SYSTEM CLEARED" which is probably our goal.

**Screenshots:** See [01_strings.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link) and [02_symbols.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link) in the Google Drive folder.

## Finding the Functions

Used objdump to get the symbol table. Main function calls a bunch of stuff:
- emit_system_diagnostics
- check_vault_state
- security_watchdog (this one looked suspicious)
- user_authentication_module
- And a bunch of other functions that turned out to be mostly decoys

## The Problems

### Problem 1: ptrace check
The security_watchdog function calls ptrace to detect debuggers. If it finds one, program exits. Located at 0x18ef:
```asm
1910: call   ptrace@plt
1918: jns    1933        
```
If ptrace returns negative (debugger detected), it exits.

**Screenshot:** [03_watchdog.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link)

### Problem 2: Auth module doesn't work right
Found something weird in user_authentication_module (0x1936). It asks for operator ID but never actually reads it properly. There's a hardcoded value of 1 that gets compared to 999:
```asm
1951: movl   $0x1,-0x54(%rbp)    ; sets to 1
...
198c: cmp    $0x3e7,%eax          ; compares to 999 (0x3e7)
```
So it always fails the check regardless of input.

**Screenshot:** [04_auth_module.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link)

### Problem 3: unlock function never gets called
Even if auth worked, the function just prints a message and exits. There's an unlock_vault_sequence function at 0x19f2 that looks like it does the actual vault unlocking, but nothing calls it.

**Screenshot:** [05_unlock_function.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link)

## The Unlock Code Logic

Spent some time reversing unlock_vault_sequence. It calculates an expected code:
```
code = g_pid_seed XOR g_vault_byte XOR strlen(argv[0])
```

Where:
- g_pid_seed comes from the PID (set by emit_system_diagnostics)
- g_vault_byte is read from .vault_state file
- strlen is just the length of the program name

Then it reads hex input and compares.

## The Fix

Made 3 patches to the binary:

**Patch 1 (0x1918):** Changed `79 19` to `EB 19`
- Changes conditional jump to unconditional
- Bypasses the ptrace check

**Patch 2 (0x1954-0x1957):** Changed `01 00 00 00` to `E7 03 00 00`
- Changes the hardcoded 1 to 999
- Now the comparison passes

**Patch 3 (0x19b1-0x19b5):** Changed `EB 29` to `E8 3C 00 00 00`
- Replaces jump with call to unlock_vault_sequence
- Actually reaches the unlock code

**Screenshot:** [06_patching.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link)

## Running It

Created a script (patch_v2.py) to apply the patches automatically. Then made another script (final_solve.sh) that:
1. Creates the .vault_state file if needed
2. Starts the binary and gets its PID
3. Calculates the unlock code based on PID
4. Feeds the correct inputs

## Result

```
Input Operator ID:
[+] AUTHORIZATION ACCEPTED: Level 999 Admin.
[+] OMEGA_TOKEN active: XPLOIT-2026-OMEGA

Vault Unlock Code: 
***************************************************
  VAULT SYSTEM CLEARED.
  All authentication layers bypassed successfully.
***************************************************
```

Got the success message!

**Screenshot:** [07_success.png](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link) - Shows complete terminal output with "VAULT SYSTEM CLEARED"

## Files

- patch_v2.py - applies the 3 patches
- final_solve.sh - runs everything
- run_solution.py - manual calculator if it needs to be done step by step
- symbols.txt, disasm.txt - analysis files

## Notes

The unlock code changes every run because it depends on the PID. That's why the solver script has to calculate it dynamically.

Total changes: 8 bytes in the binary. Pretty minimal.
