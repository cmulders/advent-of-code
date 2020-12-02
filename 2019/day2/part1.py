import os

scriptpath = os.path.dirname(os.path.realpath(__file__))

INPUT = "input.txt"

buffer = list(map(int, open(os.path.join(scriptpath, INPUT), 'r').read().split(',')))

#purposes mods:
buffer[1] = 12
buffer[2] = 2

op_position = 0
opcode = buffer[op_position]
while opcode != 99:
    opcode, pos1, pos2, dest = buffer[op_position:op_position+4]
    print(opcode, pos1, pos2, dest)
    n1, n2 = buffer[pos1], buffer[pos2]

    if opcode == 1:
        # Add 
        result = n1 + n2
        buffer[dest] = result
    elif opcode == 2:
        # Multiply
        result = n1 * n2
        buffer[dest] = result

    op_position += 4
    opcode = buffer[op_position]

print(buffer)