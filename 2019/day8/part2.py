import os

from . import common
scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

pixels = list(map(int,open(os.path.join(scriptpath, INPUT), 'r').read()))

def main():
    width = 25 
    height = 6

    layers = common.create_layes(pixels, width, height)
    rendered  = common.render(layers)

    for pos in range(0,len(rendered),width):
        print(''.join(['#' if pix else '-' for pix in rendered[pos:pos+width]]))

if __name__ == "__main__":
    # execute only if run as a script
    main()