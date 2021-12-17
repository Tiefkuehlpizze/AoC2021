import dataclasses
import typing


@dataclasses.dataclass
class Rect:
    x1: int
    x2: int
    y1: int
    y2: int

    def collides_point(self, x, y):
        return self.x1 <= x <= self.x2 \
               and self.y1 <= y <= self.y2

    def point_missed(self, x, y):
        return x > self.x2 or y > self.y2


def get_input() -> typing.Tuple[int, int, int, int]:
    with open('input') as f:
        x_dec, y_dec = f.read().rstrip().split(' ', 2)[2].split(', ')[0:2]
        x_start, x_end = x_dec[2:].split('..')
        y_start, y_end = y_dec[2:].split('..')
        return int(x_start), int(x_end), int(y_start), int(y_end)


def part1():
    target_area = Rect(*get_input())
    # triangular numbers formula: f(y) = (y*(y-1)/2
    # we want to hit the highest y of the target area
    # This program has no checks, whether y2 is greater than y1
    # This also might not work for all inputs
    print((abs(target_area.y1) * (abs(target_area.y1) - 1)) / 2)


def part2():
    target_area = Rect(*get_input())
    found = set()

    for x in range(1, target_area.x2 + 1):
        for y in range(target_area.y1, abs(target_area.y1)):
            xv, yv = x, y
            xp = yp = 0
            while True:
                xp += xv
                yp += yv
                xv = max(xv - 1, 0)
                yv -= 1

                if target_area.collides_point(xp, yp):
                    found.add((x, y))
                    break
                if xp > target_area.x2 or yp < target_area.y1:
                    break
    #print(sorted(found))
    print(len(found))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
