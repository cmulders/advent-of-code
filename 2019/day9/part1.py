import os
from shared import intcode

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

buffer = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))

def main():
    vm = intcode.IntCode(buffer)
    vm.stdin.write(1)
    vm.run_to_halt()
    
    print(vm.stdout.read_all())
    

if __name__ == "__main__":
    # execute only if run as a script
    main()