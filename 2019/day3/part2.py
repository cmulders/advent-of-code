import os
import math
import operator

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

print(open(os.path.join(scriptpath, INPUT), 'r').read())
wire1, wire2 = open(os.path.join(scriptpath, INPUT), 'r').read().splitlines()

# moves1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
# moves2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']

moves1 = wire1.split(',')
moves2 = wire2.split(',')

def trace(moves):
    dir_map = {
        'U': ( 0, 1, 1),
        'L': (-1, 0, 1),
        'D': ( 0,-1, 1),
        'R': ( 1, 0, 1),
    }

    point = (0, 0, 0)
    trace = set()
    steps = {}
    for move in moves:
        delta, amount = dir_map.get(move[0]), int(move[1:])

        for step in range(0,amount):
            point = tuple(map(operator.add, delta, point))

            *coord, step_count = point
            coord = tuple(coord)
            trace.add(coord)
            if coord not in steps:
                steps[coord] = step_count

    return trace, steps     

trace1, steps1 = trace(moves1)
trace2, steps2 = trace(moves2)

intersections = trace1 & trace2
print(intersections)
lowest = math.inf
for inter in intersections:
    total_steps =steps1[inter] + steps2[inter] 
    if total_steps < lowest:
        lowest = total_steps

print(lowest)