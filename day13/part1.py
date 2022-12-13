from __future__ import annotations

import argparse
import itertools
import json
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ListLike = int | list['ListLike']


def compare(left: ListLike, right: ListLike) -> int:
    if isinstance(left, int) and not isinstance(right, int):
        left = [left]

    if isinstance(right, int) and not isinstance(left, int):
        right = [right]

    if isinstance(left, int) and isinstance(right, int):
        return left - right

    elif isinstance(left, list) and isinstance(right, list):
        for lef, rig in itertools.zip_longest(left, right):
            if lef is None:
                return -1
            elif rig is None:
                return 1

            compared = compare(lef, rig)
            if compared != 0:
                return compared

        else:
            return 0
    return 99


def compute(s: str) -> int:
    total = 0

    for i, pair in enumerate(s.split('\n\n'), 1):
        raw_left, raw_right = pair.splitlines()
        left = json.loads(raw_left)
        right = json.loads(raw_right)

        if compare(left, right) <= 0:
            total += i

    return total


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
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
