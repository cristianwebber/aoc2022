from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move_tail(head: list[int], tail: list[int]) -> list[int]:
    if head == tail:
        pass

    if head[0] - tail[0] > 1:
        tail[0] += 1

        if head[1] - tail[1] == 1:
            tail[1] += 1
        if head[1] - tail[1] == -1:
            tail[1] -= 1

    elif head[0] - tail[0] < -1:
        tail[0] -= 1

        if head[1] - tail[1] == 1:
            tail[1] += 1
        if head[1] - tail[1] == -1:
            tail[1] -= 1

    if head[1] - tail[1] > 1:
        tail[1] += 1

        if head[0] - tail[0] == 1:
            tail[0] += 1
        if head[0] - tail[0] == -1:
            tail[0] -= 1

    elif head[1] - tail[1] < -1:
        tail[1] -= 1

        if head[0] - tail[0] == 1:
            tail[0] += 1
        if head[0] - tail[0] == -1:
            tail[0] -= 1

    return tail


def compute(s: str) -> int:
    lines = [x.split(' ') for x in s.splitlines()]
    visited: set[tuple[int, ...]] = set()
    head = [1, 1]
    tail = [1, 1]

    for direction, count in lines:
        for i in range(int(count)):
            match direction:
                case 'R':
                    head[0] += 1
                case 'L':
                    head[0] -= 1
                case 'U':
                    head[1] += 1
                case 'D':
                    head[1] -= 1

            tail = move_tail(head, tail)
            visited.add(tuple(tail))

    return len(visited)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
