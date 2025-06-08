# --- Day 7: Some Assembly Required ---

# This year, Santa brought little Bobby Tables a set of wires and bitwise logic
# gates! Unfortunately, little Bobby is a little under the recommended age
# range, and he needs help assembling the circuit.

# Each wire has an identifier (some lowercase letters) and can carry a 16-bit
# signal (a number from 0 to 65535). A signal is provided to each wire by a
# gate, another wire, or some specific value. Each wire can only get a signal
# from one source, but can provide its signal to multiple destinations. A gate
# provides no signal until all of its inputs have a signal.

# The included instructions booklet describes how to connect the parts together:
# x AND y -> z means to connect wires x and y to an AND gate, and then connect
# its output to wire z.

# For example:

#     123 -> x means that the signal 123 is provided to wire x.

#     x AND y -> z means that the bitwise AND of wire x and wire y is provided
#     to wire z.

#     p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and
#     then provided to wire q.

#     NOT e -> f means that the bitwise complement of the value from wire e is
#     provided to wire f.

# Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for
# some reason, you'd like to emulate the circuit instead, almost all programming
# languages (for example, C, JavaScript, or Python) provide operators for these
# gates.

# For example, here is a simple circuit:

# 123 -> x
# 456 -> y
# x AND y -> d
# x OR y -> e
# x LSHIFT 2 -> f
# y RSHIFT 2 -> g
# NOT x -> h
# NOT y -> i

# After it is run, these are the signals on the wires:

# d: 72
# e: 507
# f: 492
# g: 114
# h: 65412
# i: 65079
# x: 123
# y: 456

# In little Bobby's kit's instructions booklet (provided as your puzzle input),
# what signal is ultimately provided to wire a?

# --- Part Two ---

# Now, take the signal you got on wire a, override wire b to that signal, and
# reset the other wires (including wire a). What new signal is ultimately
# provided to wire a?


#import pytest
from dataclasses import dataclass
from typing import NewType
import re


@dataclass
class Operation:
    input_wire: tuple[str] | None
    output_wire: str
    operator: str | None = None
    signal: int | None = None
    shifting: int | None = None

    def __post_init__(self):
        assert isinstance(self.input_wire, tuple | None), f"'Operation' class field 'input_wire' must be a tuple of str or Nonetype; instead input_wire='{self.input_wire}' of type={type(self.input_wire)}"
        assert isinstance(self.output_wire, str), f"'Operation' class field 'output_wire' must be str; instead output_wire='{self.output_wire}' of type={type(self.output_wire)}"
        assert isinstance(self.operator, str | None), f"'Operation' class field 'operator' must be a str or Nonetype; instead operator='{self.operator}' of type={type(self.operator)}"
        assert isinstance(self.signal, int | None), f"'Operation' class field 'signal' must be an int or Nonetype; instead signal='{self.signal}' of type={type(self.signal)}"
        assert isinstance(self.shifting, int | None), f"'Operation' class field 'shifting' must be an int or Nonetype; instead shifting='{self.shifting}' of type={type(self.shifting)}"


Operations = list[Operation]
Wires = dict[str : int]


PUZZLE_FILE: str = "./puzzle"
TEST_FILE: str = "./test"
MAX_16BIT_INT: int = 65335
FIRST_PART_ANSWER: int = 46065


def parse_operation(s: str) -> Operation:
    "Parse an input string as an Operation; return None if input was invalid."

    reg = r"^([a-zA-Z0-9]+) ?([A-Z]*) ?([a-z0-9]*) -> ([a-z]+)$"
    m = re.match (reg, s)

    if m.group(1) == 'NOT': # is a NOT operation
        inp: tuple[str] = tuple([m.group(3)])
        out: str = m.group(4)
        op: str = m.group(1)
        return Operation(inp, out, op)

    if not m.group(2): # is a direct signaling operation
        out: str = m.group(4)
        if m.group(1).isdigit():
            signal: int = int(m.group(1))
            return Operation(None, out, 'SIGNAL', signal)
        else:
            return Operation(tuple([m.group(1)]), out, 'SIGNAL')

    elif m.group(2).endswith("SHIFT"): # is a shifting operation
        inp: tuple[str] = tuple([m.group(1)])
        out: str = m.group(4)
        op: str = m.group(2)
        shift: int = int(m.group(3))
        return Operation(inp, out, op, shifting=shift)

    elif m: # is an OR or AND operation
        inp: tuple[str] = (m.group(1), m.group(3))
        out: str = m.group(4)
        op: str = m.group(2)
        return Operation(inp, out, op)

    else: # is a blank or invalid input string
        raise ValueError("Input string couldn't be parsed: ", s)


