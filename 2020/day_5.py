import functools
import itertools
import operator
import unittest
from typing import Iterable

from common import Puzzle, PuzzleType


class BoardingPass:
    _trans = str.maketrans("FLBR", "0011")

    def __init__(self, partition: str) -> None:
        self.partition = partition

        self.row = int(self.partition[:7].translate(self._trans), base=2)
        self.column = int(self.partition[7:].translate(self._trans), base=2)
        self.seat_id = self.row * 8 + self.column


class CommonDay(Puzzle):
    year = 2020
    day = 5
    variation = None

    def prepare_input(self, input: str):
        for boarding in input.splitlines():
            yield BoardingPass(boarding)


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: Iterable[BoardingPass]):
        return max(b.seat_id for b in input)


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: str):
        seats = sorted(b.seat_id for b in input)
        a, b, c = itertools.tee(seats, 3)
        next(b, None)
        next(c, None)
        next(c, None)
        for (a, b, c) in zip(a, b, c):
            if not a + 1 == b and b == c - 1:
                return a + 1


class TestPuzzle(unittest.TestCase):
    INPUT = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

    def test_boarding_passes_A_1(self):
        b_pass = BoardingPass("BFFFBBFRRR")
        self.assertEqual(b_pass.row, 70)
        self.assertEqual(b_pass.column, 7)
        self.assertEqual(b_pass.seat_id, 567)

    def test_boarding_passes_A_2(self):
        b_pass = BoardingPass("FFFBBBFRRR")
        self.assertEqual(b_pass.row, 14)
        self.assertEqual(b_pass.column, 7)
        self.assertEqual(b_pass.seat_id, 119)

    def test_boarding_passes_A_3(self):
        b_pass = BoardingPass("BBFFBBFRLL")
        self.assertEqual(b_pass.row, 102)
        self.assertEqual(b_pass.column, 4)
        self.assertEqual(b_pass.seat_id, 820)

    def test_example_a(self):
        expected = 820
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)
