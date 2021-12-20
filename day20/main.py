import typing
from collections import defaultdict

TYPE_IMAGE = defaultdict[int, defaultdict[int, str]]


def get_input() -> typing.Tuple[str, str]:
    with open('input') as f:
        algorithm, image = f.read().split('\n\n')
        return (algorithm.rstrip().replace('.', '0').replace('#', '1'),
                image.rstrip().replace('.', '0').replace('#', '1').split('\n'))


def get_pixel_square_as_dec(image, x, y) -> int:
    result = ''
    for y_cur in range(y - 1, y + 2):
        for x_cur in range(x - 1, x + 2):
            result += image[y_cur][x_cur]
    return int(result, 2)


def print_image(image: TYPE_IMAGE):
    for row in image.values():
        print(''.join(row.values()))


def get_new_pixel(algorithm, position) -> str:
    return algorithm[position]


def expand_image(algorithm: str, source_image: TYPE_IMAGE, infinity_value: str) -> TYPE_IMAGE:
    # prepare another defaultdict as target for the expanded image
    size_x, size_y = len(source_image[0]), len(source_image)
    new_image = defaultdict(lambda: defaultdict(lambda: infinity_value))
    for y in range(-1, size_y + 1):
        for x in range(-1, size_x + 1):
            # fill new image at (y+1,x+1) because we want to avoid negative keys
            # it would cause wrong calculations on the next run due to the loop's range
            new_image[y + 1][x + 1] = get_new_pixel(algorithm, get_pixel_square_as_dec(source_image, x, y))
    return new_image


def part1():
    algorithm, image = get_input()

    # prepare the image using defaultdict to avoid messing with borders
    cur_image = defaultdict(lambda: defaultdict(lambda: '0'))
    for y, row in enumerate(image):
        for x, value in enumerate(row):
            cur_image[y][x] = value
    for i in range(2):
        # today's trick: the infinity is initially 0, so we must replace the infinity aka default value
        # checks if i is even or uneven and negates the value
        universe_blink = str(i & 1 ^ 1)
        cur_image = expand_image(algorithm, cur_image, universe_blink)
    print(sum([y for y in x.values()].count('1') for x in cur_image.values()))


def part2():
    # lol copy'n'paste
    algorithm, image = get_input()

    # prepare the image using defaultdict to avoid messing with borders
    cur_image = defaultdict(lambda: defaultdict(lambda: '0'))
    for y, row in enumerate(image):
        for x, value in enumerate(row):
            cur_image[y][x] = value
    for i in range(50):
        # today's trick: the infinity is initially 0, so we must replace the infinity aka default value
        # checks if i is even or uneven and negates the value
        universe_blink = str(i & 1 ^ 1)
        cur_image = expand_image(algorithm, cur_image, universe_blink)
    print(sum([y for y in x.values()].count('1') for x in cur_image.values()))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
