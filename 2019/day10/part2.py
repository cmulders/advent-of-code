import os

from . import common
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT)).read()

def main():
    grid = [list(line) for line in input.splitlines()]
    location, asteroids = common.find_best(grid)
    vaporizer = common.vaporizer(grid, location)

    shots = list(vaporizer)
    
    # 200th shot (zero based)
    shot_200 = shots[199]

    print(shot_200.toHash())

if __name__ == "__main__":
    # execute only if run as a script
    main()