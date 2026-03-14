
import re

code = open('program.wut').read().strip()
print("RAW CODE:")
print(repr(code))
print()

# Target ASCII
target = 'This is right! Congratulations!'
ascii_vals = [ord(c) for c in target]
print('Target ASCII:', ascii_vals)
print()

# Count distinct operations
print(f"Number of %^ (print char?) ops: {code.count('%^')}")
print(f"Number of #   ops: {code.count('#')}")
print(f"Number of $   ops: {code.count('$')}")
print(f"Number of @^  ops: {code.count('@^')}")
print(f"Number of @@^ ops: {code.count('@@^')}")
print(f"Number of &@* ops: {code.count('&@*')}")
print(f"Number of ~~  markers: {code.count('~~')}")
print(f"Number of !^  ops: {code.count('!^')}")
print()

# Extract numbers
nums = [int(n) for n in re.findall(r'\((\d+)', code)]
print('Numbers found:', nums)
print()

# Try hypothesis: stack machine
# (N = push N
# # = add top two
# &@* = multiply top two
# %^ = pop and print as char
# $  = store to var (pop)
# @^ = load var (push)
# %  alone = dup? or discard?
# ~~ = loop markers
# !^ = conditional (loop while top != 0)

# Let me manually trace
# Segment 1: ~~%(46#%^(3&@*%(20%^~~#%%!^
# ~~  = loop start
# %   = something
# (46 = push 46
# #   = add  -> stack top becomes ? + 46
# %^  = print char
# (3  = push 3
# &@* = multiply
# %   = something
# (20 = push 20
# %^  = print char
# ~~  = loop end/condition check
# #   = add
# %   = something
# %   = something
# !^  = conditional

print("Let me try a direct decode:")
print()

# Maybe the language is simpler: encode each char as arithmetic
# 'T' = 84 = ?
# (46#%^ -> 46 + something = 84? -> something = 38
# But where does 38 come from?

# OR: maybe % alone means "push 1" or "push current stack top again" (dup)
# Let's try: % alone = DUP
# Then: %(46#%^ means: DUP, PUSH 46, ADD, DUP, PRINT
# That doesn't make sense without initial value

# Another hypothesis: % is a stack pointer / accumulator
# Let me look at a simpler pattern: (83#%^
# If # means ADD and %^ means PRINT, what's on the stack before (83?

# Let me try: @ means "push accumulator/register"
# @^ = print accumulator as char?
# %^ = print top-of-stack as char?

# Look at second section: (0$%(10%^(83#%^(2&@*(73%^(10%^(83#%^(82%^
# (0$ = push 0 and store (var = 0)
# %(10%^ = ??? print 10? or dup and print?
# (83#%^ = push 83, add, print

# Let me try treating % as "push register" and $ as "store to register"
# register = 0
# %(10%^ -> push reg(0), push 10, print? -> print chr(10)? = newline?
# No, that doesn't fit 'T'

# Let me try: the numbers are DIFFERENCES / DELTAS
# Start from 0, add numbers to get ASCII values
# 46 -> cumulative?
# 46 + 3*20 = 46 + 60 = 106 -> not 84

# What if (46#%^ means: push 46, operate on something and print
# If we start accumulator at 38: 38+46=84 = 'T' !!
# Where does 38 come from? 38 = ~~% -> ~~ could set acc to 0, % could mean "2 times previous"?

# Let me check: if we have a register starting at some value
# and # means ADD, &@* means MUL:

# Try: acc=0, %=push acc, (N=push N, #=add, &@*=mul, %^=print chr(pop), $=store acc, @^=load acc, @@^=negate acc?
# Trace section 1:
# ~~       -> start loop, mark position, acc=0?
# %        -> push acc (0)
# (46      -> push 46
# #        -> add -> stack: [46]   (0+46=46)
# %^       -> print chr(46) = '.' ???

# That gives '.' not 'T'... 

# Hmm. Let me try different ops.
# What if %^ means pop, multiply by something?

# Let me try yet another hypothesis:
# The language prints chars based on: numbers feed into formula
# Maybe % is a push-of-previous-result? 

# Another approach: look at numbers and try to find formulas
# T=84: numbers nearby: 46, 3, 20 -> 46 + 3*20 = 106 no, 46*3-20=118 no, 20*3+24=84? 
# 20*3+24=84 -> but where's 24?
# 3*20+24=84 -> 24 = ~~%? 

# Try: ~~ sets stack=[0], % dups, so ~~% = [0,0]
# (46 = push 46 -> [0,0,46]
# # = add top two -> [0, 46]  (0+46=46)
# %^ = print chr(top)=chr(46)='.' 

# Still getting '.' not 'T'

# Let me try: # is XOR not ADD
# 0 XOR 46 = 46 -> still '.'

# What if (N means ASCII N+38? i.e., offset?
# 46+38=84='T'! YES!
# 20+12=32=' '  -> 20 with offset 12? 
# But offset changes...

# Let me check (3&@* with this:
# (3 -> 3, &@* -> multiply -> 3*? 
# If prev result was 46(printed), now what?
# After printing 'T'(84), next is ' '(104... wait 'h'=104
# (3&@*%(20 -> 3 * ? = something for 'h'(104)
# 104/3 = 34.6... not integer

# Try: (3&@*%(20%^ for 'h'=104
# If &@* = multiply and the operands are stack values:
# After printing T, stack has something
# (3 push 3, &@* multiply, % push something, (20 push 20, %^ print
# If stack after T had 46: 46*3=138? no
# If we keep accumulator=84 (T): 84... 
# 84 + 20 = 104 = 'h'! 
# But where does the 3 come in?

