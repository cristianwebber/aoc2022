from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def sand_flow(rocks: set[tuple[int, int]], top: int, bottom: int) -> int:
    filled = rocks.copy()
    x, y = 500, 0
    while True:
        if (x, y+1) not in filled:
            if y > top:
                break
            y += 1
        elif (x-1, y+1) not in filled:
            x = x - 1
        elif (x+1, y+1) not in filled:
            x = x + 1
        else:
            filled.add((x, y))
            x, y = 500, 0

    return len(filled) - len(rocks)


def compute(s: str) -> int:
    rocks = set()
    bottom = 1_000_000
    top = 0
    lines = s.splitlines()
    for line in lines:
        rock_points = line.split(' -> ')
        for i in range(len(rock_points)-1):
            rock1 = rock_points[i].split(',')
            rock2 = rock_points[i+1].split(',')
            r1x, r1y = int(rock1[0]), int(rock1[1])
            r2x, r2y = int(rock2[0]), int(rock2[1])

            if r1x != r2x:
                if r1x < r2x:
                    x = range(r1x, r2x+1)
                else:
                    x = range(r2x, r1x+1)

                rocks.update(list(itertools.product(x, [r1y])))

            if r1y != r2y:
                if r1y < r2y:
                    y = range(r1y, r2y+1)
                else:
                    y = range(r2y, r1y+1)

                rocks.update(list(itertools.product([r1x], y)))

    top = max([i[1] for i in rocks])
    bottom = min([i[1] for i in rocks])

    return sand_flow(rocks, top, bottom)


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


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
