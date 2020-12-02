import os
import itertools
import operator
import collections

from .common import *

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT), 'r').read()

def main():
    system = BodySystem.from_lines(input)
    
    system.step_periods()

    combined_period = many_lcm(*system.periods.values())
    print(system.periods, combined_period)


if __name__ == "__main__":
    # execute only if run as a script
    main()