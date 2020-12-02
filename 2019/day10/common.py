import collections
import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def angle(self, other):
        deltax = self.x - other.x
        deltay = self.y - other.y
        angle = math.atan2(deltax, deltay)
        angle %= 2*math.pi
        return round(angle, 8)
    
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self):
        return str(self)

    def toHash(self):
        return self.x * 100 + self.y

def parse_grid(grid):
    lookup = set()
    for y, line in enumerate(grid):
        for x, obj in enumerate(line):
            if obj == '#':
                lookup.add(Point(x, y))
    return lookup

def find_best(grid):
    lookup = parse_grid(grid)

    distances = collections.defaultdict(lambda: collections.defaultdict(dict))
    for main in lookup:
        for alternate in sorted([a for a in lookup if not a == main], key=lambda x: main.distance(x), reverse=True):
            distances[main][main.angle(alternate)] = alternate

    counts = [
        (obj, len(others.keys())) 
        for obj, others in distances.items()
    ]

    point, count = max(counts, key=lambda x: x[1])
    return point, count

def vaporizer(grid, location):
    angle = 0

    asteroids = parse_grid(grid)
    asteroids.remove(location)

    last_angle = None

    while asteroids:

        angles = {
            location.angle(a): a
            for a in sorted(asteroids, key=lambda x: location.distance(x), reverse=True)
        }

        if len(angles) == 1:
            last_angle = None
        
        if not any(a <= angle for a in angles.keys() if a != last_angle):
            angle += 2 * math.pi
        
        closest = max(a for a in angles.keys() if a <= angle and a != last_angle)
        last_angle = angle = closest
        
        closest_asteroid = angles[angle]
        asteroids.remove(closest_asteroid)
        yield closest_asteroid