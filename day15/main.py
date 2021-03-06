import heapq
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


def get_cave_size(cave: TYPE_MAP) -> typing.Tuple[int, int]:
    return max(x for y, x in cave), max(y for y, x in cave)


def navigate(cave: TYPE_MAP) -> int:
    """
    Brute force solution that'll try every solution. Fun to see the numbers decrementing, but
    it takes an increasing amount of time
    """
    todo = deque([(0, 0)])
    visited: TYPE_PATH_COST = defaultdict(lambda: sys.maxsize)
    visited[(0, 0)] = 0
    width, height = get_cave_size(cave)

    while todo:
        current_position = todo.pop()
        for y, x in adjacents(*current_position):
            if in_bounds(width, height, x, y) \
                    and (visited[current_position] + cave[(y, x)]) < visited[(y, x)]:
                visited[(y, x)] = visited[current_position] + cave[(y, x)]
                todo.append((y, x))
    return visited[height, width]


def navigate_better(cave: TYPE_MAP) -> int:
    width, height = get_cave_size(cave)

    # initialize queue, zero cost at starting point
    # [cost, (y, x)]
    todo = [(0, (0, 0))]
    visited: TYPE_PATH_COST = dict()
    destination = (height, width)

    while todo:
        cost, pt = heapq.heappop(todo)

        # end the loop once we've reached the destination
        if pt == destination:
            return cost

        # if known and costs are higher, skip it
        if pt in visited and cost >= visited[pt]:
            continue
        else:
            visited[pt] = cost

        for neighbour in adjacents(*pt):
            if in_bounds(width, height, *neighbour):
                heapq.heappush(todo, (cost + cave[neighbour], neighbour))


def expand_map(cave: TYPE_MAP, expand_count: int):
    width, height = get_cave_size(cave)
    # increment by one because these are used as multiplicator
    width += 1
    height += 1

    for y_i in range(expand_count):
        for x_i in range(expand_count):
            # skip the initial tile
            if y_i == x_i == 0:
                continue
            for src_y in range(height):
                for src_x in range(width):
                    source_pt = (src_y, src_x)
                    target_pt = (height * y_i + src_y, width * x_i + src_x)
                    new_value = (cave[source_pt] + y_i + x_i) % 9
                    cave[target_pt] = new_value if new_value > 0 else 9


def part1():
    cave = get_input()
    # print(navigate(cave))
    print(navigate_better(cave))


def part2():
    cave = get_input()
    expand_map(cave, 5)
    print(navigate_better(cave))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
