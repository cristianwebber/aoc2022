from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    assignment_count = 0

    lines = s.splitlines()
    for line in lines:
        elf1 = line.split(',')[0].split('-')
        elf1_set = set(range(int(elf1[0]), int(elf1[1])+1))
        elf2 = line.split(',')[1].split('-')
        elf2_set = set(range(int(elf2[0]), int(elf2[1])+1))
        if elf1_set.issubset(elf2_set):
            assignment_count += 1
        elif elf2_set.issubset(elf1_set):
            assignment_count += 1
    return assignment_count


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2


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
