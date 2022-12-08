from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def visible(lines: list[list[int]], x: int, y: int) -> bool:
    tree = int(lines[y][x])
    line = [int(tree) for tree in lines[y]]
    row = [int(tree[x]) for tree in lines]
    max_left = max(line[:x], default=-1)
    max_right = max(line[x+1:], default=-1)
    max_up = max(row[:y], default=-1)
    max_down = max(row[y+1:], default=-1)
    return (
        tree > max_left or tree > max_right
        or tree > max_up or tree > max_down
    )


def compute(s: str) -> int:
    trees_visible = 0
    lines = [[*x] for x in s.splitlines()]
    for y, line in enumerate(lines):
        for x, row in enumerate(line):
            trees_visible += visible(lines, x, y)

    return trees_visible


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
