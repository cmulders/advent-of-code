import argparse
import importlib
import inspect
import operator
import unittest
from operator import attrgetter
from typing import List, Type

from common import Puzzle, PuzzleType


def find_puzzle_module(year, day):
    try:
        return importlib.import_module(f"{year}.day_{day}")
    except ImportError:
        raise ImportError(f"Puzzle code for {year}-{day} was not found.")
    except SyntaxError:
        raise SyntaxError(f"Puzzle code for {year}-{day} is invalid.")


def import_puzzles(module) -> List[Type[Puzzle]]:
    return [
        getattr(module, name)
        for name in dir(module)
        if inspect.isclass(getattr(module, name))
        and issubclass(getattr(module, name), Puzzle)
    ]


def filter_puzzles(puzzles, year, day, variation=None) -> Type[Puzzle]:

    candidates = list()

    for cls in puzzles:
        puzzle_id = cls.puzzle_id()
        if not cls.valid_puzzle():
            continue

        if year is not None and puzzle_id[0] != year:
            continue

        if day is not None and puzzle_id[1] != day:
            continue

        if variation is not None and puzzle_id[2] != variation:
            continue

        candidates.append(cls)

    if len(candidates) == 0:
        raise ValueError(f"Could not find puzzle: {year}-{day}-{variation}")
    return candidates


def exec_puzzle(cls):
    output = cls().exec()
    print("Puzzle: ", " ".join(map(str, cls.puzzle_id())))
    print("Output:", output)
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", choices=range(1, 26), type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--variation", "-v", required=False, type=PuzzleType, choices=list(PuzzleType)
    )
    group.add_argument("--test", "-t", action="store_true")

    options = parser.parse_args()

    module = find_puzzle_module(options.year, options.day)

    if options.test:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner().run(suite)
    else:
        puzzles = import_puzzles(module)
        filt = filter_puzzles(puzzles, options.year, options.day, options.variation)
        for puzzle in filt:
            exec_puzzle(puzzle)


if __name__ == "__main__":
    main()
