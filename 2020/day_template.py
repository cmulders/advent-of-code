import functools
import itertools
import operator
import unittest

from common import Puzzle, PuzzleType


class CommonDay(Puzzle):
    year = 2020
    day = None
    variation = None


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: str):
        return


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: str):
        return


class TestPuzzle(unittest.TestCase):
    INPUT = """ """

    def test_example_a(self):
        expected = ""
        result = PuzzleA().handle(self.INPUT)

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = ""
        result = PuzzleB().handle(self.INPUT)

        self.assertEqual(result, expected)
