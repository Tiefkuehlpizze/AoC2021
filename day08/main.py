import typing


def get_input() -> typing.List[str]:
    with open('input') as f:
        return f.readlines()


def part1():
    signals = []
    for line in get_input():
        signals.extend(line.split(' | ')[1].rstrip().split(' '))
    digit_count = sum(len(digit) in (2, 3, 4, 7) for digit in signals)
    print(digit_count)


def part2():
    lines = get_input()
    overall_result = 0
    for line in lines:
        signal_pattern, output = line.rstrip().split(' | ')

        number_to_str_mapping = {}
        for c, v in ((2, 1), (4, 4), (3, 7), (7, 8)):
            number_to_str_mapping[v] = set(''.join(pattern for pattern in signal_pattern.split() if len(pattern) == c))

        number_to_str_mapping[3] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if len(pattern) == 5
            and len(set(pattern) & set(number_to_str_mapping[7])) == 3
        ))

        number_to_str_mapping[9] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if set(pattern) == set(
                number_to_str_mapping[3] | number_to_str_mapping[4])
        ))

        number_to_str_mapping[0] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if len(pattern) == 6
            and set(pattern) not in number_to_str_mapping.values()
            and len(set(pattern) & number_to_str_mapping[1]) == 2
        ))

        number_to_str_mapping[6] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if len(pattern) == 6
            and set(pattern) not in number_to_str_mapping.values()
        ))

        number_to_str_mapping[5] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if len(pattern) == 5
            and set(pattern) not in number_to_str_mapping.values()
            and len(number_to_str_mapping[6] - set(pattern)) == 1
        ))

        number_to_str_mapping[2] = set(''.join(
            pattern for pattern in signal_pattern.split()
            if len(pattern) == 5
            and set(pattern) not in number_to_str_mapping.values()
        ))

        decoder = {}
        for number, signals in number_to_str_mapping.items():
            representation = ''.join(sorted(signals))
            decoder[representation] = number

        output_numbers = output.split()
        result = 0
        for i, munge in zip(range(len(output_numbers) - 1, -1, -1), output_numbers):
            result += 10 ** i * decoder[''.join(sorted(munge))]
        overall_result += result
    print(overall_result)


if __name__ == '__main__':
    part1()
    part2()
