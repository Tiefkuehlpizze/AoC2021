import json
import typing


def get_input() -> list:
    with open('input') as f:
        return [json.loads(line) for line in f.readlines()]


def add_leftmost(num, val):
    if val is None:
        return num
    if isinstance(num, list):
        return [add_leftmost(num[0], val), num[1]]
    return num + val


def add_rightmost(num, val):
    if val is None:
        return num
    if isinstance(num, list):
        return [num[0], add_rightmost(num[1], val)]
    return num + val


def explode(number_stack: list, depth=0):
    # boom!
    # If any pair is nested inside four pairs, the leftmost such pair explodes.
    if depth >= 4 and isinstance(number_stack[0], int) and isinstance(number_stack[1], int):
        return True, number_stack[0], number_stack[1], 0

    # check left element
    if isinstance(number_stack[0], list):
        has_exploded, left, right, inner_result = explode(number_stack[0], depth + 1)
        if has_exploded:
            if right:
                return has_exploded, left, None, [inner_result, add_leftmost(number_stack[1], right)]
            else:
                return has_exploded, left, None, [inner_result, number_stack[1]]
    # check right element
    if isinstance(number_stack[1], list):
        has_exploded, left, right, inner_result = explode(number_stack[1], depth + 1)
        if has_exploded:
            if left:
                return has_exploded, None, right, [add_rightmost(number_stack[0], left), inner_result]
            else:
                return has_exploded, None, right, [number_stack[0], inner_result]
    # No more action: Done
    return False, None, None, number_stack


def split(number_stack: list) -> typing.Tuple[bool, list[int, int]]:
    # To split a regular number...
    if isinstance(number_stack, int):
        # If any regular number is 10 or greater, the leftmost such regular number splits
        if number_stack >= 10:
            # ...replace it with a pair
            # left element divided by 2 and rounded down
            # same for right element, but rounded up
            left = number_stack // 2
            return True, [left, number_stack - left]
    else:
        # go deeper
        was_split, n0 = split(number_stack[0])
        # left number is always higher
        if was_split:
            return was_split, [n0, number_stack[1]]
        # ...but right number can also split...
        was_split, n1 = split(number_stack[1])
        if was_split:
            return was_split, [number_stack[0], n1]
        # if not, we're done
    return False, number_stack


def reduce(number_stack: list) -> list:
    changed = True
    # abort condition: no splits and no explosions happened
    while changed:
        changed, _, _, number_stack = explode(number_stack, 0)
        # if no explosion happened, let a split happen that can cause new explosions
        if not changed:
            changed, number_stack = split(number_stack)
    return number_stack


def magnitude(result: list) -> typing.Union[int, list]:
    # go deeper on left and right value until we hit numbers that we can add
    if isinstance(result, list):
        return 3 * magnitude(result[0]) + 2 * magnitude(result[1])
    # otherwise just return the number
    return result


def part1():
    data = get_input()
    # take the first term as starting point
    result = data.pop(0)
    for term in data:
        result = reduce([result, term])
    print(magnitude(result))


def part2():
    data = get_input()
    result = 0
    # combine every line
    for i in range(len(data)):
        for j in range(len(data)):
            result = max(result, magnitude(reduce([data[i], data[j]])))
    print(result)


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
