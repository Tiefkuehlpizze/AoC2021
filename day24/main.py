from __future__ import annotations
from functools import cache
import typing

TYPE_SUBROUTINE = typing.List[typing.Tuple[str, str, str]]

routines: typing.List[TYPE_SUBROUTINE]
model_num: str = ''


def get_input() -> typing.List[TYPE_SUBROUTINE]:
    subroutines: typing.List[TYPE_SUBROUTINE] = []
    with open('input') as f:
        routine: TYPE_SUBROUTINE = []
        for line in f:
            instruction, operands = line.rstrip().split(' ', maxsplit=1)
            if instruction == 'inp':
                if len(routine) > 0:
                    subroutines.append(routine)
                routine = []
            else:
                operands = operands.split(' ')
                left, right = operands[0], operands[1] if len(operands) > 1 else ''
                routine.append((instruction, left, right))
        subroutines.append(routine)
    return subroutines


def run_program(subroutine: TYPE_SUBROUTINE, w, z):
    registers = {'w': w, 'x': 0, 'y': 0, 'z': z}

    for instruction, left, right in subroutine:
        right_value: int = registers[right] if right.isalpha() else int(right)

        match instruction:
            case 'add':
                registers[left] += right_value
            case 'mul':
                registers[left] *= right_value
            case 'div':
                assert right_value != 0
                registers[left] = int(registers[left] / right_value)
            case 'mod':
                assert registers[left] >= 0 and right_value > 0
                registers[left] = registers[left] % right_value
            case 'eql':
                registers[left] = int(registers[left] == right_value)
    return registers['z']


@cache
def crack_model_number(routine_idx: int, z: int, inverse=False):
    if z >= 1000000:
        return False

    global model_num
    if routine_idx == len(routines):
        if z == 0:
            return True
        return False

    r = range(9, 0, -1) if not inverse else range(1, 10)
    for w in r:
        model_num += str(w)
        if crack_model_number(routine_idx + 1, run_program(routines[routine_idx], w, z), inverse):
            return True
        model_num = model_num[:-1]
    return False


def part1():
    global model_num, routines
    model_num = ''
    routines = get_input()
    if crack_model_number(0, 0):
        print(model_num)
    else:
        print('something\'s wrong')


def part2():
    global model_num, routines
    model_num = ''
    routines = get_input()
    if crack_model_number(0, 0, inverse=True):
        print(model_num)
    else:
        print('something\'s wrong')


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
