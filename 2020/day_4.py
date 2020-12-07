import dataclasses
import functools
import itertools
import operator
import re
import unittest
from typing import Dict, Iterable

from common import Puzzle, PuzzleType


@dataclasses.dataclass
class Passport:
    byr: str = ""  # (Birth Year)
    iyr: str = ""  # (Issue Year)
    eyr: str = ""  # (Expiration Year)
    hgt: str = ""  # (Height)
    hcl: str = ""  # (Hair Color)
    ecl: str = ""  # (Eye Color)
    pid: str = ""  # (Passport ID)
    cid: str = ""  # (Country ID)

    def valid_fields(self):
        field_getter = operator.attrgetter(
            "byr",
            "iyr",
            "eyr",
            "hgt",
            "hcl",
            "ecl",
            "pid",
        )
        return all(field_getter(self))

    def valid_values(self):
        return all(
            [
                self.validate_byr(),
                self.validate_iyr(),
                self.validate_eyr(),
                self.validate_hgt(),
                self.validate_hcl(),
                self.validate_ecl(),
                self.validate_pid(),
                self.validate_cid(),
            ]
        )

    def validate_byr(self):
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        return self.byr.isdigit() and 1920 <= int(self.byr) <= 2002

    def validate_iyr(self):
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        return self.iyr.isdigit() and 2010 <= int(self.iyr) <= 2020

    def validate_eyr(self):
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        return self.eyr.isdigit() and 2020 <= int(self.eyr) <= 2030

    def validate_hgt(self):
        # hgt (Height) - a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        if self.hgt[-2:] == "cm":
            return self.hgt[:-2].isdigit() and 150 <= int(self.hgt[:-2]) <= 193
        elif self.hgt[-2:] == "in":
            return self.hgt[:-2].isdigit() and 59 <= int(self.hgt[:-2]) <= 76

    def validate_hcl(self):
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        return bool(re.match("#[0-9a-f]{6}", self.hcl))

    def validate_ecl(self):
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        return self.ecl in "amb blu brn gry grn hzl oth".split()

    def validate_pid(self):
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        return len(self.pid) == 9 and self.pid.isdigit()

    def validate_cid(self):
        # cid (Country ID) - ignored, missing or not.
        return True


class CommonDay(Puzzle):
    year = 2020
    day = 4
    variation = None

    def prepare_input(self, input: str):
        data = Passport()
        for line in input.splitlines():
            if not line:
                yield data
                data = Passport()

            fields = line.split()
            for key, val in [field.split(":", maxsplit=1) for field in fields]:
                setattr(data, key, val)
        yield data


class PuzzleA(CommonDay):
    """"""

    variation = PuzzleType.A

    def handle(self, input: Iterable[Passport]):
        return sum(p.valid_fields() for p in input)


class PuzzleB(CommonDay):
    """"""

    variation = PuzzleType.B

    def handle(self, input: Iterable[Passport]):
        return sum(p.valid_fields() and p.valid_values() for p in input)


class TestPuzzle(unittest.TestCase):
    INPUT = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

    INPUT_INVALID_B = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

    INPUT_VALID_B = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

    def test_example_a(self):
        expected = 2
        result = PuzzleA(self.INPUT).exec()

        self.assertEqual(result, expected)

    def test_example_b_invalid(self):
        expected = 0
        result = PuzzleB(self.INPUT_INVALID_B).exec()

        self.assertEqual(result, expected)

    def test_example_b_valid(self):
        expected = 4
        result = PuzzleB(self.INPUT_VALID_B).exec()

        self.assertEqual(result, expected)

    def test_field_validation(self):
        # byr valid:   2002
        self.assertTrue(Passport(byr="2002").validate_byr())
        # byr invalid: 2003
        self.assertFalse(Passport(byr="2003").validate_byr())

        # hgt valid:   60in
        self.assertTrue(Passport(hgt="60in").validate_hgt())
        # hgt valid:   190cm
        self.assertTrue(Passport(hgt="190cm").validate_hgt())
        # hgt invalid: 190in
        self.assertFalse(Passport(hgt="190in").validate_hgt())
        # hgt invalid: 190
        self.assertFalse(Passport(hgt="190").validate_hgt())

        # hcl valid:   #123abc
        self.assertTrue(Passport(hcl="#123abc").validate_hcl())
        # hcl invalid: #123abz
        self.assertFalse(Passport(hcl="#123abz").validate_hcl())
        # hcl invalid: 123abc
        self.assertFalse(Passport(hcl="123abc").validate_hcl())

        # ecl valid:   brn
        self.assertTrue(Passport(ecl="brn").validate_ecl())
        # ecl invalid: wat
        self.assertFalse(Passport(ecl="wat").validate_ecl())

        # pid valid:   000000001
        self.assertTrue(Passport(pid="000000001").validate_pid())
        # pid invalid: 0123456789
        self.assertFalse(Passport(pid="0123456789").validate_pid())
