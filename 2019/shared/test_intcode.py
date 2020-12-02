import unittest
import copy

from .intcode import IntCode

class TestIntCodeFeatures(unittest.TestCase):
    def test_input_output(self):        
        for i in range(-10, 10):
            vm  = IntCode([3,0,4,0,99])
            vm.stdin.write(i)

            vm.run_to_halt()

            self.assertEqual(vm.stdout.read(), i)
            # After reading a value, it should be empty
            self.assertEqual(len(vm.stdout), 0)
    
    def test_parameter_immediate_mode(self):
        vm  = IntCode([1101,100,-1,4,0])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [1101,100,-1,4,99])
        
    def test_parameter_mixed_mode(self):
        vm  = IntCode([1002,4,3,4,33])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [1002,4,3,4,99])

    def test_comparision_equals_position(self):
        # Using position mode, consider whether the input is equal to 8; 
        # output 1 (if it is) or 0 (if it is not).
        vm  = IntCode([3,9,8,9,10,9,4,9,99,-1,8])
        vm.stdin.write(8)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

        vm  = IntCode([3,9,8,9,10,9,4,9,99,-1,8])
        vm.stdin.write(7)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

    def test_comparision_lessthan_position(self):
        # Using position mode, consider whether the input is less than 8; 
        # output 1 (if it is) or 0 (if it is not).
        vm  = IntCode([3,9,7,9,10,9,4,9,99,-1,8])
        vm.stdin.write(7)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

        vm  = IntCode([3,9,7,9,10,9,4,9,99,-1,8])
        vm.stdin.write(8)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

    def test_comparision_equals_immediate(self):
        # Using immediate mode, consider whether the input is equal to 8; 
        # output 1 (if it is) or 0 (if it is not).
        vm  = IntCode([3,3,1108,-1,8,3,4,3,99])
        vm.stdin.write(8)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

        vm  = IntCode([3,3,1108,-1,8,3,4,3,99])
        vm.stdin.write(7)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

    def test_comparision_lessthan_immediate(self):
        # Using immediate mode, consider whether the input is less than 8; 
        # output 1 (if it is) or 0 (if it is not).
        vm  = IntCode([3,3,1107,-1,8,3,4,3,99])
        vm.stdin.write(7)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

        vm  = IntCode([3,3,1107,-1,8,3,4,3,99])
        vm.stdin.write(8)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

    def test_jump_postion_mode(self):
        # Here are some jump tests that take an input, then output 0 if the input was zero or 
        # 1 if the input was non-zero:
        vm  = IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        vm.stdin.write(0)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

        vm  = IntCode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        vm.stdin.write(1)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

    def test_jump_immediate_mode(self):
        # Here are some jump tests that take an input, then output 0 if the input was zero or 
        # 1 if the input was non-zero:
        vm  = IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        vm.stdin.write(0)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 0)

        vm  = IntCode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        vm.stdin.write(1)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1)

    def test_relative_mode(self):
        bytecode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        vm  = IntCode(bytecode)
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read_all(), bytecode)

    def test_16bit_number(self):
        # should output a 16-digit number.
        vm  = IntCode([1102,34915192,34915192,7,4,7,99,0])
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1219070632396864)
    
    def test_large_number(self):
        # should output the large number in the middle.
        vm  = IntCode([104,1125899906842624,99])
        vm.run_to_halt()
        self.assertEqual(vm.stdout.read(), 1125899906842624)
    
    def assertVMInputToExpected(self, input, output):
        vm  = IntCode(input)
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, output)

    def test_day1_examples(self):
        vm  = IntCode([1,0,0,0,99])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [2,0,0,0,99])
        
        vm  = IntCode([2,3,0,3,99])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [2,3,0,6,99])
        
        vm  = IntCode([2,4,4,5,99,0])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [2,4,4,5,99,9801])
        
        vm  = IntCode([1,1,1,4,99,5,6,0,99])
        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [30,1,1,4,2,5,6,0,99])
    
    def test_copy(self):
        vm  = IntCode([1,1,1,4,99,5,6,0,99])
        vm.run_step()
        vm_clone = copy.copy(vm)
        vm.run_step()
        
        self.assertNotEqual(vm.buffer, vm_clone.buffer)
        vm_clone.run_step()
        self.assertEqual(vm.buffer, vm_clone.buffer)

        vm.run_to_halt()
        self.assertListEqual(vm.buffer, [30,1,1,4,2,5,6,0,99])
        
        vm_clone.run_to_halt()
        self.assertListEqual(vm_clone.buffer, [30,1,1,4,2,5,6,0,99])
        

        
if __name__ == '__main__':
    unittest.main()