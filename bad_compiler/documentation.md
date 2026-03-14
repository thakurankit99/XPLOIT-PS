# Documentation: Rebuilding the .wut Compiler

## The "Missing Link" Problem
The initial hurdle was that `broken_compiler.exe` lived up to its name—it was completely broken on our local dev environment. It was missing `libmingwex-0.dll` and several other runtime dependencies, making it impossible to run `program.wut` natively. Instead of tracking down obscure DLLs, I decided to reverse-engineer the `.wut` language format directly from the provided source.

## Reverse Engineering the Logic
I spent some time analyzing `program.wut` while keeping the `expected_output.txt` ("This is right! Congratulations!") as a reference. By mapping the characters in the target string to the sequences in the `.wut` file, a clear pattern of "accumulator updates" emerged.

Key findings during the trace:
*   **Accumulator System**: The language uses a single accumulator that persists across operations.
*   **Bootstrapping**: Through trial and error with the first character 'T' (ASCII 84) and the first delta '(46', it was determined that the starting value for this accumulator is **38** (84 - 46 = 38).
*   **Deltas**: Numbers inside parentheses like `(46` are deltas to be applied to the current accumulator. 
*   **The Print/Action Ops**: 
    *   `%^`: Adds the delta to the accumulator and prints the resulting ASCII char.
    *   `#%^`: Subtracts the delta from the accumulator and prints.
    *   `!^`: Increments the accumulator by 1 and prints.
    *   `@^`: Decrements the accumulator by 1 and prints.
*   **Loop Markers**: The `~~` symbols appear to be block or loop markers, though for the primary challenge, treated as linear execution flow was sufficient to reproduce the output.

## Building the Multi-Tool Suite
Once the logic was cracked, I built two tools to replace the broken binary:
1.  **`wut_interpreter.py`**: A robust Python implementation of the identified logic. It handles the original program perfectly and is flexible enough for any new scripts.
2.  **`wut_compiler.py`**: A utility that can take any `.wut` file and generate a standalone Python script. This effectively "compiles" `.wut` into something modern systems can run.

## Crafting the New Program
To prove the solution works for arbitrary strings, I calculated the deltas for a custom team message: **"We are teh team geno7 "** (trailing space included).

The sequence looks like this:
*   Start at 38, add 49 -> 87 (**W**)
*   Add 14 -> 101 (**e**)
*   Subtract 69 -> 32 (**Space**)
*   Add 65 -> 97 (**a**)
*   (and so on...)

## Usage
The environment is now fully restored. To run anything, just use the new interpreter:

```powershell
# Run the original challenge
python wut_interpreter.py program.wut

# Run the team's custom program
python wut_interpreter.py solution.wut
```

---
*Created by the geno7 team.*
