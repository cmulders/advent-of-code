import unittest

from shared import intcode
from . import common

class TestDay8(unittest.TestCase):
    def test_example1(self):
        pixels = list(map(int,"""123456789012"""))
        
        layers = common.create_layes(pixels, 3, 2)
        layer  = common.find_fewest_zeros(layers)
        hashed = common.calculate_one_two_hash(layer)
        self.assertEqual(hashed, 1)
    
    def test_example2(self):
        pixels = list(map(int,"""0222112222120000"""))
        
        layers = common.create_layes(pixels, 2, 2)
        rendered  = common.render(layers)
        
        self.assertEqual(rendered, [0, 1, 1, 0])


if __name__ == '__main__':
    unittest.main()    
