import typing

DOTS_TYPE = typing.Set[typing.Tuple[int, int]]


def get_input():
    with open('input') as f:
        # 2 pieces contained: dots and commands separated by \n\n
        dot_line, command_lines = f.read().split('\n\n')
        # create the dot matrix with only the marked dots
        dots = set()
        for line in dot_line.splitlines():
            x, y = line.rstrip().split(',')
            dots.add((int(x), int(y)))

        folding_instructions = []
        for line in command_lines.splitlines():
            assignment_idx = line.index('=')
            folding_instructions.append((
                line[assignment_idx - 1],
                int(line[assignment_idx + 1:])
            ))
        return dots, folding_instructions


def fold(dots: DOTS_TYPE, folding_line: str, folding_idx: int) -> DOTS_TYPE:
    folding_copy = set()
    # folding_line can be x or y
    # logic is, that we do not care about dots after the folding index
    # and calculate their new position after folding
    if folding_line == 'x':
        for x, y in dots:
            folding_copy.add((
                x if x < folding_idx else folding_idx - (x - folding_idx),
                y
            ))
    else:
        for x, y in dots:
            folding_copy.add((
                x,
                y if y < folding_idx else folding_idx - (y - folding_idx)
            ))
    return folding_copy


def part1():
    dots, instructions = get_input()
    for folding_line, folding_idx in instructions:
        dots = fold(dots, folding_line, folding_idx)
        # part 1 only does one fold
        break
    print(len(dots))


def part2():
    dots, instructions = get_input()
    for folding_line, folding_idx in instructions:
        dots = fold(dots, folding_line, folding_idx)
    # calculate display size
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    # print dot by dot. not efficient, but works
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print('#' if (x, y) in dots else '.', end='')
        print()


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
