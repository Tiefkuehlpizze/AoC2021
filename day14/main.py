import typing
from collections import Counter


def get_input() -> typing.Tuple[str, typing.Dict[str, str]]:
    with open('input') as f:
        polymer, raw_mapping = f.read().split('\n\n')
        mapping = {}
        for line in raw_mapping.split('\n'):
            key, value = line.split(' -> ')
            mapping[key] = value
    return polymer, mapping


def part1():
    polymer, mapping = get_input()

    for _ in range(10):
        new_polymer: typing.List[str] = []
        for i in range(len(polymer)):
            pattern = polymer[i:i + 2]
            if pattern in mapping:
                new_polymer.extend((polymer[i], mapping[pattern]))
            else:
                new_polymer.append(polymer[i])
        polymer = ''.join(new_polymer)
    counts = {key: polymer.count(key) for key in set(mapping.values())}
    count_ranking = sorted([v for v in counts.values()])
    print(count_ranking[-1] - count_ranking[0])


def part2():
    polymer, mapping = get_input()

    pattern_count = Counter()
    # Count every existing pattern in the initial polymer
    # do not go for the full length here: it would just be a single letter
    for i in range(len(polymer) - 1):
        pattern_count[polymer[i:i + 2]] += 1
    for _ in range(40):
        new_count = Counter()
        letter_count = Counter()
        for pattern in pattern_count:
            # form the new patten left and right
            left, right = pattern[0] + mapping[pattern], mapping[pattern] + pattern[1]
            # counts for left and right are the same as for the current pattern
            # right will be considered again in the next run
            new_count[left] += pattern_count[pattern]
            new_count[right] += pattern_count[pattern]
            # count the letters in this pattern shaping run
            letter_count[mapping[pattern]] += pattern_count[pattern]
            letter_count[pattern[0]] += pattern_count[pattern]
        pattern_count = new_count
    # add the stripped last character back
    # noinspection PyUnboundLocalVariable
    letter_count[polymer[-1]] += 1
    ranked_letter_count = sorted([v for v in letter_count.values()])
    print(ranked_letter_count[-1] - ranked_letter_count[0])


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
