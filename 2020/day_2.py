import re
import unittest

from common import Puzzle, PuzzleType


class CommonDay(Puzzle):
    year = 2020
    day = 2
    variation = None

    def prepare_input(self, input: str):
        parser = re.compile("^(\d+)-(\d+) ([a-z]): ([a-z]+)$")
        for line in input.splitlines():
            match = parser.fullmatch(line)
            if not match:
                raise ValueError(f"Could not match {line}")

            c_min, c_max, c, password = match.groups()
            yield int(c_min), int(c_max), c, password.strip()

    def handle(self, input: str):
        return sum(1 for password in input if self.is_valid(*password))


class PuzzleA(CommonDay):
    """
    Validate the passwords with the rule stating the number of
    occurences of the char
    """

    variation = PuzzleType.A

    def is_valid(self, c_min: int, c_max: int, c: str, password: str):
        return c_min <= password.count(c) <= c_max


class PuzzleB(CommonDay):
    """
    Validate the passwords with the rule by checking that only one of
    the positions (1-indexed) is the char
    """

    variation = PuzzleType.B

    def is_valid(self, c_min: int, c_max: int, c: str, password: str):
        return (password[c_min - 1] == c) ^ (password[c_max - 1] == c)


class TestPuzzle(unittest.TestCase):
    INPUT = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    def test_example_a(self):
        expected = 2
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = 1
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, expected)
