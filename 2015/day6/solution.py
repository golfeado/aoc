# --- Day 6: Probably a Fire Hazard ---

# Because your neighbors keep defeating you in the holiday house decorating
# contest year after year, you've decided to deploy one million lights in a
# 1000x1000 grid.

# Furthermore, because you've been especially nice this year, Santa has mailed
# you instructions on how to display the ideal lighting configuration.

# Lights in your grid are numbered from 0 to 999 in each direction; the lights
# at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include
# whether to turn on, turn off, or toggle various inclusive ranges given as
# coordinate pairs. Each coordinate pair represents opposite corners of a
# rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers
# to 9 lights in a 3x3 square. The lights all start turned off.

# Grid representation:

# (999, 0) ........ (999, 999)
# .........................
# .........................
# .........................
# (0, 0) ........... (0, 999)

# We could represent the whole grid from the beginning as a list of lists with
# 1-0 values (on - off).

# [[0, 0, 0, 0, ... 0, 0, 0, 0]
#  [0, 0, 0, 0, ... 0, 0, 0, 0]
#  [0, 0, 0, 0, ... 0, 0, 0, 0]
#               ...
#  [0, 0, 0, 0, ... 0, 0, 0, 0]
#  [0, 0, 0, 0, ... 0, 0, 0, 0]
#  [0, 0, 0, 0, ... 0, 0, 0, 0]]

# We could also represent the grid starting with an empty dict and creating new
# keys (if they didn't exist yet) or updating them to the correspondent value.

# {}
# =>
# {(0, 0) : 1, (0, 50) : 1, (100, 900) : 1}
# =>
# {(0, 0) : 0, (0, 50) : 0, (100, 900) : 1}
# ...

# PUZZLE_FILE fragment:

# turn on 294,132 through 460,338
# turn on 823,500 through 899,529
# turn off 225,603 through 483,920
# toggle 717,493 through 930,875
# toggle 534,948 through 599,968
# turn on 522,730 through 968,950
# turn off 102,229 through 674,529

# TEST_FILE:

# turn on 0,0 through 999,999
# toggle 0,0 through 999,0
# turn off 499,499 through 500,500

# To defeat your neighbors this year, all you have to do is set up your lights
# by doing the instructions Santa sent you in order.

# For example:

#     turn on 0,0 through 999,999 would turn on (or leave on) every light.

#     toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
#     turning off the ones that were on, and turning on the ones that were off.

#     turn off 499,499 through 500,500 would turn off (or leave off) the middle
#     four lights.

# --- Part Two ---

# You just finish implementing your winning light pattern when you realize you
# mistranslated Santa's message from Ancient Nordic Elvish.

# The light grid you bought actually has individual brightness controls; each
# light can have a brightness of zero or more. The lights all start at zero.

# The phrase turn on actually means that you should increase the brightness of
# those lights by 1.

# The phrase turn off actually means that you should decrease the brightness of
# those lights by 1, to a minimum of zero.

# The phrase toggle actually means that you should increase the brightness of
# those lights by 2.

# What is the total brightness of all lights combined after following Santa's
# instructions?

# For example:

#     turn on 0,0 through 0,0 would increase the total brightness by 1.

#     toggle 0,0 through 999,999 would increase the total brightness by 2000000.

# After following the instructions, how many lights are lit?


import pytest
from typing import NewType
from collections import namedtuple
import re


Point = namedtuple('Point', ['x', 'y'])
Grid = list[list[int]]

PUZZLE_FILE: str = './puzzle'
TEST_FILE: str = './test'


def make_grid(n: int = 1000) -> Grid:
    "Return a Grid of n by n dimensions with all values initialized as zeroes."
    val: int = 0 # ON value on grid
    return [list([val] * n) for __ in range(n)]


def parse_instruction(s: str) -> dict:
    """Parse puzzle instruction (str) into a dict of keys: 'action', 'p1' and
    'p2'. Action must be 'turn on', 'turn off' or 'toggle'; p1 and p2 must be
    valid Points.
    """
    m = re.match(r"^([a-z ]+) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)$", s)

    if not m: return None

    action = m.group(1)
    p1 = Point(int(m.group(2)), int(m.group(3)))
    p2 = Point(int(m.group(4)), int(m.group(5)))

    return {'action' : action, 'p1' : p1, 'p2' : p2}


