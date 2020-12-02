import unittest

from .math import Point

class TestPoint(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Point(x=1, y=1, z=1), Point.from_tuple((1,1,1)))
    
    def test_eq(self):
        self.assertEqual(Point(x=1, y=1, z=1), (1,1,1))
        self.assertNotEqual(Point(x=1, y=1, z=1), Point(x=1, y=2, z=1))

        self.assertEqual(Point(x=1, y=1, z=1), (1,1,1))
        self.assertNotEqual(Point(x=1, y=1, z=1), (1,2,1))
    
    def test_add(self):
        p1 = Point(x=1, y=2, z=6)
        p2 = Point(x=2, y=3, z=7)
        p3 = Point(x=3, y=5, z=13)
        self.assertEqual(p1 + p2, p3)
    
    def test_radd(self):
        p1 = (1, 2, 6)
        p2 = Point(x=2, y=3, z=7)
        p3 = Point(x=3, y=5, z=13)
        self.assertEqual(p1 + p2, p3)

    def test_mul(self):
        p1 = Point(x=2, y=3, z=4)
        p2 = Point(x=2, y=3, z=4)
        p3 = Point(x=4, y=9, z=16)
        self.assertEqual(p1 * p2, p3)
    
    def test_rmul(self):
        p1 = (2, 3, 4)
        p2 = Point(x=2, y=3, z=4)
        p3 = Point(x=4, y=9, z=16)
        self.assertEqual(p1 * p2, p3)
            
if __name__ == '__main__':
    unittest.main()