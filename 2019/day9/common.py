import itertools
from shared import intcode

def run_amplifier(amplifier_code, a, b, c, d, e):
    amp_a = intcode.IntCode(amplifier_code)
    amp_a.stdin.write(a)
    amp_a.stdin.write(0)
    amp_a.run_to_halt()

    amp_b = intcode.IntCode(amplifier_code)
    amp_b.stdin.write(b)
    amp_b.stdin.write(amp_a.stdout.read())
    amp_b.run_to_halt()

    amp_c = intcode.IntCode(amplifier_code)
    amp_c.stdin.write(c)
    amp_c.stdin.write(amp_b.stdout.read())
    amp_c.run_to_halt()

    amp_d = intcode.IntCode(amplifier_code)
    amp_d.stdin.write(d)
    amp_d.stdin.write(amp_c.stdout.read())
    amp_d.run_to_halt()

    amp_e = intcode.IntCode(amplifier_code)
    amp_e.stdin.write(e)
    amp_e.stdin.write(amp_d.stdout.read())
    amp_e.run_to_halt()

    return amp_e.stdout.read()

def looped_amplifier(amplifier_code, a, b, c, d, e):
    pipe_ab = intcode.Pipe()
    pipe_bc = intcode.Pipe()
    pipe_cd = intcode.Pipe()
    pipe_de = intcode.Pipe()
    pipe_ea = intcode.Pipe()
    
    pipe_ea.write(a)
    pipe_ab.write(b)
    pipe_bc.write(c)
    pipe_cd.write(d)
    pipe_de.write(e)

    amp_a = intcode.IntCode(amplifier_code[:], stdin=pipe_ea, stdout=pipe_ab)
    amp_b = intcode.IntCode(amplifier_code[:], stdin=pipe_ab, stdout=pipe_bc)
    amp_c = intcode.IntCode(amplifier_code[:], stdin=pipe_bc, stdout=pipe_cd)
    amp_d = intcode.IntCode(amplifier_code[:], stdin=pipe_cd, stdout=pipe_de)
    amp_e = intcode.IntCode(amplifier_code[:], stdin=pipe_de, stdout=pipe_ea)

    pipe_ea.write(0) # Bootstrap signal

    amps = itertools.cycle([amp_a, amp_b, amp_c, amp_d, amp_e])

    cur_amp = next(amps)
    last_amp_e = 0
    while not all(a.halted for a in [amp_a, amp_b, amp_c, amp_d, amp_e]):
        cur_amp.run_step()
        if cur_amp.halted or len(cur_amp.stdout) != 0:
            if cur_amp == amp_e and len(cur_amp.stdout) != 0:
                last_amp_e = list(cur_amp.stdout)[0]
            cur_amp = next(amps)
    
    return last_amp_e