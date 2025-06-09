# -- Day 8: Matchsticks ---

# Space on the sleigh is limited this year, and so Santa will be bringing his
# list as a digital copy. He needs to know how much space it will take up when
# stored.

# It is common in many programming languages to provide a way to escape special
# characters in strings. For example, C, JavaScript, Perl, Python, and even PHP
# handle special characters in very similar ways.

# However, it is important to realize the difference between the number of
# characters in the code representation of the string literal and the number of
# characters in the in-memory string itself.

# For example:

#     "" is 2 characters of code (the two double quotes), but the string
#     contains zero characters.

#     "abc" is 5 characters of code, but 3 characters in the string data.

#     "aaa\"aaa" is 10 characters of code, but the string itself contains six
#     "a" characters and a single, escaped quote character, for a total of 7
#     characters in the string data.

#     "\x27" is 6 characters of code, but the string itself contains just one -
#     an apostrophe ('), escaped using hexadecimal notation.

# Santa's list is a file that contains many double-quoted string literals, one
# on each line. The only escape sequences used are \\ (which represents a single
# backslash), \" (which represents a lone double-quote character), and \x plus
# two hexadecimal characters (which represents a single character with that
# ASCII code).

# Disregarding the whitespace in the file, what is the number of characters of
# code for string literals minus the number of characters in memory for the
# values of the strings in total for the entire file?

# For example, given the four strings above, the total number of characters of
# string code (2 + 5 + 10 + 6 = 23) minus the total number of characters in
# memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.

# --- Part Two ---

# Now, let's go the other way. In addition to finding the number of characters
# of code, you should now encode each code representation as a new string and
# find the number of characters of the new encoded representation, including the
# surrounding double quotes.

# For example:

#     "" encodes to "\"\"", an increase from 2 characters to 6.

#     "abc" encodes to "\"abc\"", an increase from 5 characters to 9.

#     "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to
#     16.

#     "\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11.

# Your task is to find the total number of characters to represent the newly
# encoded strings minus the number of characters of code in each original string
# literal. For example, for the strings above, the total encoded length (6 + 9 +
# 16 + 11 = 42) minus the characters in the original code representation (23,
# just like in the first part of this puzzle) is 42 - 23 = 19.


import pytest
import re

PUZZLE_FILE: str = './puzzle'
TEST_FILE: str = './test'
ESC_SEQ_RE: str = r'(\\x[0-9a-f]{2})|(\\")|(\\\\)'
ESC_SEQ_NO_HEX: set = {'\\"', '\\\\'}


def string_value_len(s: str) -> int:
    "Return the number of characters in memory for string value in 's'."
    # remove the starting and ending double quotes
    ss: str = s.removesuffix('\"').removeprefix('\"')
    length: int = len(ss)
    m = re.finditer(ESC_SEQ_RE, ss)
    if m:
        for i in m:
            # Check if match is '\"' or '\\'.
            if i.group() in ESC_SEQ_NO_HEX:
                length -= 1
            # Then match should be some hex escaping sequence.
            else:
                length -= 3
    return length


def solve1(puzzle: str = PUZZLE_FILE) -> int:
    with open(puzzle, 'r') as p:
        data: list[str] = [l.rstrip('\n') for l in p.readlines()]
        code_len: int = sum(len(s) for s in data)
        mem_value_len: int = sum(string_value_len(s) for s in data)
        return code_len - mem_value_len


def string_added_value(s: str) -> int:
    "Return the number of characters in memory for string value in 's'."
    # Add the value of two new double quotes and two backslashes
    length: int = len(s) + 4
    m = re.finditer(ESC_SEQ_RE, s)
    if m:
        for i in m:
            # Check if match is '\"' or '\\'.
            if i.group() in ESC_SEQ_NO_HEX:
                length += 2
            # Then match should be some hex escaping sequence.
            else:
                length += 1
    return length

def solve2(puzzle: str = PUZZLE_FILE) -> int:
    with open(puzzle) as p:
        data: list[str] = [l.rstrip('\n') for l in p.readlines()]
        code_len: int = sum(len(s) for s in data)
        encoded_added_len: int = sum(string_added_value(s) for s in data)
        return encoded_added_len - code_len


### TESTS

# TEST_FILE content
#
# "sjdivfriyaaqa\xd2v\"k\"mpcu\"yyu\"en"
# "vcqc"
# "zbcwgmbpijcxu\"yins\"sfxn"
# "yumngprx"
# "bbdj"
# "czbggabkzo\"wsnw\"voklp\"s"
# "b\\bdj"

# Expected solve1() results from TEST_FILE:
#
# (+ 38 6 27 10 6 28 8) = 123 chars in string code
# (+ 29 4 23 8 4 23 5)  = 96 chars in memory for string values
# (- 123 96)            = 27 is the answer

def test_string_value_len():
    with open(TEST_FILE, 'r') as tf:
        data = [l.rstrip('\n') for l in tf.readlines()]
        assert string_value_len(data[0])              == 29
        assert string_value_len(data[1])              == 4
        assert string_value_len(data[2])              == 23
        assert string_value_len(data[3])              == 8
        assert string_value_len(data[4])              == 4
        assert string_value_len(data[5])              == 23
        assert string_value_len(data[6])              == 5
        assert sum(string_value_len(l) for l in data) == 96


def test_solve1():
    assert solve1(TEST_FILE) == 27
    assert solve1() == 1333


def test_solve2():
    assert solve2() == 2046
