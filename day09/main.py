import sys
import typing
from collections import defaultdict


def get_input() -> defaultdict[(int, int), int]:
    with open('input') as f:
        input_map = defaultdict(lambda: sys.maxsize)

        for y, line in enumerate(f):
            for x, char in enumerate(line.rstrip()):
                input_map[(y, x)] = int(char)
        return input_map


def part1():
    height_map = get_input()
    low_points = 0
    # basins do not have saddles, so just searching for the lowest number is enough
    for (y, x), height in tuple(height_map.items()):
        if height_map[(y - 1, x)] > height \
                and height_map[(y, x - 1)] > height \
                and height_map[(y, x + 1)] > height \
                and height_map[(y + 1, x)] > height:
            low_points += 1 + height_map[(y, x)]
    print(low_points)


def adjacents(y: int, x: int) -> typing.Generator[tuple[int, int], None, None]:
    yield y, x + 1
    yield y, x - 1
    yield y - 1, x
    yield y + 1, x


def is_lowest_point(height_map, coord):
    return all(
        height_map[adj_coord] > height_map[coord]
        for adj_coord in adjacents(*coord)
    )


def flood_basin(height_map, low: typing.Tuple[int, int]):
    seen = set()
    # initialize with current coord to start
    neighbours = [low]
    while neighbours:
        y, x = neighbours.pop()
        seen.add((y, x))
        # process the adjacent coordinates
        for neighbour in adjacents(y, x):
            # ignore, what we've already seen, is a top or out of bounds and add it to the processing queue
            if neighbour not in seen and height_map[(y, x)] < 9:
                neighbours.append(neighbour)
    # out of bounds of the map values like (-1, -1) have an "invalid" default value if sys.maxsize
    # filter these out, because these do not count
    coords_within_bounds = set(filter(lambda coord: height_map[coord] < 9, seen))
    return len(coords_within_bounds)


def part2():
    height_map = get_input()
    sizes = []
    # figure out where the lowest point of a basin is to start of and then flood it
    for (y, x), height in tuple(height_map.items()):
        if is_lowest_point(height_map, (y, x)):
            sizes.append(flood_basin(height_map, (y, x)))
    # sort sizes to pick the biggest 3 basis
    sizes.sort()
    print(sizes[-1] * sizes[-2] * sizes[-3])


if __name__ == '__main__':
    part1()
    part2()
