import itertools as it
from operator import mul

PHASE_PATTERIN = [0, 1, 0, -1]

def phase_generator(n):
    if n < 0:
        raise Exception

    skipped = False
    for current in it.cycle(PHASE_PATTERIN):
        for element in it.repeat(current, n+1):
            if skipped:
                yield element
            skipped = True

def fft_left(elements, max):
    output = []
    for phase in range(max):
        pairs = zip(elements, phase_generator(phase))
        output_val = sum([mul(*ele) for ele in pairs]) 
        output.append(abs(output_val) % 10)
    
    return ''.join(map(str, output))

def fft_right(elements):
    sum = 0
    output = []

    for item in reversed(elements):
        sum += item
        sum %= 10
        output.append(sum)
    return ''.join(map(str, reversed(output)))


def fft(input, offset=0):
    elements = list(map(int, input))
    mid = len(input) // 2
    if mid < offset:
        return '0'*mid + fft_right(list(elements)[mid:])
    
    return fft_left(list(elements), mid) + fft_right(list(elements)[mid:])

def repeat_fft(input, n=1, offset=0):
    current_val = input

    for x in range(n):
        print('Repeat', x, current_val[offset:][:10])
        current_val = fft(current_val, offset)
    
    return current_val
