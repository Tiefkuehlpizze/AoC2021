import dataclasses
import typing


@dataclasses.dataclass()
class Point:
    x: int
    y: int


def is_horizontal_or_vertical(p1: Point, p2: Point):
    return p1.x == p2.x or p1.y == p2.y


class Grid:
    _grid: typing.List[typing.List[int]]

    def __init__(self, size):
        self._grid = [
            [0] * size for _ in range(size)
        ]

    def draw(self, p1: Point, p2: Point):
        if is_horizontal_or_vertical(p1, p2):
            self.draw_hv_line(p1, p2)
        else:
            self.draw_diagonal_line(p1, p2)

    def draw_hv_line(self, p1: Point, p2: Point):
        if not is_horizontal_or_vertical(p1, p2):
            print('Not drawing diagonal line', p1, p2)
            return

        print('Drawing line', p1, p2)
        x_start = min(p1.x, p2.x)
        y_start = min(p1.y, p2.y)
        x_end = max(p1.x, p2.x) + 1
        y_end = max(p1.y, p2.y) + 1

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                self._grid[y][x] += 1

    def draw_diagonal_line(self, p1: Point, p2: Point):
        print('Drawing diagonal line', p1, p2)
        x_dir = 1 if p1.x < p2.x else -1
        y_dir = 1 if p1.y < p2.y else -1

        x, y = (p1.x, p1.y)
        while True:
            self._grid[y][x] += 1
            if x == p2.x:
                break
            x += x_dir
            y += y_dir

    def get_overlap_count_for(self, how_many):
        return sum([len(list(filter(lambda x: x >= how_many, row))) for row in self._grid])


def parse_point(line: str) -> typing.Tuple[Point, Point]:
    p1_raw, p2_raw = line.split(' -> ')
    return Point(*map(int, p1_raw.split(','))), Point(*map(int, p2_raw.split(',')))


def part1():
    grid = Grid(1000)
    with open('input') as f:
        for line in f:
            grid.draw_hv_line(*parse_point(line.rstrip()))
    print(grid.get_overlap_count_for(2))


def part2():
    grid = Grid(1000)
    with open('input') as f:
        for line in f:
            grid.draw(*parse_point(line.rstrip()))
    print(grid.get_overlap_count_for(2))


if __name__ == '__main__':
    # part1()
    part2()
