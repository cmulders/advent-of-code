import collections
import functools
import itertools
import operator
import re
import unittest

from common import Puzzle, PuzzleType


class CommonDay(Puzzle):
    year = 2020
    day = 7
    variation = None

    def prepare_input(self, input: str):
        graph = dict()
        for line in input.splitlines():
            if "contain no other bags" in line:
                col1, col2, *_ = line.split()
                graph[f"{col1} {col2}".strip()] = []
                continue

            head, others = line.split("bags contain")
            others = others.split(",")

            graph[head.strip()] = [
                (int(i), f"{col1} {col2}".strip())
                for (i, col1, col2, *_) in map(str.split, others)
            ]

        return graph


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: dict):
        inv_graph = collections.defaultdict(list)
        for key, items in input.items():
            for i, col in items:
                inv_graph[col].append(key)

        containers = set()
        to_visit = collections.deque(inv_graph["shiny gold"])
        while to_visit:
            cur = to_visit.popleft()
            containers.add(cur)
            to_visit.extend(inv_graph[cur])

        return len(containers)


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: str):
        containers = list()
        to_visit = collections.deque(input["shiny gold"])
        while to_visit:
            c, cur = to_visit.popleft()
            containers.extend([cur] * c)
            to_visit.extend(input[cur] * c)

        return len(containers)


class TestPuzzle(unittest.TestCase):
    INPUT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

    INPUT_B = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

    def test_example_a(self):
        expected = 4
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b(self):
        expected = 32
        result = PuzzleB(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b2(self):
        expected = 126
        result = PuzzleB(self.INPUT_B).exec()

        self.assertEqual(result, expected)
