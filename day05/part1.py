from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    lines = s.splitlines()
    stack_lines = lines[:lines.index('')-1]
    instructions = lines[lines.index('')+1:]

    crates = [x[1::4] for x in stack_lines]

    len_crates = len(crates[-1])
    stacks: dict[int, list[str]] = {i+1: [] for i in range(len_crates)}

    for row in crates[::-1]:
        for idx, crate in enumerate(row):
            if crate != ' ':
                stacks[idx+1].append(crate)

    for instruction in instructions:
        inst = instruction.split()
        times = int(inst[1])
        from_queue = int(inst[3])
        to_queue = int(inst[5])
        for i in range(times):
            pop_value = stacks[from_queue].pop()
            stacks[to_queue].append(pop_value)

    tops = ''
    for i in range(len_crates):
        tops += stacks[i+1][-1]

    return tops


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
