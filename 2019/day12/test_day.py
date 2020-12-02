import unittest

from . import common

class TestDay12(unittest.TestCase):
    def assertSystem(self, system, systemstr):
        other_system = common.BodySystem.from_lines(systemstr)
        self.assertEqual(system, other_system)

    def assertBody(self, body, bodystr):
        self.assertEqual(body, common.Body.from_str(bodystr))

    def test_body_str(self):
        self.assertEqual(common.Body.from_str('pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>'), common.Body(5, -3, -1,  3,-2,-2))
        self.assertEqual(common.Body.from_str('pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>'), common.Body(1, -2,  2, -2, 5,  6))
        self.assertEqual(common.Body.from_str('pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>'), common.Body(1, -4, -1,  0, 3, -6))
        self.assertEqual(common.Body.from_str('pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>'), common.Body(1, -4,  2, -1,-6, 2))

        self.assertEqual(common.Body.from_str('<x=-1, y=0, z=2>'), common.Body(-1, 0, 2))
        self.assertEqual(common.Body.from_str('<x=2, y=-10, z=-7>'), common.Body(2, -10, -7))
        self.assertEqual(common.Body.from_str('<x=4, y=-8, z=8>'), common.Body(4, -8, 8))
        self.assertEqual(common.Body.from_str('<x=3, y=5, z=-1>'), common.Body(3, 5, -1))

    def test_body(self):
        b1 = common.Body(3, 0, 0)
        b2 = common.Body(5, 0, 0)
        
        b1.gravity(b2)
        b2.gravity(b1)

        self.assertEqual(b1.dx, 1)
        self.assertEqual(b2.dx, -1)

    def test_simulate(self):
        b1 = common.Body.from_str('<x=-1, y=0, z=2>')
        b2 = common.Body.from_str('<x=2, y=-10, z=-7>')
        b3 = common.Body.from_str('<x=4, y=-8, z=8>')
        b4 = common.Body.from_str('<x=3, y=5, z=-1>')
        bodies = [b1, b2, b3, b4]

        self.assertBody(b1, 'pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b2, 'pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b3, 'pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b4, 'pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>')
        
        common.simulate_step(*bodies)

        self.assertBody(b1, 'pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>')
        self.assertBody(b2, 'pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>')
        self.assertBody(b3, 'pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>')
        self.assertBody(b4, 'pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>')

    def test_example1(self):
        b1 = common.Body.from_str('<x=-1, y=0, z=2>')
        b2 = common.Body.from_str('<x=2, y=-10, z=-7>')
        b3 = common.Body.from_str('<x=4, y=-8, z=8>')
        b4 = common.Body.from_str('<x=3, y=5, z=-1>')
        bodies = [b1, b2, b3, b4]

        self.assertBody(b1, 'pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b2, 'pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b3, 'pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(b4, 'pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>')
        self.assertBody(b2, 'pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>')
        self.assertBody(b3, 'pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>')
        self.assertBody(b4, 'pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>')
        self.assertBody(b2, 'pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>')
        self.assertBody(b3, 'pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>')
        self.assertBody(b4, 'pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>')
        self.assertBody(b2, 'pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>')
        self.assertBody(b3, 'pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>')
        self.assertBody(b4, 'pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>')
        self.assertBody(b2, 'pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>')
        self.assertBody(b3, 'pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>')
        self.assertBody(b4, 'pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>')
        self.assertBody(b2, 'pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>')
        self.assertBody(b3, 'pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>')
        self.assertBody(b4, 'pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>')
        self.assertBody(b2, 'pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>')
        self.assertBody(b3, 'pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>')
        self.assertBody(b4, 'pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>')
        self.assertBody(b2, 'pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>')
        self.assertBody(b3, 'pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>')
        self.assertBody(b4, 'pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>')
        self.assertBody(b2, 'pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>')
        self.assertBody(b3, 'pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>')
        self.assertBody(b4, 'pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>')
        self.assertBody(b2, 'pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>')
        self.assertBody(b3, 'pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>')
        self.assertBody(b4, 'pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>')

        common.apply_gravity(*bodies)
        common.apply_velocity(*bodies)

        self.assertBody(b1, 'pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>')
        self.assertBody(b2, 'pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>')
        self.assertBody(b3, 'pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>')
        self.assertBody(b4, 'pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>')

    def test_system(self):
        system = common.BodySystem.from_lines('''   <x=-1, y=0, z=2>
                                                    <x=2, y=-10, z=-7>
                                                    <x=4, y=-8, z=8>
                                                    <x=3, y=5, z=-1>''')
        
        self.assertBody(system.bodies[0], 'pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(system.bodies[1], 'pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(system.bodies[2], 'pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>')
        self.assertBody(system.bodies[3], 'pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>')

        system.step()

        self.assertBody(system.bodies[0], 'pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>')
        self.assertBody(system.bodies[1], 'pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>')
        self.assertBody(system.bodies[2], 'pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>')
        self.assertBody(system.bodies[3], 'pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>')

        system.step()

        self.assertSystem(system, '''
                        pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
                        pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
                        pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
                        pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>''')
    
    def test_example_energy(self):
        system = common.BodySystem.from_lines('''   <x=-1, y=0, z=2>
                                                    <x=2, y=-10, z=-7>
                                                    <x=4, y=-8, z=8>
                                                    <x=3, y=5, z=-1>''')

        system.step_n(10)

        self.assertSystem(system, '''
                        pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
                        pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
                        pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
                        pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>''')

        self.assertEqual(system.bodies[0].energy, 36)
        self.assertEqual(system.bodies[1].energy, 45)
        self.assertEqual(system.bodies[2].energy, 80)
        self.assertEqual(system.bodies[3].energy, 18)
        self.assertEqual(system.energy, 179)

    def test_example_energy2(self):
        system = common.BodySystem.from_lines('''   <x=-8, y=-10, z=0>
                                                    <x=5, y=5, z=10>
                                                    <x=2, y=-7, z=3>
                                                    <x=9, y=-8, z=-3>''')

        system.step_n(10)
        self.assertEqual(system.step_count, 10)
        self.assertSystem(system, '''
                        pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
                        pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
                        pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
                        pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>''')
        
        system.step_n(10)
        
        self.assertEqual(system.step_count, 20)
        self.assertSystem(system, '''pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
        pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
        pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
        pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 30)
        self.assertSystem(system, '''pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
        pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
        pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
        pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 40)
        self.assertSystem(system, '''pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
        pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
        pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
        pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 50)
        self.assertSystem(system, '''pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
        pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
        pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
        pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 60)
        self.assertSystem(system, '''pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
        pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
        pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
        pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 70)
        self.assertSystem(system, '''pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
        pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
        pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
        pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 80)
        self.assertSystem(system, '''pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
        pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
        pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
        pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 90)
        self.assertSystem(system, '''pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
        pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
        pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
        pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>''')

        system.step_n(10)
        
        self.assertEqual(system.step_count, 100)
        self.assertSystem(system, '''pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
        pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
        pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
        pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>''')

        self.assertEqual(system.energy, 1940)

    def test_period(self):
        system = common.BodySystem.from_lines('''   <x=-8, y=-10, z=0>
                                                    <x=5, y=5, z=10>
                                                    <x=2, y=-7, z=3>
                                                    <x=9, y=-8, z=-3>''')

        system.step_periods()
        self.assertEqual(system.periods, {'x': 2028, 'y': 5898, 'z': 4702})
    
        combined_period = common.many_lcm(*system.periods.values())
        self.assertEqual(combined_period, 4686774924)

    def test_lcm(self):
        self.assertEqual(common.lcm(21,6), 42)
        

if __name__ == '__main__':
    unittest.main()    
