import dataclasses
import typing

TYPE_COORDINATE = typing.Tuple[int, int, int]
TYPE_GRID = typing.Set[TYPE_COORDINATE]
TYPE_GRID2 = typing.List['Cuboid']


@dataclasses.dataclass
class Command:
    on: bool
    x: typing.Tuple[int, int]
    y: typing.Tuple[int, int]
    z: typing.Tuple[int, int]

    @classmethod
    def parse(cls, line: str) -> 'Command':
        toggle, area_str = line.rstrip().split(' ')
        x_str, y_str, z_str = area_str.split(',')
        x, y, z = x_str.split('..'), y_str.split('..'), z_str.split('..')
        return cls(toggle == 'on',
                   (int(x[0].split('=')[1]), int(x[1]) + 1),
                   (int(y[0].split('=')[1]), int(y[1]) + 1),
                   (int(z[0].split('=')[1]), int(z[1]) + 1)
                   )


@dataclasses.dataclass
class Cuboid:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    def __init__(self, x0, x1, y0, y1, z0, z1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1

    def __hash__(self):
        return hash(repr(self))

    @property
    def size(self) -> int:
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0)


def contains(c1: Cuboid, c2: Cuboid) -> bool:
    return (
            c1.x0 <= c2.x0 and
            c1.x1 >= c2.x1 and
            c1.y0 <= c2.y0 and
            c1.y1 >= c2.y1 and
            c1.z0 <= c2.z0 and
            c1.z1 >= c2.z1
    )


def intersects(c1: Cuboid, other: Cuboid) -> bool:
    return (
            c1.x0 <= other.x1 - 1 and
            c1.x1 - 1 >= other.x0 and
            c1.y0 <= other.y1 - 1 and
            c1.y1 - 1 >= other.y0 and
            c1.z0 <= other.z1 - 1 and
            c1.z1 - 1 >= other.z0
    )


def combine_cubes(c1: Cuboid, c2: Cuboid) -> typing.List[Cuboid]:
    if not intersects(c1, c2):
        return [c1]
    elif contains(c2, c1):
        return []

    xs = sorted([c1.x0, c1.x1, c2.x0, c2.x1])
    ys = sorted([c1.y0, c1.y1, c2.y0, c2.y1])
    zs = sorted([c1.z0, c1.z1, c2.z0, c2.z1])
    result = []
    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            for z0, z1 in zip(zs, zs[1:]):
                chunk = Cuboid(x0, x1, y0, y1, z0, z1)
                if contains(c1, chunk) and not intersects(chunk, c2):
                    result.append(chunk)

    return result


def get_input() -> typing.Tuple[Command]:
    with open('input') as f:
        return tuple([Command.parse(line) for line in f])


def execute_command(grid: TYPE_GRID, command: Command) -> None:
    area = {
        (x, y, z)
        for x in range(max(command.x[0], -50), min(command.x[1], 50) + 1)
        for y in range(max(command.y[0], -50), min(command.y[1], 50) + 1)
        for z in range(max(command.z[0], -50), min(command.z[1], 50) + 1)
    }
    if command.on:
        grid |= area
    else:
        grid -= area


def part1():
    commands = get_input()
    grid = set()
    for command in commands:
        execute_command(grid, command)

    print(len(grid))


def part2():
    commands = get_input()
    grid: TYPE_GRID2 = []

    for i, command in enumerate(commands):
        c1 = Cuboid(*command.x, *command.y, *command.z)
        new_grid = []
        for other in grid:
            r = combine_cubes(other, c1)
            if r:
                new_grid.extend(r)
        if command.on:
            new_grid.append(c1)
        grid = new_grid
    print(sum(chunk.size for chunk in grid))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
