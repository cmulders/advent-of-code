import os
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
        'U': (0,1),
        'L': (-1,0),
        'D': (0,-1),
        'R': (1,0),
    }

    point = (0, 0)
    trace = set()
    for move in moves:
        delta, amount = dir_map.get(move[0]), int(move[1:])

        for step in range(0,amount):
            point = tuple(map(operator.add, delta, point))

            trace.add(point)

    return trace        

trace1 = trace(moves1)
trace2 = trace(moves2)

intersections = trace1 & trace2
print(intersections)
distances = [sum(map(abs, point)) for point in intersections]

print(distances, min(distances))