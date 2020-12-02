import typing

class Point:
    __slots__ = ['x', 'y', 'z', ]
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_tuple(cls, t):
        return cls(*t)

    def __hash__(self):
        return hash(self.to_tuple())

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.to_tuple() == other.to_tuple()
        elif isinstance(other, tuple):
            return self == Point.from_tuple(other)
        
        return False

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, tuple):
            return self + Point.from_tuple(other)
        raise TypeError
    
    def __radd__(self, other):
        if isinstance(other, (Point, tuple)):
            return self + other
        
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, tuple):
            return self - Point.from_tuple(other)
        raise TypeError
    
    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, tuple):
            return self * Point.from_tuple(other)
        raise TypeError
    
    def __rmul__(self, other):
        return self * other
    
    def __iter__(self):
        return iter(self.to_tuple())

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.z})'
    
    def manhatten_distance(self, other):
        return sum(abs(i) for i in (self - other))
    
    @staticmethod
    def static_manhatten_distance(a, b):
        return a.manhatten_distance(b)
    
class PointList(list):
    def __add__(self, other):
        if isinstance(other, Point):
            self.append(other)
            return self
        else:
            return super().__add__(other)

    def __hash__(self):
        return hash(tuple(self))