from __future__ import annotations

import argparse
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Sensor(NamedTuple):
    sx: int
    sy: int
    bx: int
    by: int


def compute(s: str, depth: int = 4_000_000) -> int:
    beacons = set()
    sensors: list[Sensor] = list()

    lines = s.splitlines()
    for line in lines:
        sx, sy, bx, by = re.findall('=([0-9-]*)', line)
        sensor = Sensor(int(sx), int(sy), int(bx), int(by))
        beacon = (int(bx), int(by))

        sensors.append(sensor)
        beacons.add(beacon)

    for sensor in sensors:
        distance = abs(sensor.sx - sensor.bx) + abs(sensor.sy - sensor.by)
        for i in range(distance):
            x_and_y = (
                (sensor.sx + i, sensor.sy + distance - 1 - i),
                (sensor.sx - i, sensor.sy + distance - 1 - i),
                (sensor.sx + i, sensor.sy - distance - 1 + i),
                (sensor.sx - i, sensor.sy - distance - 1 + i),
            )
            for x, y in x_and_y:
                if x < 0 or y < 0 or x > depth or y > depth:
                    continue

                elif (x, y) in beacons:
                    continue

                for s2 in sensors:
                    dist = abs(s2.sx - s2.bx) + abs(s2.sy - s2.by)
                    if abs(s2.sx - x) + abs(s2.sy - y) <= dist:
                        break

                else:
                    return x * 4_000_000 + y

    return 0


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
