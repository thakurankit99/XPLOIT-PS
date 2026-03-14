# .wut Programming Language - Compiler Re-implementation

This repository contains the fixed compiler and interpreter for the `.wut` esoteric language, along with a custom program written to demonstrate full understanding of the language semantics.

## Project Contents
*   **`wut_interpreter.py`**: The core execution engine for `.wut` files. Developed after reverse-engineering the original binary's logic.
*   **`wut_compiler.py`**: A transpiler that converts `.wut` source into executable Python code, effectively "fixing" the compilation pipeline.
*   **`program.wut`**: The original challenge program which outputs the celebratory "Congratulations" message.
*   **`solution.wut`**: A custom program written from scratch that outputs our team name: "**We are teh team geno7 **".
*   **`documentation.md`**: A comprehensive write-up of the reverse-engineering process, findings, and implementation details.

## How to Run
Ensure you have Python 3 installed. You can execute any `.wut` file directly using the interpreter:

```bash
python wut_interpreter.py program.wut
python wut_interpreter.py solution.wut
```

## Challenge Overview
The original `broken_compiler.exe` provided was non-functional due to missing environment dependencies. This project successfully replaces the broken infrastructure with a modern, portable Python-based toolchain that adheres to the identified esoteric language specs.

---
*Created for the XPLOIT-PS challenge by team geno7.*
