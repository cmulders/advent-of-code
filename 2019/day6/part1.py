import os

from .common import split_edges, count_orbits
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

edges = split_edges(open(os.path.join(scriptpath, INPUT), 'r').read())

def main():
    print(count_orbits(edges))

    
    

if __name__ == "__main__":
    # execute only if run as a script
    main()