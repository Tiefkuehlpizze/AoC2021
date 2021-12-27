from __future__ import annotations
import typing

TYPE_FIELD = typing.Dict[typing.Tuple[int, int], str]


def get_input() -> typing.Tuple[TYPE_FIELD, int, int]:
    with open('input') as f:
        field: TYPE_FIELD = dict()
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):
                if c in {'>', 'v'}:
                    field[(y, x)] = c
            size_x = len(line)
        return field, y + 1, size_x


def part1():
    field, size_y, size_x = get_input()

    i = 0
    while True:
        # east-facing (>)
        new_field_0: TYPE_FIELD = dict()
        for coord, direction in field.items():
            if direction == '>':
                cur_y, cur_x = coord
                new_y, new_x = cur_y, cur_x + 1
                new_x %= size_x
                new_y %= size_y
                if (new_y, new_x) not in field:
                    new_field_0[(new_y, new_x)] = direction
                else:
                    new_field_0[(cur_y, cur_x)] = direction
            else:
                new_field_0[coord] = direction

        # south-facing (v)
        new_field_1 = {}
        for coord, direction in new_field_0.items():
            if direction == 'v':
                cur_y, cur_x = coord
                new_y, new_x = cur_y + 1, cur_x
                new_x %= size_x
                new_y %= size_y
                if (new_y, new_x) not in new_field_0:
                    new_field_1[(new_y, new_x)] = direction
                else:
                    new_field_1[(cur_y, cur_x)] = direction
            else:
                new_field_1[coord] = direction
        i += 1
        if field == new_field_1:
            break
        field = new_field_1
    print('Iterations taken:', i)


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    # part 2 is clicking a link and finally find peace
