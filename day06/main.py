import typing
from collections import deque, Counter


def calc_for_days(initial: typing.List[int], days: int) -> int:
    c = Counter(initial)
    pond = deque(c[i] for i in range(9))
    for day in range(days):
        pond.rotate(-1)
        pond[6] += pond[8]
    return sum(pond)


def part1():
    with open('input') as f:
        print(calc_for_days([int(age) for age in f.readline().split(',')], 18))


def part2():
    with open('input') as f:
        print(calc_for_days([int(age) for age in f.readline().split(',')], 256))


if __name__ == '__main__':
    part1()
    part2()
