from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Vertex:
    def __init__(self, value: str):
        self.value = value
        self.adjacent: list[Vertex] = []
        self.distance = 10000
        self.visited = False
        self.previous: Vertex | None = None

    def __repr__(self) -> str:
        return f'Value: {self.value} - adjacent: {[i.value for i in self.adjacent]} - distance:{self.distance}'  # noqa:  E501

    def __lt__(self, other: str) -> bool:
        return id(self) > id(other)


def node_level(node: str) -> int:
    if node == 'S':
        return ord('a')
    elif node == 'E':
        return ord('z')
    else:
        return ord(node)


def dijkstra(matrix: list[Vertex], source: Vertex) -> None:
    source.distance = 0

    unvisited_queue = [(i.distance, i) for i in matrix]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.visited = True

        print(current)

        for edge in current.adjacent:
            if edge.visited is True:
                continue

            # weight is always 1 in this case
            new_dist = current.distance + 1

            if new_dist < edge.distance:
                edge.distance = new_dist
                edge.previous = current

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(i.distance, i) for i in matrix if not i.visited]
        heapq.heapify(unvisited_queue)


def shortest(target: Vertex) -> list[Vertex]:
    path = [target]
    curr = target
    while curr.previous:
        previous = curr.previous
        path.append(previous)
        curr = previous

    return path[::-1]


def compute(s: str) -> int:
    lines = s.splitlines()
    matrix = [[Vertex(value) for value in line] for line in lines]
    # invert source and target
    source = []

    for line in range(len(lines)):
        for idx in range(len(lines[0]) - 1):
            node1 = matrix[line][idx]
            node2 = matrix[line][idx + 1]
            if node_level(node2.value) - node_level(node1.value) <= 1:
                node2.adjacent.append(node1)
            if node_level(node1.value) - node_level(node2.value) <= 1:
                node1.adjacent.append(node2)

            # find source and target
            if node1.value in ['S', 'a']:
                source.append(node1)
            if node1.value == 'E':
                target = node1
            if node2.value in ['S', 'a']:
                source.append(node2)
            if node2.value == 'E':
                target = node2

    inverted_lines = list(zip(*lines))
    for line in range(len(inverted_lines)):
        for idx in range(len(inverted_lines[0]) - 1):
            node1 = matrix[idx][line]
            node2 = matrix[idx + 1][line]
            if node_level(node2.value) - node_level(node1.value) <= 1:
                node2.adjacent.append(node1)
            if node_level(node1.value) - node_level(node2.value) <= 1:
                node1.adjacent.append(node2)

    matrix_lst = [item for sublist in matrix for item in sublist]

    dijkstra(matrix_lst, target)

    return min([i.distance for i in source if i.distance != 10000])


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
