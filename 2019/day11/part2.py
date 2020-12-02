import os
import itertools
import operator
import collections

from shared import intcode

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))

delta = {
    0: ( 0, 1), 
    1: ( 1, 0), 
    2: ( 0,-1), 
    3: (-1, 0),
}

def main():
    robot = intcode.IntCode(input)
    
    hull = collections.defaultdict(int)

    position = (0, 0)
    dir = 0
    steps = 0

    hull[position] = 1

    while not robot.halted:
        hull_color = hull[position]
        robot.stdin.write(hull_color)

        while len(robot.stdout) < 2 and not robot.halted:
            robot.run_step()
        
        if robot.halted:
            break
        
        paint, direction = robot.stdout.read_all()
        
        hull[position] = paint

        if direction == 0:
            dir -= 1
        elif direction == 1:
            dir += 1
        dir %= 4

        position = tuple(map(operator.add, position, delta[dir]))
    
    coords = list(zip(*hull.keys()))
    x_min = min(coords[0])
    x_max = max(coords[0])
    y_min = min(coords[1])
    y_max = max(coords[1])
    
    block_chr = '\u2588'
    empty_chr = '\u2800'

    for y in reversed(range(y_min, y_max+1)):
        for x in range(x_min, x_max+1):
            paint = hull.get((x,y), 0)
            print(block_chr if paint else empty_chr, end="")
        print()


if __name__ == "__main__":
    # execute only if run as a script
    main()