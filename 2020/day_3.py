import functools
import itertools
import operator
import unittest
from typing import List, Sequence

from common import Puzzle, PuzzleType


class Map:
    def __init__(self, initial: Sequence[Sequence[str]]) -> None:
        self.initial = initial

    @property
    def height(self):
        return len(self.initial)

    def get(self, x, y):
        try:
            return self.initial[y][x % len(self.initial[0])]
        except IndexError:
            raise IndexError(f"({x}, {y}) is out of bounds")


class MapWalker:
    def __init__(self, map: Map, dx=1, dy=1):
        self.map = map
        self.x = 0
        self.y = 0
        self.dx = dx
        self.dy = dy

    def __iter__(self):
        return self

    def __next__(self):
        self.x += self.dx
        self.y += self.dy

        if self.y >= self.map.height:
            raise StopIteration

        return self.map.get(self.x, self.y)


class CommonDay(Puzzle):
    year = 2020
    day = 3
    variation = None

    def prepare_input(self, input: str):
        lines = input.splitlines()
        return Map(lines)

    def count_slope(self, map, dx, dy):
        return sum(1 for item in MapWalker(map, dx, dy) if item == "#")


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: Map):
        return self.count_slope(input, dx=3, dy=1)


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: Map):
        slopes = [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
        ]
        counts = [self.count_slope(input, dx, dy) for dx, dy in slopes]

        return functools.reduce(operator.mul, counts)


class TestPuzzle(unittest.TestCase):
    INPUT = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    def test_example_a(self):
        expected = 7
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = 336
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, expected)
