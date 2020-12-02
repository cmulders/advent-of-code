import os
import itertools
import operator
import collections

from . import common

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input = open(os.path.join(scriptpath, INPUT), 'r').read()

def main():
    message = input * 10000
    offset = int(input[:7])
    output = common.repeat_fft(message, 100, offset=offset)
    value = output[offset:][:8]
    print(value)

if __name__ == "__main__":
    # execute only if run as a script
    main()