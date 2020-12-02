import os
from itertools import permutations
from shared import intcode

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

buffer = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))

def try_combination(noun, verb):
    local_buf = buffer[:]
    local_buf[1] = noun
    local_buf[2] = verb

    vm = intcode.IntCode(local_buf)

    while not vm.halted:
        vm.run_step()

    return vm

def main():
    for noun, verb in permutations(range(0,100), 2):
        vm = try_combination(noun, verb)
        print(noun, verb, vm.buffer[0])

        if vm.buffer[0] == 19690720:
            print(noun, verb, 100 * noun + verb, vm.buffer[0])
            break
    else:
        raise Exception('Not halted')
    

if __name__ == "__main__":
    # execute only if run as a script
    main()