def parse_operations(los: list[str]) -> Operations:
    "Parse a list of strings as a list of Operation and possibly None values."
    return [parse_operation(s) for s in los]


def get_wires(ops: Operations, part_two: bool = False) -> Wires:
    """Returns a Wires dictionary made following and looping through an
    Operation list"""
    wires: Wires = {}
    while ops:
        for o in ops:
            # Its a blank line or invalid string parsed as None
            if not o:
                del ops[ops.index(o)]

            # part_two behavior hardcoded. LOL
            elif part_two and o.output_wire == 'b':
                wires['b'] = FIRST_PART_ANSWER
                del ops[ops.index(o)]

            # Its a direct signaling
            elif not o.input_wire:
                wires[o.output_wire] = o.signal
                del ops[ops.index(o)]

            # Every dependency for op is met
            elif all((in_w in wires for in_w in o.input_wire if not in_w.isdigit())):
                vals = []
                for w in o.input_wire:
                    if w.isdigit():
                        vals.append(int(w))
                    else:
                        vals.append(wires[w])
                else:
                    vals = tuple(vals)
                res = do_bit_operation(o.operator,
                                       vals,
                                       o.shifting if o.shifting else None)
                wires[o.output_wire] = res
                del ops[ops.index(o)]

    return wires


def do_bit_operation(operator: str, vals: tuple[int],
                     shift: int | None = None) -> int:
    "Return the value of the bitwise operation correspondent to given Operation."
    assert isinstance(vals[0], int), "Invalid object: '{}' of type: {}".format(vals[0], type(vals[0]))
    match operator:
        case 'SIGNAL':
            return vals[0]
        case 'NOT':
            return ~vals[0] & MAX_16BIT_INT # python black magic
        case 'AND':
            return vals[0] & vals[1]
        case 'OR':
            return vals[0] | vals[1]
        case 'LSHIFT':
            return vals[0] << shift
        case 'RSHIFT':
            return vals[0] >> shift
        case _:
            raise ValueError("'operator' argument not valid: {}".format(operator))


def solve1(puzzle: str = PUZZLE_FILE) -> int:
    with open(puzzle) as p:
        ops: Operations = parse_operations(p.readlines())
        wires: Wires = get_wires(ops)
        return wires['a']


def solve2(puzzle: str = PUZZLE_FILE) -> int:
    with open(puzzle) as p:
        ops: Operations = parse_operations(p.readlines())
        wires: Wires = get_wires(ops, part_two=True)
        return wires['a']


### TESTS

def test_get_wires():
    with open(TEST_FILE) as f:
        o = parse_operations(f.readlines())
        w = get_wires(o)
        assert len(wires) == 8
        assert w['y'] == 456   # tests direct signaling
        assert w['d'] == 72    # tests AND operator
        assert w['e'] == 507   # tests OR operator
        assert w['f'] == 492   # tests LSHIFT operator
        assert w['g'] == 114   # tests RSHIFT operator
        assert w['i'] == 65079 # tests NOT operator


def test_parse_operation():
    assert parse_operation('123 -> x') == Operation(None, 'x', None, 123, None)
    assert parse_operation('x AND y -> d') == Operation(('x', 'y'), 'd', 'AND', None, None)
    assert parse_operation('x OR y -> d') == Operation(('x', 'y'), 'd', 'OR', None, None)
    assert parse_operation('x LSHIFT 2 -> f') == Operation(tuple(['x']), 'f', 'LSHIFT', None, 2)
    assert parse_operation('NOT y -> x') == Operation(tuple(['y']), 'x', 'NOT', None, None)


def test_solve1():
    assert solve1() == 46065

def test_solve2():
    assert solve2() == 14134
