import typing


def get_input() -> typing.List[int]:
    with open('input') as f:
        return list(map(int, f.readline().split(',')))


def calc_fuel(target: int, positions: typing.List[int]) -> int:
    fuel = 0
    for pos in positions:
        fuel += abs(target - pos)
    return fuel


def calc_fuel_growing(target: int, positions: typing.List[int]) -> int:
    fuel = 0
    for pos in positions:
        diff = abs(target - pos)
        fuel += sum(range(1, diff + 1))
    return fuel


def find_key(needle: int, haystack: typing.Dict[int, int]) -> int:
    for key in haystack.keys():
        if haystack[key] == needle:
            return key


def part1():
    positions = get_input()
    pos_min = min(positions)
    pos_max = max(positions)

    consumption = {}
    for pos in range(pos_min, pos_max + 1):
        consumption[pos] = calc_fuel(pos, positions)
    min_consumption = min(consumption.values())
    min_consumption_pos = find_key(min_consumption, consumption)
    print(f'Minimum consumption of {min_consumption} at position {min_consumption_pos}')

    # part 2
    consumption = {}
    for pos in range(pos_min, pos_max + 1):
        consumption[pos] = calc_fuel_growing(pos, positions)
    min_consumption = min(consumption.values())
    min_consumption_pos = find_key(min_consumption, consumption)
    print(f'Minimum consumption of {min_consumption} at position {min_consumption_pos}')


if __name__ == '__main__':
    part1()
