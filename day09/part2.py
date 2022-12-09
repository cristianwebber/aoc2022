from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move_tail(head: list[int], tail: list[int]) -> list[int]:
    hx, hy = head
    tx, ty = tail

    if abs(hy - ty) == 2 and abs(hx - tx) == 2:
        return [(hx + tx) // 2, (hy + ty) // 2]
    if abs(hy - ty) == 2:
        return [hx, (ty + hy) // 2]
    elif abs(hx - tx) == 2:
        return [(tx + hx) // 2, hy]
    else:
        return tail


def compute(s: str) -> int:
    lines = [x.split(' ') for x in s.splitlines()]
    visited: set[tuple[int, ...]] = set()
    heads = [[0, 0] for i in range(10)]

    for direction, count in lines:
        for i in range(int(count)):
            match direction:
                case 'R':
                    heads[0][0] += 1
                case 'L':
                    heads[0][0] -= 1
                case 'U':
                    heads[0][1] += 1
                case 'D':
                    heads[0][1] -= 1

            for j in range(1, len(heads)):
                heads[j] = move_tail(heads[j-1], heads[j])

            visited.add(tuple(heads[-1]))

    return len(visited)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
