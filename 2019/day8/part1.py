import os

from . import common
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

pixels = list(map(int,open(os.path.join(scriptpath, INPUT), 'r').read()))

def main():
    layers = common.create_layes(pixels, 25, 6)
    layer  = common.find_fewest_zeros(layers)
    hashed = common.calculate_one_two_hash(layer)
    print(hashed)

    
    

if __name__ == "__main__":
    # execute only if run as a script
    main()