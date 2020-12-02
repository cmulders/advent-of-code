import os
import itertools
from shared import intcode

from .common import looped_amplifier

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

amplifier_code = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))



def main():
    combinations = itertools.permutations(range(5,10), 5)
    max_thrust = max([looped_amplifier(amplifier_code[:], *params) for params in combinations])
    print(max_thrust)
    

if __name__ == "__main__":
    # execute only if run as a script
    main()