import typing


def get_input():
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
            pattern = polymer[i:i+2]
            if pattern in mapping:
                new_polymer.extend((polymer[i], mapping[pattern]))
            else:
                new_polymer.append(polymer[i])
        polymer = ''.join(new_polymer)
    counts = {key: polymer.count(key) for key in set(mapping.values())}
    count_ranking = sorted([v for v in counts.values()])
    print(count_ranking[-1] - count_ranking[0])

def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
