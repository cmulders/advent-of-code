import unittest
import itertools

from . import common

class TestDay16(unittest.TestCase):
    def test_phase_generator(self):
        self.assertEqual(list(itertools.islice(common.phase_generator(0), 8)), [1, 0, -1, 0, 1,  0,  -1,  0])
        self.assertEqual(list(itertools.islice(common.phase_generator(1), 8)), [0, 1,  1, 0, 0, -1,  -1,  0])
        self.assertEqual(list(itertools.islice(common.phase_generator(2), 8)), [0, 0,  1, 1, 1,  0,   0,  0])
        self.assertEqual(list(itertools.islice(common.phase_generator(3), 8)), [0, 0,  0, 1, 1,  1,   1,  0])
        self.assertEqual(list(itertools.islice(common.phase_generator(4), 8)), [0, 0,  0, 0, 1,  1,   1,  1])
        self.assertEqual(list(itertools.islice(common.phase_generator(5), 8)), [0, 0,  0, 0, 0,  1,   1,  1])
        self.assertEqual(list(itertools.islice(common.phase_generator(6), 8)), [0, 0,  0, 0, 0,  0,   1,  1])
        self.assertEqual(list(itertools.islice(common.phase_generator(7), 8)), [0, 0,  0, 0, 0,  0,   0,  1])


    def test_example(self):
        input = '12345678'

        phase1 = common.fft(input)
        self.assertEqual('48226158', phase1)

        phase2 = common.fft(phase1)
        self.assertEqual('34040438', phase2)

        phase3 = common.fft(phase2)
        self.assertEqual('03415518', phase3)

        phase4 = common.fft(phase3)
        self.assertEqual('01029498', phase4)

    def test_example_large_1(self):
        input = '03036732577212944063491565474664'
        offset = int(input[:7])
        message = input * 10000
        self.assertEqual(common.repeat_fft(message, 100, offset=offset)[offset:][:8], '84462026')

    def test_example_large_2(self):
        input = '02935109699940807407585447034323'
        offset = int(input[:7])
        message = input * 10000
        self.assertEqual(common.repeat_fft(message, 100, offset=offset)[offset:][:8], '78725270')

    def test_example_large_3(self):
        input = '03081770884921959731165446850517'
        offset = int(input[:7])
        message = input * 10000
        self.assertEqual(common.repeat_fft(message, 100, offset=offset)[offset:][:8], '53553731')

if __name__ == '__main__':
    unittest.main()    
