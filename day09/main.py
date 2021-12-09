import sys
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
    for (y, x), height in tuple(height_map.items()):
        if height_map[(y - 1, x)] > height \
                and height_map[(y, x - 1)] > height \
                and height_map[(y, x + 1)] > height \
                and height_map[(y + 1, x)] > height:
            low_points += 1 + height_map[(y, x)]
    print(low_points)


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
