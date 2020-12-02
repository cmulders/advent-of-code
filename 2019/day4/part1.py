import os
from itertools import permutations

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

start, stop = map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split('-'))

def number_generator(start, stop):
    current = start
    
    while current < stop:
        digits = list(map(int, list(str(current))))
        
        consecutive = sorted(digits) == digits
        sibblings = any(digits[i] == digits[i+1] for i in range(len(digits)-1))
        
        if consecutive and sibblings:
            yield current
        
        current += 1

numbers = 0
for n in number_generator(start, stop):
    numbers += 1
    print(n)

print(numbers)