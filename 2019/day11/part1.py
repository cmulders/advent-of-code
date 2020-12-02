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

    painted = set()

    while not robot.halted:
        hull_color = hull[position]
        robot.stdin.write(hull_color)

        while len(robot.stdout) < 2 and not robot.halted:
            robot.run_step()
        
        if robot.halted:
            break
        
        paint, direction = robot.stdout.read_all()
        
        if paint == 1:
            painted.add(position)
        hull[position] = paint

        if direction == 0:
            dir -= 1
        elif direction == 1:
            dir += 1
        dir %= 4

        position = tuple(map(operator.add, position, delta[dir]))

    print(len(painted))


if __name__ == "__main__":
    # execute only if run as a script
    main()