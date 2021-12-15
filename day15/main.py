import sys
import typing
from collections import defaultdict, deque

TYPE_MAP = typing.Dict[typing.Tuple[int, int], int]
TYPE_POS = typing.Tuple[int, int]
TYPE_PATH_COST = typing.Dict[TYPE_POS, int]


def get_input() -> TYPE_MAP:
    with open('input') as f:
        input_map = defaultdict(lambda: sys.maxsize)

        for y, line in enumerate(f):
            for x, char in enumerate(line.rstrip()):
                input_map[(y, x)] = int(char)
        return input_map


def adjacents(y: int, x: int) -> typing.Generator[tuple[int, int], None, None]:
    yield y, x + 1
    yield y, x - 1
    yield y - 1, x
    yield y + 1, x


def in_bounds(width: int, height: int, x: int, y: int) -> bool:
    return 0 <= x <= width and 0 <= y <= height


def navigate(cave: TYPE_MAP):
    todo = deque([(0, 0)])
    visited: TYPE_PATH_COST = defaultdict(lambda: sys.maxsize)
    visited[(0, 0)] = 0
    width = max(x for y, x in cave)
    height = max(y for y, x in cave)

    while todo:
        current_position = todo.pop()
        for y, x in adjacents(*current_position):
            if in_bounds(width, height, x, y) \
                    and (visited[current_position] + cave[(y, x)]) < visited[(y, x)]:
                visited[(y, x)] = visited[current_position] + cave[(y, x)]
                todo.append((y, x))
    return visited[height, width]


def part1():
    cave = get_input()
    print(navigate(cave))


def part2():
    pass


if __name__ == '__main__':
    from timeit import timeit

    runs = 1
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
