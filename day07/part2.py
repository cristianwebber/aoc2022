from __future__ import annotations

import argparse
import os.path
from collections import Counter
from pathlib import Path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    fs: Counter[Path] = Counter()
    curr_dir = top = Path('/')

    lines = [x.split(' ') for x in s.splitlines()]
    for line in lines:
        if line[0] == '$':
            if line[1] == 'cd':
                if line[2] == '/':
                    curr_dir = top
                if line[2] == '..':
                    curr_dir = curr_dir.parent
                else:
                    curr_dir /= line[2]

        elif line[0] != 'dir':
            fs[curr_dir] += int(line[0])
            for p in curr_dir.parents:
                fs[p] += int(line[0])

    fs_sorted = sorted(fs.values())

    for i in fs_sorted:
        if i > fs_sorted[-1] - 40_000_000:
            return i
    return 0


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


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
