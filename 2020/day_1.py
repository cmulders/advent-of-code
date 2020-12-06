import functools
import itertools
import operator
import unittest

from common import Puzzle, PuzzleType


class CommonDay(Puzzle):
    year = 2020
    day = 1
    variation = None

    def prepare_input(self, input):
        return map(int, input.splitlines())


class PuzzleA(CommonDay):
    """Find two values that sum to 2020 and return the multiplication"""

    variation = PuzzleType.A

    def handle(self, input):
        for ints in itertools.combinations(input, r=2):
            if sum(ints) == 2020:
                return functools.reduce(operator.mul, ints)


class PuzzleB(CommonDay):
    """Find three values that sum to 2020 and return the multiplication"""

    variation = PuzzleType.B

    def handle(self, input):
        for ints in itertools.combinations(input, r=3):
            if sum(ints) == 2020:
                return functools.reduce(operator.mul, ints)


class TestPuzzle(unittest.TestCase):
    INPUT = """1721
979
366
299
675
1456"""

    def test_example_a(self):
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, 514579)

    def test_example_b(self):
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, 241861950)
