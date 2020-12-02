import unittest

from shared import intcode
from . import common

class TestDay10(unittest.TestCase):
    def test_example1(self):
        input = """.#..#
.....
#####
....#
...##"""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(3, 4))
        self.assertEqual(asteroids, 8)
    
    def test_example2(self):
        input = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(5, 8))
        self.assertEqual(asteroids, 33)
    
    def test_example2(self):
        input = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(1, 2))
        self.assertEqual(asteroids, 35)
        
    
    def test_example3(self):
        input = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(6, 3))
        self.assertEqual(asteroids, 41)
    
    def test_example4(self):
        input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(11, 13))
        self.assertEqual(asteroids, 210)

    def test_example5(self):
        input = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        self.assertEqual(location, common.Point(8, 3))
        self.assertEqual(asteroids, 30)

        vaporizer = common.vaporizer(grid, location)

        self.assertEqual(next(vaporizer), common.Point(8, 1))
        self.assertEqual(next(vaporizer), common.Point(9, 0))
        self.assertEqual(next(vaporizer), common.Point(9, 1))
        self.assertEqual(next(vaporizer), common.Point(10, 0))
        self.assertEqual(next(vaporizer), common.Point(9, 2))
        self.assertEqual(next(vaporizer), common.Point(11, 1))
        self.assertEqual(next(vaporizer), common.Point(12, 1))
        self.assertEqual(next(vaporizer), common.Point(11, 2))
        self.assertEqual(next(vaporizer), common.Point(15, 1))

        self.assertEqual(next(vaporizer), common.Point(12, 2))
        self.assertEqual(next(vaporizer), common.Point(13, 2))
        self.assertEqual(next(vaporizer), common.Point(14, 2))
        self.assertEqual(next(vaporizer), common.Point(15, 2))
        self.assertEqual(next(vaporizer), common.Point(12, 3))
        self.assertEqual(next(vaporizer), common.Point(16, 4))
        self.assertEqual(next(vaporizer), common.Point(15, 4))
        self.assertEqual(next(vaporizer), common.Point(10, 4))
        self.assertEqual(next(vaporizer), common.Point(4, 4))

    def test_example6(self):
        input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
        grid = [list(line) for line in input.splitlines()]
        
        location, asteroids = common.find_best(grid)
        
        vaporizer = common.vaporizer(grid, location)

        shots = list(vaporizer)

        self.assertEqual(shots[1 - 1],  common.Point(11,12))
        self.assertEqual(shots[2 - 1],  common.Point(12,1))
        self.assertEqual(shots[3 - 1],  common.Point(12,2))
        self.assertEqual(shots[10 - 1],  common.Point(12,8))
        self.assertEqual(shots[20 - 1],  common.Point(16,0))
        self.assertEqual(shots[50 - 1],  common.Point(16,9))
        self.assertEqual(shots[100 - 1],  common.Point(10,16))
        self.assertEqual(shots[199 - 1],  common.Point(9,6))
        self.assertEqual(shots[200 - 1],  common.Point(8,2))
        self.assertEqual(shots[201 - 1],  common.Point(10,9))
        self.assertEqual(shots[299 - 1],  common.Point(11,1))

        self.assertEqual(shots[200 - 1].toHash(),  802)

if __name__ == '__main__':
    unittest.main()    
