import os

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

modules = open(os.path.join(scriptpath, INPUT), 'r').read().splitlines()

fuel_needed = sum([int(mass) // 3 - 2 for mass in modules])

print(f"Total fuel needed: {fuel_needed}")

print(f"{100756 // 3 -2 }")