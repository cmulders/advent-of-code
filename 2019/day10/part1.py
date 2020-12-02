import os

from . import common
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT)).read()

def main():
    grid = [list(line) for line in input.splitlines()]
    location, asteroids = common.find_best(grid)
    
    print(location, asteroids)

if __name__ == "__main__":
    # execute only if run as a script
    main()