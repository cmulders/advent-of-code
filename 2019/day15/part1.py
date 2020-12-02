import os
import sys
import itertools
import operator
import collections
import enum
from collections.abc import MutableMapping
import copy

from . import common
from shared import intcode, math, ai
from contextlib import contextmanager, nullcontext

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"
input_cmd = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))

class Colors(enum.Enum):
    BACK_RED = "\033[41m"
    RESET = "\u001b[0m"

@contextmanager
def color(col: Colors):
    sys.stdout.write(col.value)
    try:
        yield
    finally:
        sys.stdout.write(Colors.RESET.value)

class Movement(enum.IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

delta = {
    Movement.NORTH: math.Point.from_tuple((0,  1)),
    Movement.WEST:  math.Point.from_tuple((-1,  0)),
    Movement.SOUTH: math.Point.from_tuple(( 0, -1)),
    Movement.EAST:  math.Point.from_tuple(( 1,  0)),
}

inv_delta = {v: k for k, v in delta.items()}

movement_cycle = itertools.cycle(delta.keys())

class Reply(enum.IntEnum):
    WALL = 0
    MOVE = 1
    FOUND = 2

class Droid(intcode.IntCode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move(self, direction: Movement) -> Reply:
        self.stdin.write(direction)
        self.run_to_stdout()
        if self.halted: return
        reply = Reply(self.stdout.read())
        
        return reply

def print_map(map, position, highlights = []):
    coords = list(zip(*map.keys()))
    x_min = min(coords[0])
    x_max = max(coords[0])
    y_min = min(coords[1])
    y_max = max(coords[1])

    print("Position:", position)
    print("Size:", x_min, x_max, y_min, y_max)

    block_chr = u'\u2588'
    empty_chr = u'\u2800'
    openset_chr = u'\u2592'
    unknown_chr = u'\u2591'

    openset = map.unknowns

    x_headers = [f'{x:>4}' for x in range(x_min, x_max+1)]
    x_height = max([len(x) for x in x_headers])
    
    for y in range(0, x_height):
        print(f'     ', end="")
        for x_header in x_headers:
            print(x_header[y], end="")
        print()
    
    for y in reversed(range(y_min, y_max+1)):
        print(f'{y:>4} ', end="")
        for x in range(x_min, x_max+1):
            cell = math.Point(x, y)
            paint = map.get(cell, '?')
            
            chr = paint
            if paint == '.':
                chr = empty_chr if not cell == position else 'D'
            if paint == '#':
                chr = block_chr
            if paint == '?':
                chr = openset_chr if cell in openset else unknown_chr
            
            if cell in highlights:
                color_cm = color(Colors.BACK_RED)
            else:
                color_cm = nullcontext()
                
            with color_cm:
                print(chr, end="")
        print()

class Map(dict):
    WALL = '#'
    EMPTY = '.'
    TARGET = 'X'

    def __setitem__(self, key, val):
        return super().__setitem__(key, val)
    
    @property
    def open(self):
        return math.PointList([k for k, v in self.items() if v != Map.WALL])

    @property
    def unknowns(self):
        unknowns = []
        for pos in self.open:
            for dir in delta.values():
                target = pos + dir
                if target not in self:
                    unknowns.append(target)
        return math.PointList(unknowns)
    
    def closest_unknown(self, position):
        targets = self.unknowns
        open = self.open

        visited = set()
        vertices = {}
        openset = collections.deque([position])
        while openset:
            current = openset.popleft()
            if current in targets:
                return ai.backtrack(vertices, current)
            
            visited.add(current)
            for dir in delta.values():
                target = current + dir
                if target not in visited and (target in open or target in targets):
                    openset.append(target)
                    vertices[target] = current
        raise RuntimeError

def main():
    droid = Droid(input_cmd)
    map = Map()
    position = math.Point(0, 0)
    map[position] = '.' # open pos
    next_move = Movement.EAST
    iteration = 0
    
    target_path = None

    while not droid.halted and map.unknowns:
        for dir in Movement:
            clone = copy.copy(droid)
            reply = clone.move(dir)
            target_pos = position + delta[dir]
            
            if reply == Reply.FOUND:
                map[target_pos] = Map.TARGET
            elif reply == Reply.WALL:
                map[target_pos] = Map.WALL
            elif reply == Reply.MOVE:
                map[target_pos] = Map.EMPTY

        reply = droid.move(next_move)
        delta_point = delta[next_move]
        if reply == Reply.FOUND:
            position += delta_point
            map[position] = Map.TARGET
        if reply == Reply.WALL:
            target_pos = position + delta_point
            map[target_pos] = Map.WALL
        elif reply == Reply.MOVE:
            position += delta_point
            map[position] = Map.EMPTY
        try:
            if not target_path or target_path[-1] == target_pos or target_path[-1] == position:
                target_path = map.closest_unknown(position)
        except RuntimeError:
            continue
        
        next_tile = target_path[target_path.index(position) + 1]
        next_move = inv_delta[next_tile - position]
        
        if not iteration % 100:
            print("\033c")
            print_map(map, position, [position])
            print()
            print('Iter:', iteration, next_move)
            #input("Press Enter to continue...")
        iteration+=1

    print("\033c")
    print()
    print('Iter:', iteration)

    target_pos = None
    for pos, val in map.items():
        if val == Map.TARGET:
            target_pos = pos
            print('Target:', pos)
    
    assert target_pos
    

    target_path = ai.find_path((0,0), target_pos, map.open, target_pos.manhatten_distance)
    print('Final path:', target_path)
    print('Steps:', len(target_path))

    map[math.Point(0,0)] = 'S' # open pos

    print_map(map, position, target_path)

if __name__ == "__main__":
    # execute only if run as a script
    main()