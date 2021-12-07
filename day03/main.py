import functools


def part1():
    with open('input') as f:
        raw_data = list(map(lambda x: x.rstrip(), f.readlines()))
    gamma_rate = 0
    epsilon = 0
    for i in range(12):
        if sum(map(lambda x: int(x[-i - 1]), raw_data)) > len(raw_data) / 2:
            gamma_rate += 1 << i
        else:
            epsilon += 1 << i
    print(gamma_rate * epsilon)


def part2():
    def most_common_value(input_data: list[str], index: int) -> str:
        return '1' if sum(map(lambda x: int(x[index]), input_data)) >= len(input_data) / 2 else '0'
    with open('input') as f:
        raw_data = list(map(lambda x: x.rstrip(), f.readlines()))
    oxygen_gen_haystack = list(raw_data)
    co2_scrub_haystack = list(raw_data)
    for i in range(len(raw_data[0])):
        most_common_bit = most_common_value(oxygen_gen_haystack, i)
        new_oxygen_gen_haystack = list(filter(lambda x: x[i] == most_common_bit, oxygen_gen_haystack))
        oxygen_gen_haystack = new_oxygen_gen_haystack

    for i in range(len(raw_data[0])):
        most_common_bit = most_common_value(co2_scrub_haystack, i)
        new_co2_scrub_haystack = list(filter(lambda x: x[i] != most_common_bit, co2_scrub_haystack))
        co2_scrub_haystack = new_co2_scrub_haystack
        if len(new_co2_scrub_haystack) == 1:
            break

    print(int(oxygen_gen_haystack[0], 2) * int(co2_scrub_haystack[0], 2))


if __name__ == '__main__':
    part1()
    part2()
