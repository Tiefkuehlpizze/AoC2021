from collections import deque
import typing


def get_input():
    with open('input') as f:
        input_map = {}

        for y, line in enumerate(f):
            for x, char in enumerate(line.rstrip()):
                input_map[(y, x)] = int(char)
        return input_map


def adjacents(y: int, x: int) -> typing.Generator[tuple[int, int], None, None]:
    for ya in range(y - 1, y + 2):
        for xa in range(x - 1, x + 2):
            # skip if it the initial coordinate
            if xa == x and ya == y:
                continue
            yield ya, xa


def part1():
    oct_map = get_input()
    flashes = 0
    for _ in range(100):
        flash_later = deque()
        for coord in oct_map:
            oct_map[coord] += 1
            if oct_map[coord] > 9:
                flash_later.append(coord)

        while flash_later:
            coord = flash_later.pop()
            # if zero, it has recently flashed, not charging again
            if oct_map[coord] == 0:
                continue
            flashes += 1
            oct_map[coord] = 0

            # check the adjacents
            for ad_coord in adjacents(*coord):
                if ad_coord in oct_map and oct_map[ad_coord] != 0:
                    oct_map[ad_coord] += 1
                    if oct_map[ad_coord] > 9:
                        flash_later.append(ad_coord)
    print('final amount of flashes', flashes)


def part2():
    oct_map = get_input()
    iteration = 0
    while True:
        iteration += 1
        flash_later = deque()
        for coord in oct_map:
            oct_map[coord] += 1
            if oct_map[coord] > 9:
                flash_later.append(coord)

        while flash_later:
            coord = flash_later.pop()
            # if zero, it has recently flashed, not charging again
            if oct_map[coord] == 0:
                continue
            oct_map[coord] = 0

            # check the adjacents
            for ad_coord in adjacents(*coord):
                if ad_coord in oct_map and oct_map[ad_coord] != 0:
                    oct_map[ad_coord] += 1
                    if oct_map[ad_coord] > 9:
                        flash_later.append(ad_coord)
        if len(list(filter(lambda coord: oct_map[coord] == 0, oct_map))) == len(oct_map):
            break
    print('all flash at iteration', iteration)


if __name__ == '__main__':
    part1()
    part2()
