from collections import defaultdict
import typing

TYPE_CAVE_MAP = defaultdict[str, set[str]]


def get_input() -> TYPE_CAVE_MAP:
    with open('input') as f:
        cave_map = defaultdict(set)
        for line in f:
            origin, destination = line.rstrip().split('-')
            cave_map[origin].add(destination)
            cave_map[destination].add(origin)
        return cave_map


def traverse(cave_map: TYPE_CAVE_MAP, current: str, path: typing.List[str], revisit_done=True) \
        -> typing.List[typing.List[str]]:
    all_paths = []
    for neighbour in cave_map[current]:
        # local copy of the argument to change it for this iteration
        path_revisit_done = revisit_done
        # no visiting small caves again
        if neighbour.islower() and neighbour in path:
            # at least if we already revisited one or if it's start
            if path_revisit_done or neighbour == 'start':
                continue
            else:
                path_revisit_done = True
        discovered_path = path[:]
        discovered_path.append(neighbour)
        # no traversing, if we're at the end, but store the path
        if neighbour == 'end':
            all_paths.append(discovered_path)
        elif neighbour != 'start':
            # do not process start
            all_paths.extend(traverse(cave_map, neighbour, discovered_path, path_revisit_done))
    return all_paths


def part1():
    cave_map = get_input()
    all_paths = traverse(cave_map, 'start', ['start'])
    print(len(all_paths))


def part2():
    cave_map = get_input()
    all_paths = traverse(cave_map, 'start', ['start'], False)
    print(len(all_paths))


if __name__ == '__main__':
    from timeit import timeit
    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
