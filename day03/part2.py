from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total_sum = 0
    lines = s.splitlines()
    for idx in range(0, len(lines), 3):
        part1 = lines[idx]
        part2 = lines[idx+1]
        part3 = lines[idx+2]
        same_letters = set(part1) & set(part2) & set(part3)
        for letter in same_letters:
            # capital letter
            if ord(letter) >= 65 and ord(letter) <= 90:
                total_sum += (ord(letter) - 38)
            # small letters
            elif ord(letter) >= 97 and ord(letter) <= 122:
                total_sum += (ord(letter) - 96)
    return total_sum


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
