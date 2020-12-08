import copy
import functools
import itertools
import operator
import unittest
from typing import List

from common import Puzzle, PuzzleType


class AsmRunner:
    def __init__(self, instr: List[str]) -> None:
        self.instr = [i.split(" ", maxsplit=2) for i in instr]
        self.instr_i = 0
        self.acc = 0

    def __copy__(self):
        newone = type(self)("")
        newone.instr = list(self.instr)
        return newone

    @property
    def is_eop(self):  # End or program
        return self.instr_i >= len(self.instr)

    def step(self):

        instr = self.instr[self.instr_i]

        handler_fn = getattr(self, f"handle_{instr[0]}")
        handler_fn(instr[1])

        return not self.is_eop

    def handle_nop(self, *args):
        self.instr_i += 1

    def handle_acc(self, value):
        self.acc += int(value)
        self.instr_i += 1

    def handle_jmp(self, value):
        self.instr_i += int(value)


class CommonDay(Puzzle):
    year = 2020
    day = 8
    variation = None

    def prepare_input(self, input: str):
        return AsmRunner(input.splitlines())


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: AsmRunner):
        visited = set()
        while input.step():
            instr_i = input.instr_i
            if instr_i in visited:
                return input.acc
            visited.add(instr_i)


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: AsmRunner):
        orig = input

        to_check = [
            idx
            for idx, (instr, val) in enumerate(orig.instr)
            if instr in ["nop", "jmp"]
        ]

        for i in to_check:
            clone = copy.copy(orig)
            instr, val = clone.instr[i]
            clone.instr[i] = ("nop" if instr == "jmp" else "jmp", val)

            visited = set()
            while clone.step() and clone.instr_i not in visited:
                visited.add(clone.instr_i)

            if clone.is_eop:
                return clone.acc

        raise Exception("Not found")


class TestPuzzle(unittest.TestCase):
    INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

    def test_example_a(self):
        expected = 5
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = 8
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, expected)
