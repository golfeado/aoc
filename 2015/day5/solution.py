# --- Day 5: Doesn't He Have Intern-Elves For This? ---

# Santa needs help figuring out which strings in his text file are naughty or
# nice.

# A nice string is one with all of the following properties:

#     It contains at least three vowels (aeiou only), like aei, xazegov, or
#     aeiouaeiouaeiou.

#     It contains at least one letter that appears twice in a row, like xx,
#     abcdde (dd), or aabbccdd (aa, bb, cc, or dd).

#     It does not contain the strings ab, cd, pq, or xy, even if they are part
#     of one of the other requirements.


# For example:

#     ugknbfddgicrmopn is nice because it has at least three vowels
#     (u...i...o...), a double letter (...dd...), and none of the disallowed
#     substrings.

#     aaa is nice because it has at least three vowels and a double letter, even
#     though the letters used by different rules overlap.

#     jchzalrnumimnmhp is naughty because it has no double letter.

#     haegwjzuvuyypxyu is naughty because it contains the string xy.

#     dvszwmarrgswjxmb is naughty because it contains only one vowel.

# How many strings are nice?

# --- Part Two ---

# Realizing the error of his ways, Santa has switched to a better model of
# determining whether a string is naughty or nice. None of the old rules apply,
# as they are all clearly ridiculous.


# Now, a nice string is one with all of the following properties:

#     It contains a pair of any two letters that appears at least twice in the
#     string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
#     like aaa (aa, but it overlaps).

#     It contains at least one letter which repeats with exactly one letter
#     between them, like xyx, abcdefeghi (efe), or even aaa.


# For example:

#     qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and
#     a letter that repeats with exactly one letter between them (zxz).

#     xxyxx is nice because it has a pair that appears twice and a letter that
#     repeats with one between, even though the letters used by each rule
#     overlap.

#     uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with
#     a single letter between them.

#     ieodomkazucvgmuy is naughty because it has a repeating letter with one
#     between (odo), but no pair that appears twice.


# How many strings are nice under these new rules?

import pytest
import re
import io

TEST1_FILE: str = "./test1"
TEST2_FILE: str = "./test2"
PUZZLE_FILE: str = "./puzzle"
FORBIDDEN_STRINGS: list[str] = ["ab", "cd", "pq", "xy"]

def contains_three_vowels(s: str) -> bool:
    m = re.match(r'^.*([aeiou]{1}).*([aeiou]{1}).*([aeiou]{1})', s)
    if not m:
        return False
    if len(m.groups()) < 3:
        return False
    else:
        return True

def contains_pair(s: str) -> bool:
    past_ch: str = ''
    for ch in s:
        if ch == past_ch:
            return True
        else:
            past_ch = ch
    else:
        return False

def contains_substrings(string: str,
                        substrings: list[str] = FORBIDDEN_STRINGS) -> bool:
    return any(ss in string for ss in substrings)

def is_nice(s: str) -> bool:
    "Return True if s passes every nicety test of the first part puzzle"
    if not contains_three_vowels(s):
        return False
    elif not contains_pair(s):
        return False
    elif contains_substrings(s, FORBIDDEN_STRINGS):
        return False
    else:
        return True

def solve1(puzzle: str) -> int:
    with open(puzzle, 'r', encoding='utf-8') as p:
        lines: list[str] = p.readlines()
        return len([l for l in lines if is_nice(l)])

def contains_repeated_pair(s: str) -> bool:
    """Return True if s contains a pair of any two letters that appears at least
    twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa),
    but not like aaa (aa, but it overlaps).
    """
    for pos in range(1, len(s) - 1):
        pair: str = s[pos - 1 : pos + 1]
        ss: str = s[pos + 1 :]
        if pair in ss:
            return True
    else:
        return False

def contains_separated_pair(s: str) -> bool:
    """Return True if s contains at least one letter which repeats with exactly
    one letter between them, like xyx, abcdefeghi (efe), or even aaa.
    """
    length: int = len(s)

    if length < 3:
        return False
    elif length == 3:
        if s[0] == s[2]:
            return True
        else:
            return False
    else:
        for pos in range(2, len(s) - 1):
            if s[pos - 2]  == s[pos]:
                return True
        else:
            return False

def is_very_nice(s: str) -> bool:
    "Return True if s passes every nicety test of the second part puzzle"
    if not contains_separated_pair(s):
        return False
    elif not contains_repeated_pair(s):
        return False
    else:
        return True

def solve2(puzzle: str) -> int:
    with open(puzzle, 'r', encoding='utf-8') as p:
        lines: list[str] = p.readlines()
        return len([l for l in lines if is_very_nice(l)])

### TEST

# test1 file content:

# uxcplgxnkwbdwhrp # naughty
# suerykeptdsutidb # naughty
# dmrtgdkaimrrwmej # nice
# ztxhjwllrckhakut # naughty
# gdnzurjbbwmgayrg # naughty
# gjdzbtrcxwprtery # naughty

# test2 file content:

# qjhvhtzxzqqjkmpb | is nice
# xxyxx            | is nice
# uurcxstgmygtbstg | is naughty
# ieodomkazucvgmuy | is naughty


def test_contains_substrings():
    assert contains_substrings('haegwjzuvuyypxyu', FORBIDDEN_STRINGS)
    assert contains_substrings('dvszwmarrgswjxmb', FORBIDDEN_STRINGS)
    assert contains_substrings(''.join(FORBIDDEN_STRINGS), FORBIDDEN_STRINGS)

def test_is_nice():
    assert is_nice('ugknbfddgicrmopn')
    assert is_nice('aaa')
    assert not is_nice('jchzalrnumimnmhp')
    assert not is_nice('haegwjzuvuyypxyu')
    assert not is_nice('dvszwmarrgswjxmb')

def test_contains_repeated_pair():
    assert contains_repeated_pair('xyxy')
    assert contains_repeated_pair('aabcdefgaa')
    assert contains_repeated_pair('fasfkkhkkff')
    assert not contains_repeated_pair('aaa')

def test_contains_separated_pair():
    assert contains_separated_pair('xyx')
    assert contains_separated_pair('abcdefeghi')
    assert contains_separated_pair('aaa')
    assert not contains_separated_pair('aa')

def test_is_very_nice():
    assert is_very_nice('qjhvhtzxzqqjkmpb')
    assert is_very_nice('xxyxx')
    assert not  is_very_nice('ieodomkazucvgmuy')
    assert not  is_very_nice('uurcxstgmygtbstg')

def test_solve1():
    assert solve1(TEST1_FILE) == 1
    assert solve1(PUZZLE_FILE) == 236

def test_solve2():
    assert solve2(TEST2_FILE) == 2
    assert solve2(PUZZLE_FILE) == 51

