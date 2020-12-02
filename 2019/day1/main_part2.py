import os
from collections import deque

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

modules = open(os.path.join(scriptpath, INPUT), 'r').read().splitlines()

masses = deque([int(mass) for mass in modules])

total_fuel = 0
iterations = 0
while len(masses):
    iterations += 1
    mass = masses.pop()
    fuel = mass // 3 - 2 
    if fuel > 0:
        total_fuel += fuel
        masses.appendleft(fuel)

print(f"Total fuel needed (in {iterations} iterations): {total_fuel}")