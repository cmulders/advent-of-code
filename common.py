import enum
import logging
import pathlib
import shutil
import unittest
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO)

INPUT_FOLDER = Path.cwd() / "input"
TOKEN = (Path.cwd() / ".aoc_token").read_text()


def fetch_puzzle_input(year, day) -> Path:
    year = int(year)
    day = int(day)
    out_dir = INPUT_FOLDER / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"day_{day}.dat"

    if not output.exists():
        url = f"https://adventofcode.com/{year}/day/{day}/input"

        logging.info(url)

        with requests.get(url, cookies={"session": TOKEN}) as response:
            output.write_text(response.text)

    return output


class PuzzleType(enum.Enum):
    A = "A"
    B = "B"

    def __str__(self):
        return self.value


class Puzzle:
    year: int = None
    day: int = None
    variation: PuzzleType = None

    def __init__(self, input=None):
        if input is None:
            self.input = fetch_puzzle_input(year=self.year, day=self.day).read_text()
        else:
            self.input = input

    @classmethod
    def puzzle_id(cls):
        return (cls.year, cls.day, cls.variation)
    
    @classmethod
    def valid_puzzle(cls):
        return all(cls.puzzle_id())

    def prepare_input(self, input: str):
        return input

    def handle(self, input: str):
        raise NotImplementedError

    def exec(self):
        assert self.year and self.day, "Fill in year and day"
        prepped = self.prepare_input(self.input)
        output = self.handle(prepped)
        return output
