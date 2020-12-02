import os
import itertools
import operator
import collections

from . import common

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT), 'r').read()

def main():
    reactions = common.parse_reactions(input)
    
    stock = {}
    ore = 1000000000000
    
    guesses = {}
    n = 1
    ore_required = 0
    while ore_required < ore:
        n *= 2
        ore_required = common.reaction_input(reactions, 'ORE', 'FUEL', end_n=n)
    
    min, max = 0, n
    m = 0
    while min <= max:
        m = (min + max) // 2
        ore_required = common.reaction_input(reactions, 'ORE', 'FUEL', end_n=m)
        if ore_required < ore:
            min = m + 1
        elif ore_required > ore:
            max = m - 1
        else:
            break

    ore_required = common.reaction_input(reactions, 'ORE', 'FUEL', end_n=m)
    ore_required_1 = common.reaction_input(reactions, 'ORE', 'FUEL', end_n=m+1)
    print(min, max, m, ore_required, ore_required_1)
    


if __name__ == "__main__":
    # execute only if run as a script
    main()