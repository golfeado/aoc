# --- Day 3: Perfectly Spherical Houses in a Vacuum ---

# Santa is delivering presents to an infinite two-dimensional grid of houses.

# He begins by delivering a present to the house at his starting location, and
# then an elf at the North Pole calls him via radio and tells him where to move
# next. Moves are always exactly one house to the north (^), south (v), east
# (>), or west (<). After each move, he delivers another present to the house at
# his new location.

# However, the elf back at the north pole has had a little too much eggnog, and
# so his directions are a little off, and Santa ends up visiting some houses
# more than once. How many houses receive at least one present?

# For example:

#     > delivers presents to 2 houses: one at the starting location, and one to
#     > the east.

#     ^>v< delivers presents to 4 houses in a square, including twice to the
#     house at his starting/ending location.

#     ^v^v^v^v^v delivers a bunch of presents to some very lucky children at
#     only 2 houses.

# --- Part Two ---

# The next year, to speed up the process, Santa creates a robot version of
# himself, Robo-Santa, to deliver presents with him.


# Santa and Robo-Santa start at the same location (delivering two presents to
# the same starting house), then take turns moving based on instructions from
# the elf, who is eggnoggedly reading from the same script as the previous year.

# This year, how many houses receive at least one present?

# For example:

#     ^v delivers presents to 3 houses, because Santa goes north, and then
#     Robo-Santa goes south.

#     ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up
#     back where they started.

#     ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one
#     direction and Robo-Santa going the other.

import pytest
from dataclasses import dataclass

PUZZLE_FILE: str = './puzzle'
TEST_FILE: str = './test'

@dataclass
class Point:
    x: int
    y: int

def is_south(d: str) -> bool:
    return d == 'v'

def is_north(d: str) -> bool:
    return d == '^'

def is_east(d: str) -> bool:
    return d == '>'

def is_west(d: str) -> bool:
    return d == '<'

def delivered(directions: str) -> int:
    "Calculate how many houses got delivered at least one present"
    loc: Point = Point(0, 0)
    visited: list[Point] = [loc]

    for d in directions:

        if is_north(d):
            loc = Point(loc.x, loc.y + 1)
        elif is_south(d):
            loc = Point(loc.x, loc.y - 1)
        elif is_east(d):
            loc = Point(loc.x + 1, loc.y)
        elif is_west(d):
            loc = Point(loc.x - 1, loc.y)
        else:
            break

        visited.append(loc)

    return len({(l.x, l.y) for l in visited})

def robo_delivered(directions: str) -> int:
    turn: str            = 'santa' # 'santa' or 'robot'
    sloc: Point          = Point(0, 0)
    rloc: Point          = Point(0, 0)
    visited: list[Point] = [Point(0, 0)]

    for d in directions:

        if turn == 'santa':

            if is_north(d):
                sloc = Point(sloc.x, sloc.y + 1)
            elif is_south(d):
                sloc = Point(sloc.x, sloc.y - 1)
            elif is_east(d):
                sloc = Point(sloc.x + 1, sloc.y)
            elif is_west(d):
                sloc = Point(sloc.x - 1, sloc.y)
            else:
                break

            visited.append(sloc)
            turn = 'robot'

        elif turn == 'robot':

            if is_north(d):
                rloc = Point(rloc.x, rloc.y + 1)
            elif is_south(d):
                rloc = Point(rloc.x, rloc.y - 1)
            elif is_east(d):
                rloc = Point(rloc.x + 1, rloc.y)
            elif is_west(d):
                rloc = Point(rloc.x - 1, rloc.y)
            else:
                break

            visited.append(rloc)
            turn = 'santa'

    return len({(l.x, l.y) for l in visited})

def solve1(puzzle: str) -> int :
    with open(puzzle, 'r') as p:
        data: str = p.read().rstrip()
        return delivered(data)

def solve2(puzzle: str) -> int :
    with open(puzzle, 'r') as p:
        data: str = p.read().rstrip()
        return robo_delivered(data)

### TESTS

def test_delivered():
    assert delivered('') == 1
    assert delivered('>') == 2
    assert delivered('^>v<') == 4
    assert delivered('^v^v^v^v^v') == 2

def test_robo_delivered():
    assert robo_delivered('') == 1
    assert robo_delivered('^v') == 3
    assert robo_delivered('^>v<') == 3
    assert robo_delivered('^v^v^v^v^v') == 11

def test_solve1():
    assert solve1(TEST_FILE) == 2
    assert solve1(PUZZLE_FILE) == 2565

def test_solve2():
    assert solve2(TEST_FILE) == 11
    assert solve2(PUZZLE_FILE) == 2639
