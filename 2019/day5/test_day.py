import unittest

from shared import intcode

class TestDay5(unittest.TestCase):
    def test_example(self):
        vm  = intcode.IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        vm.stdin.write(7)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 999)

        vm  = intcode.IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        vm.stdin.write(8)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1000)

        vm  = intcode.IntCode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        vm.stdin.write(9)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1001)


if __name__ == '__main__':
    unittest.main()    
