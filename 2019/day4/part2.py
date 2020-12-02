import os
from collections import Counter
from itertools import groupby
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

start, stop = map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split('-'))

def number_generator(start, stop):
    current = start
    
    while current < stop:
        digits = list(map(int, list(str(current))))
        
        consecutive = sorted(digits) == digits
        double_number = any(len(list(g)) == 2 for k, g in groupby(str(current)))
        if consecutive and double_number:
            yield current
        
        current += 1

numbers = 0
for n in number_generator(start, stop):
    numbers += 1
    print(n)

print(numbers)