def make_rectangle(p1: Point, p2: Point) -> list[Point]:
    """Return a list of the Points ocurring inside a given rectangle defined by
    the two corners (inclusive) given as Points (p1 and p2.)"""
    assert isinstance(p1, Point) and isinstance(p2, Point), "make_rectangle(): p1 and p2 must be Points"
    x_range = range(min(p1.x, p2.x), max((p1.x, p2.x)) + 1)
    y_range = range(min(p1.y, p2.y), max((p1.y, p2.y)) + 1)

    return [Point(x_pos, y_pos) for x_pos in x_range for y_pos in y_range]


def turn_on(p: Point, g: Grid) -> int:
    g[p.y][p.x] = 1
    return None


def turn_off(p: Point, g: Grid) -> int:
    g[p.y][p.x] = 0
    return None


def toggle(p: Point, g: Grid) -> int:
    "Toggle a given binary value to its other state."
    if g[p.y][p.x] == 0:
        turn_on(p, g)
    else:
        turn_off(p,g)

    return None


def solve1(puzzle: str) -> int:
    with open(puzzle) as p:
        grid: Grid = make_grid()
        data: list[str] = p.readlines()
        instructions: list[dict] = [parse_instruction(l) for l in data]

        for i in instructions:

            # Loop if we parsed a blank or incorrect line as None
            if not i: continue

            for p in make_rectangle(i['p1'], i['p2']):

                if i['action'] == 'turn on':
                    turn_on(p, grid)
                elif i['action'] == 'turn off':
                    turn_off(p, grid)
                elif i['action'] == 'toggle':
                    toggle(p, grid)
                else:
                    raise RuntimeError

        return sum((sum(row) for row in grid))


def is_turned_off(p: Point, g: Grid) -> bool:
    if g[p.y][p.x] == 0:
        return True
    else:
        return False


def correct_turn_on(p: Point, g: Grid) -> int:
    "Add 1 to brightness level of Point"
    g[p.y][p.x] += 1
    return None


def correct_turn_off(p: Point, g: Grid) -> int:
    "Substract 1 to brightness level of Point."
    if is_turned_off(p, g):
        return None
    else:
        g[p.y][p.x] -= 1
        return None


def correct_toggle(p: Point, g: Grid) -> int:
    "Add 2 to the brightness level of Point."
    g[p.y][p.x] += 2
    return None


def solve2(puzzle: str) -> int:
    with open(puzzle) as p:
        grid: Grid = make_grid()
        lines: list[str] = p.readlines()
        instructions: list[dict] = [parse_instruction(l) for l in lines]

        for i in instructions:
            # Skip i if we parsed a blank or malformed line as None
            if not i: continue

            for p in make_rectangle(i['p1'], i['p2']):

                if i['action'] == 'turn on':
                    correct_turn_on(p, grid)
                elif i['action'] == 'turn off':
                    correct_turn_off(p, grid)
                elif i['action'] == 'toggle':
                    correct_toggle(p, grid)
                else:
                    raise RuntimeError(f"Couldn't understand 'action' in: '{i['action']}'")

        return sum((sum(row) for row in grid))


### TESTS

def test_make_rectangle():
    assert len(make_rectangle(Point(0, 0), Point(2, 2))) == 9
    rectangle = make_rectangle(Point(1, 1), Point(0, 0))
    points = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]
    assert all((p in rectangle for p in points))


def test_make_grid():
    assert len(make_grid()) == 1000
    assert len(make_grid()[69]) == 1000
    assert make_grid()[420][69] == 0
    assert len({id(row) for row in make_grid()}) == 1000


def test_parse_instructions():
    assert parse_instruction('turn on 294,132 through 460,338') == {'action' : 'turn on', 'p1' : Point(294, 132), 'p2' : (460, 338)}
    assert parse_instruction('turn off 294,132 through 460,338') == {'action' : 'turn off', 'p1' : Point(294, 132), 'p2' : (460, 338)}
    assert parse_instruction('toggle 294,132 through 460,338') == {'action' : 'toggle', 'p1' : Point(294, 132), 'p2' : (460, 338)}


def test_solve1():
    assert solve1(TEST_FILE) == 4
    assert solve1(PUZZLE_FILE) == 377891


def test_solve2():
    assert solve2(TEST_FILE) == (3 * 1000000) - 4
    assert solve2(PUZZLE_FILE) == 14110788
