import operator
import itertools
import functools
import re
import functools

def cmp(a, b):
    return int(a>b) - int(a<b)

body_string_pattern = re.compile("^(pos=)?<x=\s*(?P<x>-?\d*), y=\s*(?P<y>-?\d*), z=\s*(?P<z>-?\d*)>(, vel=<x=\s*(?P<dx>-?\d*), y=\s*(?P<dy>-?\d*), z=\s*(?P<dz>-?\d*)>)?$")

@functools.total_ordering
class Body():
    def __init__(self, x, y, z, dx=0, dy=0, dz=0):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.dx = int(dx or 0)
        self.dy = int(dy or 0)
        self.dz = int(dz or 0)
    
    def move(self):
        self.x += self.dx 
        self.y += self.dy 
        self.z += self.dz 

    def gravity(self, other):
        assert isinstance(other, Body)

        for axis, daxis in [('x', 'dx'), ('y', 'dy'), ('z', 'dz')]:
            axis_get = operator.attrgetter(axis)
            delta = cmp(axis_get(other), axis_get(self)) # Compare to -1, 0 or +1
            new_delta = getattr(self, daxis) + delta
            setattr(self, daxis, new_delta) 

    @property
    def energy(self):
        potential = (self.x, self.y, self.z)
        kinetic = (self.dx, self.dy, self.dz)
        return sum(map(abs, potential)) * sum(map(abs, kinetic))

    def to_tuple(self):
        return (self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def __hash__(self):
        return hash(self.to_tuple())

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def __repr__(self):
        return f'Body(pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.dx}, y={self.dy}, z={self.dz}>)'
    
    def clone(self):
        return Body(*self.to_tuple())

    @classmethod
    def from_str(cls, body_str):
        m = body_string_pattern.fullmatch(body_str.strip())
        if not m:
            raise Exception('Invalid body str')
        return cls(**m.groupdict())

class BodySystem():
    def __init__(self, *bodies):
        self.initial_state = []
        self.bodies = []
        self.periods = {
            'x': None,
            'y': None,
            'z': None,
        }
        self.step_count = 0
        
        for b in bodies:
            self.add_body(b)
    
    def add_body(self, body):
        assert self.step_count == 0
        assert isinstance(body, Body)
        self.bodies.append(body)
    
    def apply_gravity(self):
        for b1, b2 in itertools.permutations(self.bodies, 2):
            b1.gravity(b2)

    def apply_velocity(self):
        for body in self.bodies:
            body.move()

    def check_period(self):
        for axis, daxis in [('x', 'dx'), ('y', 'dy'), ('z', 'dz')]:
            axis_get = operator.attrgetter(axis)
            daxis_get = operator.attrgetter(daxis)
            initial = [(axis_get(b), daxis_get(b)) for b in self.initial_state]
            current = [(axis_get(b), daxis_get(b)) for b in self.bodies]
            if initial == current and not self.periods[axis]:
                self.periods[axis] = self.step_count

    @property
    def energy(self):
        return sum([b.energy for b in self.bodies])

    def step_periods(self):
        while not all(self.periods.values()):
            self.step()

    def step_n(self, n=1):
        for d in range(n):
            self.step()

    def step(self):
        if self.step_count == 0:
            self.initial_state = [b.clone() for b in self.bodies]
        self.step_count += 1
            
        self.apply_gravity()
        self.apply_velocity()
        self.check_period()
    
    def __hash__(self):
        return hash(self.bodies)

    def __eq__(self, other):
        return sorted(self.bodies) == sorted(other.bodies)

    @classmethod
    def from_bodies(cls, *bodies):
        new = cls()
        for b_str in bodies:
            new.add_body(Body.from_str(b_str))
        return new
    
    @classmethod
    def from_lines(cls, lines: str):
        return cls.from_bodies(*filter(bool, lines.splitlines()))
    
    def __repr__(self):
        return "System(\n{}\n)".format('\n'.join(repr(b) for b in self.bodies))
        

def apply_gravity(*bodies):
    for b1, b2 in itertools.permutations(bodies, 2):
        b1.gravity(b2)

def apply_velocity(*bodies):
    for body in bodies:
        body.move()

def simulate_step(*bodies):
    apply_gravity(*bodies)
    apply_velocity(*bodies)

def gcd(a, b):
        if b > a:
            #Make a the largest
            a, b = b, a
        
        while b != 0:
            a, b = b, a % b
        
        return a

def lcm(a, b):
    # Special cases to short circuit
    if a is None: return b
    if b is None: return a

    if a < 0 or b < 0:
        raise NotImplementedError('Only positive factors supported')

    return a * b // gcd(a, b)
        

def many_lcm(*factors):
    return functools.reduce(lcm, factors, None)
        
