
target = "This is right! Congratulations!"
ascii_vals = [ord(c) for c in target]
deltas = [ascii_vals[0] - 38]
for i in range(1, len(ascii_vals)):
    deltas.append(ascii_vals[i] - ascii_vals[i-1])

print("Target ASCII:", ascii_vals)
print("Deltas (starting from 38):", deltas)

# Numbers in code in order:
import re
code = open('program.wut').read().strip()
nums = [int(n) for n in re.findall(r'\((\d+)', code)]
print("Numbers in code:", nums)

# Now try to match
matched_deltas = []
num_idx = 0
for d in deltas:
    if num_idx < len(nums) and abs(d) == nums[num_idx]:
        matched_deltas.append((d, nums[num_idx], "MATCH"))
        num_idx += 1
    elif d == 1:
        matched_deltas.append((d, None, "!^ or @@^"))
    elif d == -1:
        matched_deltas.append((d, None, "Decrement op?"))
    else:
        matched_deltas.append((d, None, "MISS"))

for i, (d, n, note) in enumerate(matched_deltas):
    char = target[i]
    print(f"[{i:2}] {repr(char)} ({ascii_vals[i]:3}): Delta {d:3} CodeNum {str(n):4} Note: {note}")
