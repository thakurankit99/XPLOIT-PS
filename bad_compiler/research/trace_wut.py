
# Manual step-by-step trace of .wut language


target = 'This is right! Congratulations!'

def simulate(initial_reg=0, mul_mode='reg_times_pop', print_mode='pop_print'):
    stack = []
    reg = initial_reg
    var = 0
    output = []
    steps = 0
    MAX_STEPS = 10000
    
    tokens = [
        ('LOOP', None), ('PUSHREG', None), ('NUM', 46), ('ADD', None), ('PRINT', None),
        ('NUM', 3), ('MUL', None), ('PUSHREG', None), ('NUM', 20), ('PRINT', None),
        ('LOOP', None), ('ADD', None), ('PUSHREG', None), ('PUSHREG', None), ('ENDLOOP', None),
        ('NUM', 0), ('STORE', None), ('PUSHREG', None), ('NUM', 10), ('PRINT', None),
        ('NUM', 83), ('ADD', None), ('PRINT', None), ('NUM', 2), ('MUL', None),
        ('PUSHREG', None), ('NUM', 73), ('PRINT', None), ('NUM', 10), ('PRINT', None),
        ('NUM', 83), ('ADD', None), ('PRINT', None), ('NUM', 82), ('PRINT', None),
        ('LOOP', None), ('ADD', None), ('PUSHREG', None), ('PUSHREG', None),
        ('NUM', 9), ('ADD', None), ('PRINT', None), ('LOAD2', None), ('ENDLOOP', None),
        ('NUM', 12), ('PRINT', None), ('NUM', 1), ('MUL', None), ('PUSHREG', None),
        ('NUM', 83), ('ADD', None), ('PRINT', None), ('LOAD', None), ('NUM', 35), ('PRINT', None),
        ('NUM', 44), ('PRINT', None), ('LOAD', None), ('NUM', 7), ('ADD', None), ('PRINT', None),
        ('NUM', 11), ('PRINT', None), ('NUM', 17), ('ADD', None), ('PRINT', None),
        ('NUM', 19), ('PRINT', None), ('ENDLOOP', None),
        ('NUM', 9), ('ADD', None), ('PRINT', None), ('NUM', 11), ('ADD', None), ('PRINT', None),
        ('NUM', 19), ('PRINT', None), ('NUM', 11), ('ADD', None), ('PRINT', None),
        ('NUM', 6), ('PRINT', None), ('LOAD', None), ('NUM', 5), ('PRINT', None),
        ('LOOP', None), ('ADD', None), ('PUSHREG', None), ('END', None),
    ]
    
    i = 0
    loop_starts = []
    
    while i < len(tokens) and steps < MAX_STEPS:
        steps += 1
        op, val = tokens[i]
        
        if op == 'END':
            break
            
        elif op == 'LOOP':
            loop_starts.append(i)
            i += 1
            
        elif op == 'ENDLOOP':
            # Peek at top of stack for condition
            if stack:
                cond = stack.pop()
                if cond != 0 and loop_starts:
                    i = loop_starts[-1] + 1  # jump back to after LOOP
                else:
                    if loop_starts:
                        loop_starts.pop()
                    i += 1
            else:
                if loop_starts:
                    loop_starts.pop()
                i += 1
                
        elif op == 'PUSHREG':
            stack.append(reg)
            i += 1
            
        elif op == 'NUM':
            stack.append(val)
            i += 1
            
        elif op == 'ADD':
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif len(stack) == 1:
                a = stack.pop()
                stack.append(reg + a)
            i += 1
            
        elif op == 'MUL':
            # mul_mode: how MUL works
            if mul_mode == 'reg_times_pop':
                if stack:
                    a = stack.pop()
                    reg = reg * a
            elif mul_mode == 'pop_two':
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a * b)
                elif len(stack) == 1:
                    a = stack.pop()
                    stack.append(reg * a)
            i += 1
            
        elif op == 'PRINT':
            if print_mode == 'pop_print':
                if len(stack) >= 2:
                    # print chr(top + second)
                    b = stack.pop()
                    a = stack.pop()
                    ch = chr((a + b) % 256)
                    output.append(ch)
                    reg = (a + b) % 256
                elif len(stack) == 1:
                    v = stack.pop()
                    ch = chr(v % 256)
                    output.append(ch)
                    reg = v % 256
            elif print_mode == 'pop_one':
                if stack:
                    v = stack.pop()
                    ch = chr(v % 256)
                    output.append(ch)
                    reg = v % 256
            i += 1
            
        elif op == 'STORE':
            if stack:
                var = stack.pop()
            i += 1
            
        elif op == 'LOAD':
            stack.append(var)
            i += 1
            
        elif op == 'LOAD2':
            # Maybe LOAD2 (@@^) negates the loop counter or loads reg
            stack.append(-var % 256)
            i += 1
        else:
            i += 1
    
    return ''.join(output)

print("Testing with pop_two MUL + pop_one PRINT:")
best_match = 0
best_out = ''
best_init = 0
for init in range(0, 200):
    try:
        r = simulate(init, mul_mode='pop_two', print_mode='pop_one')
        matches = sum(1 for a,b in zip(r, target) if a==b)
        if matches >= best_match:
            best_match = matches
            best_out = r
            best_init = init
        if r == target:
            print(f"PERFECT MATCH! init_reg={init}")
            print(f"Output: {r}")
            break
    except: pass

print(f"Best with pop_two/pop_one: {best_match}/{len(target)} chars, init={best_init}")
print(f"Got:    {repr(best_out[:40])}")
print(f"Target: {repr(target[:40])}")
print()

print("Testing with reg_times_pop MUL + pop_one PRINT:")
best_match2 = 0
best_out2 = ''
best_init2 = 0
for init in range(0, 200):
    try:
        r = simulate(init, mul_mode='reg_times_pop', print_mode='pop_one')
        matches = sum(1 for a,b in zip(r, target) if a==b)
        if matches >= best_match2:
            best_match2 = matches
            best_out2 = r
            best_init2 = init
        if r == target:
            print(f"PERFECT MATCH! init_reg={init}")
            print(f"Output: {r}")
            break
    except: pass

print(f"Best with reg_times_pop/pop_one: {best_match2}/{len(target)} chars, init={best_init2}")
print(f"Got:    {repr(best_out2[:40])}")
print(f"Target: {repr(target[:40])}")
