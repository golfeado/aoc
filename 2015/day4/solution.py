# --- Day 4: The Ideal Stocking Stuffer ---

# Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
# gifts for all the economically forward-thinking little girls and boys.


# To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
# least five zeroes. The input to the MD5 hash is some secret key (your puzzle
# input, given below) followed by a number in decimal. To mine AdventCoins, you
# must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
# that produces such a hash.


# For example:

#     If your secret key is abcdef, the answer is 609043, because the MD5 hash of
#     abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
#     such number to do so.

#     If your secret key is pqrstuv, the lowest number it combines with to make an
#     MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
#     pqrstuv1048970 looks like 000006136ef....

# Your puzzle input is yzbqklnj.

# --- Part Two ---

# Now find one that starts with six zeroes.

#import pytest
from typing import Callable
import hashlib
import re

PUZZLE_KEY: str = 'yzbqklnj'

def starts_with_five_zeroes(hex: str) -> bool:
    "Returns true if hex starts  with five zeroes ('00000...')"
    match = re.search(r"^00000", hex)
    if match: return True
    else: return False

def starts_with_six_zeroes(hex: str) -> bool:
    "Returns true if hex starts with six zeroes ('000000...')"
    match = re.search(r"^000000", hex)
    if match: return True
    else: return False

def get_hash_key_num_suffix(key: str, pred: Callable) -> int:
    """Get numerical suffix added to key that, when MD5 hashed, digests into an
    hexadecimal str that satisfies pred function."""
    suffix: int = 0
    while True:
        full_key: str = key + str(suffix)
        hexa: str = hashlib.md5(full_key.encode()).hexdigest()
        if pred(hexa):
            break
        else:
            suffix += 1

    return suffix

def solve1(key: str = PUZZLE_KEY) -> int:
    return  get_hash_key_num_suffix(key, starts_with_five_zeroes)

def solve2(key: str = PUZZLE_KEY) -> int:
    return  get_hash_key_num_suffix(key, starts_with_six_zeroes)

### TEST

def test_starts_with_five_zeroes():
    assert starts_with_five_zeroes('00000a')
    assert starts_with_five_zeroes('000000a')
    assert not starts_with_five_zeroes('a00000')
    assert not starts_with_five_zeroes('0000a0')
    assert not starts_with_five_zeroes('0x00000fasdl')

def test_solve1():
    assert solve1('abcdef') == 609043
    assert solve1('pqrstuv') == 1048970
    assert solve1(PUZZLE_KEY) == 282749

def test_solve2():
    assert solve2(PUZZLE_KEY) == 9962624
