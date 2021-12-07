import sys


def part1():
    increases = 0
    previous = sys.maxsize
    with open('input') as f:
        for line in f.readlines():
            current = int(line)
            if current > previous:
                increases += 1
            previous = current
    print(increases)


def part2():
    increases = 0
    prev_window = sys.maxsize
    with open('input') as f:
        data = [int(line) for line in f]
    for i in range(2, len(data)):
        cur_window = sum(data[i - 2:i + 1])
        if cur_window > prev_window:
            increases += 1
        prev_window = cur_window
    print(increases)


if __name__ == '__main__':
    part2()
