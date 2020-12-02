import operator
import collections

class BaseSignal(Exception): pass

class HaltSignal(BaseSignal): pass

class JumpSignal(BaseSignal):
    def __init__(self, pos):
        self.pos = pos

class RelativeSignal(BaseSignal):
    def __init__(self, delta):
        self.delta = delta

class IOSignal(BaseSignal):
    STDIN = 1
    STDOUT = 2

    def __init__(self, pos=None, value=None, pipe=STDIN):
        self.pipe = pipe
        self.pos = pos
        self.value = value

class IntCodeOp():
    size = 1

    def __call__(self, pos, buffer, rel_base):
        self.pos = pos
        self.buffer = buffer
        self.rel_base = rel_base
        opcode_modes, *self.params = self.parameters()
        self.opcode = opcode_modes % 100
        self.modes = [int(i) for i in f"{opcode_modes // 100:04}"]
        self.modes.reverse()
        self.handle(*zip(self.params, self.modes))
    
    def parameters(self):
        start = self.pos
        stop = start+self.size
        return self.buffer[start:stop]
    
    def get_address(self, param):
        value, mode = param
        if mode == 0:
            return value
        elif mode == 1:
            raise NotImplementedError
        elif mode == 2:
            return value + self.rel_base

    def value(self, param):
        value, mode = param
        if mode == 0:
            return self.buffer[value]
        elif mode == 1:
            return value
        elif mode == 2:
            return self.buffer[value + self.rel_base]
        else:
            raise NotImplementedError("Parameter mode not supported")

class MutateOp(IntCodeOp):
    size = 4
    def handle(self, param1, param2, destparam):
        n1, n2, dest = self.value(param1), self.value(param2), self.get_address(destparam)
        self.buffer[dest] = self.handle_mutate(n1, n2)

class HaltOp(IntCodeOp):
    def handle(self):
        raise HaltSignal

class AddOp(MutateOp):
    handle_mutate = operator.add

class MulOp(MutateOp):
    handle_mutate = operator.mul

class InputOp(IntCodeOp):
    size = 2
    def handle(self, destparam):
        raise IOSignal(pos=self.get_address(destparam), pipe=IOSignal.STDIN)

class OutputOp(IntCodeOp):
    size = 2
    def handle(self, parampos):
        raise IOSignal(value=self.value(parampos), pipe=IOSignal.STDOUT)

class EqualOp(MutateOp):
    def handle_mutate(self, p1, p2):
        return int(p1 == p2)

class LessThanOp(MutateOp):
    def handle_mutate(self, p1, p2):
        return int(p1 < p2)

class JumpTrueOp(IntCodeOp):
    size = 3
    
    def handle(self, param1, destparam):
        n1, dest = self.value(param1), self.value(destparam)
        if n1 != 0:
            raise JumpSignal(dest)

class JumpFalseOp(IntCodeOp):
    size = 3
    
    def handle(self, param1, destparam):
        n1, dest = self.value(param1), self.value(destparam)
        if n1 == 0:
            raise JumpSignal(dest)

class RelativeOp(IntCodeOp):
    size = 2
    def handle(self, parampos):
        delta = self.value(parampos)
        raise RelativeSignal(delta)

class Pipe(collections.deque):

    def write_all(self, iterable):
        for val in iter(iterable):
            self.write(val)

    def write(self, val):
        self.appendleft(val)
    
    def read_all(self):
        items = []
        while len(self):
            items.append(self.read())
        
        return items

    def read(self):
        try:
            return self.pop()
        except IndexError:
            return None

class IntCodeMemory(list):
    def __init__(self, bytecode):
        self[:] = bytecode[:]

    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except IndexError:
            return 0
    
    def __setitem__(self, index, value):
        try:
            return super().__setitem__(index, value)
        except IndexError:
            if not isinstance(index, int):
                raise NotImplementedError
            missing = index - len(self) + 1
            self.extend([0] * missing)
            return super().__setitem__(index, value)

class IntCode():
    instructions = {
        1: AddOp(),
        2: MulOp(),
        3: InputOp(),
        4: OutputOp(),
        5: JumpTrueOp(),
        6: JumpFalseOp(),
        7: LessThanOp(),
        8: EqualOp(),
        9: RelativeOp(),
        99: HaltOp(),
    }

    def __init__(self, buffer = list(), stdin=Pipe(), stdout=Pipe()):
        self.buffer = IntCodeMemory(buffer)
        self.stdin = stdin
        self.stdout = stdout

        self.inst = 0
        self.halted = False
        self.steps = 0
        self.rel_base = 0

    def run_step(self):
        if self.halted: return

        opcode = self.buffer[self.inst] % 100   
        opfn = self.instructions.get(opcode, None)
        self.last_op = opfn
        if not opfn:
            raise NotImplementedError(f'Unknown op {opcode}')

        try:
            new_inst = self.inst + opfn.size
            opfn(self.inst, self.buffer, self.rel_base)
        except IOSignal as signal:
            if signal.pipe == IOSignal.STDIN:
                value = self.stdin.read()
                if value == None:
                    raise Exception("Input expected")
                self.buffer[signal.pos] = value

            elif signal.pipe == IOSignal.STDOUT:
                self.stdout.write(signal.value)
            else:
                raise NotImplementedError(f"Pipe {signal.pipe} not supported")

        except JumpSignal as jump:
            new_inst = jump.pos

        except RelativeSignal as rel:
            self.rel_base += rel.delta

        except HaltSignal:
            self.halted = True
        
        finally:
            self.inst = new_inst
        
        self.steps += 1
    
    def run_to_stdout(self):
        while not self.halted and len(self.stdout) == 0:
            self.run_step()
        return

    def run_to_halt(self):
        while not self.halted:
            self.run_step()
    
    def __copy__(self):
        newcls = self.__class__(buffer=self.buffer)
        newcls.inst = self.inst
        newcls.halted = self.halted
        newcls.steps = self.steps
        newcls.rel_base = self.rel_base

        return newcls