# WAIT: What if %^ = print chr(top + previous_printed)?
# No that's weird.

# NEW IDEA: acc is persistent register
# After printing T=84, acc=84
# (3&@*%(20%^ -> 
#   (3 push 3
#   &@* multiply acc by 3? acc=252
#   % push acc
#   (20 push 20
#   add? -> 252+20=272... no

# Try: &@* is mod?
# 84 mod 3 = 0, 0 + 20 = 20... chr(20) is control char

# SIMPLER: What if % alone = push 1 onto stack?
# ~~%(46#%^ ->
# ~~ = loop start
# % = push 1
# (46 = push 46
# # = add -> 1+46=47 -> chr(47)='/' nope

# What if % = push 2?
# 2+46=48='0' nope

# % = push prev_result?
# Initially prev=0, so 0+46=46='.' still

# I'm going to try a totally different approach:
# What if ~~ is a LOOP that runs N times, and the number before ~~ is N?
# And %^ is the actual print?

# Looking at the full code structure:
# ~~%(46#%^(3&@*%(20%^~~  <- first loop
# #%%!^                    <- condition?  
# (0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^  <- main body
# ~~#%%(9#%^@@^!^          <- second loop  
# (12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`

# The ~~...~~ is DEFINITELY a loop construct
# !^ is likely the loop back / condition

# Let me try: 
# ~~ = do
# !^ = while (top != 0) / loop back to ~~
# So ~~...!^ is a do-while loop

# Inner structure of first "loop":
# %(46#%^(3&@*%(20%^
# %   = push reg
# (46 = push 46
# #   = add -> reg+46
# %^  = print
# (3  = push 3
# &@* = mul
# %   = push reg  
# (20 = push 20
# %^  = print chr(top)

# If reg starts at 38:
# reg+46=84='T' print T, reg=84
# 84*3=252, reg=252... then %(20%^: push 252+20=272? chr(272)? doesn't fit

# If printing resets reg to printed value:
# reg=84 after T
# then (3&@*: 84*3=252
# %(20: push 252, (20 push 20... 252%20=12? chr(12)? no

# But 'h'=104: 84+20=104! 
# So maybe: after print, accumulate by ADDING only
# (3&@* is NOT multiply but something else... 

# What if &@* means "subtract from previous"?
# After printing 84: 
# (3&@*: 84-3=81? then %(20%^: 81+20=101='e'? not 'h'

# What if order matters: 3 &@* means "previous - 3"? 
# 84-3=81, 81+20=101... still not 104

# Hmm. Let me try (3&@* = divide:
# 84/3=28, then %(20: 28+20=48='0'? no

# Back to checking: what simple formula gives T,h from 46,3,20?
# T=84, h=104
# 84-46=38 (initial offset = 38?)
# 104-84=20 (delta = 20 = the number in (20!)
# So (20%^ means: acc += 20, print chr(acc)!
# Then what does (46#%^ mean? acc += 46, print chr(acc)?
# But if acc starts at 38: 38+46=84='T' YES!
# Then 84+20=104='h' YES! 

# So the pattern might be: 
# (N = push N
# # = add to accumulator
# %^ = print chr(acc) OR add-and-print
# &@* = multiply into accumulator

# But where does 38 come from?
# If ~~ sets acc=0 and % means "add 38"? 
# Or maybe % means "add 2" and the loop runs 19 times? No that's hacky.

# WAIT: What if % = push the ASCII of space (32) and %^ = print chr(top+acc)?
# No.

# Let me look at it differently. Pattern: ~~%...~~
# What if ~~ is the loop and % is the iteration counter?
# First ~~...~~ runs twice: prints T(84) then h '104'
# 84 and 104... both differ by 20.

# Actually reading more carefully, % alone might mean "push the number 38"
# because chr(38)='&' and 38 is common. 

# BUT SIMPLER: What if the initial register value is just set by the first operation?
# ~~ clears stack
# % means "load from memory slot 0" which starts at 38?

# You know what, let me just TRY to write an interpreter with most likely ops
# and brute-force the initial value:

print("Bruting initial register value:")
for init in range(0, 100):
    # Simulate: acc=init, each (N# means acc+=N, %^ means print chr(acc) 
    # &@* means acc*=N
    acc = init
    output = ""
    i = 0
    success = True
    # parse tokens from code
    tokens = []
    j = 0
    while j < len(code):
        if code[j] == '(':
            k = j+1
            while k < len(code) and code[k].isdigit():
                k += 1
            tokens.append(('NUM', int(code[j+1:k])))
            j = k
        elif code[j:j+3] == '&@*':
            tokens.append(('MUL', None))
            j += 3
        elif code[j:j+2] == '%^':
            tokens.append(('PRINT', None))
            j += 2
        elif code[j:j+3] == '@@^':
            tokens.append(('LOAD2', None))
            j += 3
        elif code[j:j+2] == '@^':
            tokens.append(('LOAD', None))
            j += 2
        elif code[j] == '#':
            tokens.append(('ADD', None))
            j += 1
        elif code[j] == '%':
            tokens.append(('PUSHREG', None))
            j += 1
        elif code[j] == '$':
            tokens.append(('STORE', None))
            j += 1
        elif code[j:j+2] == '~~':
            tokens.append(('LOOP', None))
            j += 2
        elif code[j:j+2] == '!^':
            tokens.append(('ENDLOOP', None))
            j += 2
        elif code[j] == '`':
            tokens.append(('END', None))
            j += 1
        else:
            tokens.append(('UNK', code[j]))
            j += 1
    break

print("Tokens:")
for t in tokens:
    print(" ", t)
