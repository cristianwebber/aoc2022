from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def scenic_view(seq_trees: list[int], tree: int) -> int:
    if seq_trees:
        for idx, val in enumerate(seq_trees):
            if val >= tree:
                return idx+1
        return len(seq_trees)
    else:
        return 0


def visible(lines: list[list[int]], x: int, y: int) -> int:
    tree = int(lines[y][x])
    line = [int(tree) for tree in lines[y]]
    row = [int(tree[x]) for tree in lines]
    view_left = scenic_view(line[:x][::-1], tree)
    view_right = scenic_view(line[x+1:], tree)
    view_up = scenic_view(row[:y][::-1], tree)
    view_down = scenic_view(row[y+1:], tree)
    return view_left * view_right * view_up * view_down


def compute(s: str) -> int:
    max_view = 0
    lines = [[*x] for x in s.splitlines()]
    for y, line in enumerate(lines):
        for x, row in enumerate(line):
            view = visible(lines, x, y)
            if view > max_view:
                max_view = view

    return max_view


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
