from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Monkey:
    monkey_items: list[int]
    operation: str
    divisible_test: int
    if_true: int
    if_false: int
    inspections: int = 0

    def monkey_turn(self, monkeys: list[Monkey], fac: int) -> None:
        for item in self.monkey_items:
            self.inspections += 1
            old: int = item  # noqa: F841
            worry_level = eval(self.operation)
            worry_level = worry_level % fac
            if worry_level % self.divisible_test == 0:
                monkeys[self.if_true].monkey_items.append(worry_level)
            else:
                monkeys[self.if_false].monkey_items.append(worry_level)
        self.monkey_items = []


def compute(s: str) -> int:
    monkeys = []
    raw_monkeys = s.split('\n\n')
    for raw_monkey in raw_monkeys:
        _, items, operation, test, if_true, if_false = raw_monkey.split('\n  ')
        monkeys.append(
            Monkey(
                monkey_items=[int(i) for i in items[16:].split(', ')],
                operation=operation[17:],
                divisible_test=int(test.split()[-1]),
                if_true=int(if_true.split()[-1]),
                if_false=int(if_false.split()[-1]),
            ),
        )

    fac = 1
    for monkey in monkeys:
        fac = fac*monkey.divisible_test

    for m_round in range(10_000):
        for monkey in monkeys:
            monkey.monkey_turn(monkeys, fac)

    big, second = sorted([i.inspections for i in monkeys])[-2:]
    return big*second


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
