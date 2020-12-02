import os
import itertools
import operator
import collections

from . import common

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT), 'r').read()

def main():
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()