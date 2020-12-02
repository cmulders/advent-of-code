import unittest

from shared import intcode
from .common import split_edges, count_orbits, count_transfers

class TestDay6(unittest.TestCase):
    def test_example1(self):
        edges_raw = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
        edges = split_edges(edges_raw)

        self.assertEqual(count_orbits(edges), 42)        

    def test_example2(self):
        edges_raw = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
        edges = split_edges(edges_raw)

        self.assertEqual(count_transfers(edges, 'YOU', 'SAN'), 4)  


if __name__ == '__main__':
    unittest.main()    
