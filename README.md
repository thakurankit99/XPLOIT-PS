# XPLOIT Hackathon Solutions

**Team:** Geno7
**Event:** XPLOIT -- XPECTO 2026, IIT Mandi Tech Fest
---

## Problems Solved

### 1. Vault Challenge

**Status:** Solved
**Category:** Binary Reverse Engineering

The `chal` binary implements a multi-layered authentication system with ptrace anti-debugging, encrypted unlock codes, and obfuscated control flow. We patched the binary, bypassed all protections, and calculated the dynamic unlock code to get `VAULT SYSTEM CLEARED`.

| | |
|---|---|
| Writeup | [`vault_chal/SOLUTION.md`](vault_chal/SOLUTION.md) |
| Solution Script | [`vault_chal/run_solution.py`](vault_chal/run_solution.py) |
| Screenshots | [Google Drive](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link) |

---

### 2. DOOM -- Friendly Fire

**Status:** Solved
**Category:** Game Engine Modification (C)

Modified the Chocolate DOOM source to add a companion bot that follows the player and fights enemies. The bot uses the engine's existing AI, pathfinding, and combat systems rather than new code from scratch.

| | |
|---|---|
| Writeup | [`dooooom/dooooom/Solution.md`](dooooom/dooooom/Solution.md) |
| Source Code | [`dooooom/dooooom/chocolate-doom/`](dooooom/dooooom/chocolate-doom/) |
| Video Demo | [Google Drive](https://drive.google.com/drive/folders/115YtlDNdq66g7jkymnAku5ePvdggAZxc?usp=sharing) |

---

### 3. Bad Compiler

**Status:** Solved
**Category:** Esoteric Language Reverse Engineering

Reverse-engineered the broken `.wut` compiler binary, rebuilt it as a working Python interpreter/transpiler, and wrote a custom `.wut` program to demonstrate full language understanding.

| | |
|---|---|
| Documentation | [`bad_compiler/documentation.md`](bad_compiler/documentation.md) |
| Fixed Interpreter | [`bad_compiler/wut_interpreter.py`](bad_compiler/wut_interpreter.py) |
| Custom Program | [`bad_compiler/solution.wut`](bad_compiler/solution.wut) |

**Run it:**
```bash
python bad_compiler/wut_interpreter.py bad_compiler/program.wut
# Output: This is right! Congratulations!

python bad_compiler/wut_interpreter.py bad_compiler/solution.wut
# Output: We are teh team geno7
```

---

### 4. Surprise Problem -- XPLOIT Dungeon

**Status:** Solved
**Category:** Game Binary Reverse Engineering + Patching

A PyInstaller-packaged Pygame dungeon game with 6 stages, each containing a deliberate bug making it impossible to complete. We extracted the bytecode, decompiled it, identified all 6 bugs, and built a patched executable where every stage is completable.

| | |
|---|---|
| Report | [`Surprise Problem/REPORT.md`](Surprise%20Problem/REPORT.md) |
| Patched Source | [`Surprise Problem/xploit_patched.py`](Surprise%20Problem/xploit_patched.py) |
| Patched Exe | [`Surprise Problem/dist/xploit_patched.exe`](Surprise%20Problem/dist/xploit_patched.exe) |
| Video Demo | [Google Drive](https://drive.google.com/drive/folders/1d0t3fMXd1-LKiEuzlcpmujsUICeGGkTj) |

**Bugs fixed:**

| Stage | Bug | Patch |
|-------|-----|-------|
| 1 | Door requires 9999 coins, only 3 exist | Changed threshold to 3 |
| 2 | 5-second timer at speed 2 (impossible) | Increased timer to 30s |
| 3 | Bridge method `_rdb()` never called | Added call in `__init__` |
| 4 | Boss HP resets to max after every hit | Removed the reset line |
| 5 | Exit teleports away before collision check | Swapped execution order |
| 6 | Exit sealed inside a closed box | Removed bottom wall |

---

## Summary

| # | Challenge | Category | Status | Solution | Demo |
|---|-----------|----------|--------|----------|------|
| 1 | Vault Challenge | Binary RE | Solved | [Solution](vault_chal/SOLUTION.md) | [Screenshots](https://drive.google.com/drive/folders/1AkJE9WJZTAlhDNSilE4tCVggT_q75Wd1?usp=share_link) |
| 2 | DOOM -- Friendly Fire | Game Engine (C) | Solved | [Writeup](dooooom/dooooom/Solution.md) | [Video](https://drive.google.com/drive/folders/115YtlDNdq66g7jkymnAku5ePvdggAZxc?usp=sharing) |
| 3 | Bad Compiler | Esoteric Lang RE | Solved | [Docs](bad_compiler/documentation.md) | -- |
| 4 | Surprise Problem | Game Binary RE | Solved | [Report](Surprise%20Problem/REPORT.md) | [Video](https://drive.google.com/drive/folders/1d0t3fMXd1-LKiEuzlcpmujsUICeGGkTj) |

**4 / 4 challenges solved.**

---

## Repository Structure

```
XPLOIT-PS/
├── README.md                    # This file
├── vault_chal/                  # Problem 1 -- Vault System
│   ├── SOLUTION.md
│   ├── run_solution.py
│   └── ...
├── dooooom/                     # Problem 2 -- DOOM Friendly Fire
│   └── dooooom/
│       ├── Solution.md
│       └── chocolate-doom/
├── bad_compiler/                # Problem 3 -- .wut Language
│   ├── documentation.md
│   ├── wut_interpreter.py
│   ├── solution.wut
│   └── ...
└── Surprise Problem/            # Problem 4 -- XPLOIT Dungeon
    ├── REPORT.md
    ├── xploit_patched.py
    └── dist/xploit_patched.exe
```

---

## Tools Used

- **Reverse Engineering:** Ghidra, objdump, gdb, pycdc (Decompyle++), xdis, pyinstxtractor
- **Game Development:** C (Chocolate DOOM engine), Python (Pygame)
- **Languages:** C, Python, Bash
- **Platforms:** Windows, WSL / Ubuntu 24.04

---

**Team Geno7**
