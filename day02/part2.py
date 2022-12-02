from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


POINTS = {
    'X': 0,  # LOSS
    'Y': 3,  # DRAW
    'Z': 6,  # WIN
}

# A(1) for Rock, B(2) for Paper, and C(3) for Scissors

WHO_WIN = {
    'A': {
        'X': 3,
        'Y': 1,
        'Z': 2,
    },
    'B': {
        'X': 1,
        'Y': 2,
        'Z': 3,
    },
    'C': {
        'X': 2,
        'Y': 3,
        'Z': 1,
    },
}


def compute(s: str) -> int:
    lines = [x.split(' ') for x in s.splitlines()]
    return sum(POINTS[line[1]] + WHO_WIN[line[0]][line[1]] for line in lines)


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
