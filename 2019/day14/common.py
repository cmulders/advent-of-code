import itertools
import collections

def ceildiv(a, b):
    return -(-a // b)

class Reaction():
    
    def __init__(self, out_n, out_name, *inputs):
        if len(inputs) % 2 != 0:
            raise Exception('inputs should be in pairs')
        self.out_name = out_name
        self.out_n = int(out_n)
        
        self.inputs =  {(int(inputs[i]), inputs[i+1]) for i in range(0, len(inputs), 2)}
    
    def react_amount(self, amount):
        n = ceildiv(amount, self.out_n)
        return (n * self.out_n, {
            (chem_in * n, chem_name) for chem_in, chem_name in self.inputs
        })

    def __eq__(self, other):
        if not isinstance(other, Reaction):
            raise NotImplementedError
        return (    self.out_name == other.out_name
                and self.out_n == other.out_n
                and self.inputs == other.inputs
        )
    
    def __hash__(self):
        return hash((self.out_n, self.out_name, *self.inputs))

    def __repr__(self):
        input_chems = ", ".join(f"{n} {name}" for n, name in self.inputs)
        return f"Reaction: {input_chems} => {self.out_n} {self.out_name}"


def parse_reactions(lines):
    reactions = set()
    for l in filter(bool, map(str.strip, lines.splitlines())):
        inp, out = map(str.strip, l.split(' => ', maxsplit=2))
        in_list = itertools.chain.from_iterable([s.strip().split(' ') for s in inp.split(', ')])
        out_n, out_name = map(str.strip, out.split(' '))
        reactions.add(Reaction(out_n, out_name, *in_list))
    return reactions

def reaction_input(reactions, start='ORE', end='FUEL', end_n=1):
    reaction_dict = {
        r.out_name: r
        for r in reactions
    }

    stock = collections.defaultdict(int)

    order_book = collections.deque([(end_n, end)])

    base_required = 0

    while order_book:
        #print(order_book, {k:v for k,v in stock.items() if v != 0})
        amount, chem = order_book.pop()
        
        if chem == start:
            base_required += amount
            continue

        if stock[chem] >= amount:
            stock[chem] -= amount
            continue
    
        if stock[chem] > 0:
            amount -= stock[chem]
            stock[chem] = 0

        added, orders = reaction_dict[chem].react_amount(amount)
        if added != amount:
            stock[chem] += added - amount

        for o in orders:
            order_book.append(o)
                
    return base_required