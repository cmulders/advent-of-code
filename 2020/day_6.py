import collections
import functools
import itertools
import operator
import unittest
from typing import Iterable, Tuple

from common import Puzzle, PuzzleType


class CommonDay(Puzzle):
    year = 2020
    day = 6
    variation = None

    def prepare_input(self, input: str):
        counts = []
        for line in input.splitlines():
            if not line:
                yield counts
                counts.clear()
                group_size = 0
            else:
                counts.append(collections.Counter(line))
        yield counts


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: Iterable[Tuple[int, dict]]):
        return sum(
            len(sum(counts, start=collections.Counter()).keys()) for counts in input
        )


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: str):
        total = 0
        for counts in input:
            counter = sum(counts, start=collections.Counter())
            total += len(
                [key for key, count in counter.items() if len(counts) == count]
            )
        return total


class TestPuzzle(unittest.TestCase):
    INPUT = """abc

a
b
c

ab
ac

a
a
a
a

b"""

    def test_example_a(self):
        expected = 11
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = 6
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, expected)
