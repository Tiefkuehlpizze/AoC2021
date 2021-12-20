import typing
# these two methods, I've never found a use for, were very handy in this case
# I wrote everything by hand and tried to optimize this stupid task and found solutions using these
from itertools import permutations, product
from collections import Counter

TYPE_BEACON = typing.Tuple[int, int, int]
TYPE_BEACON_MAP = typing.Set[TYPE_BEACON]
TYPE_COORDINATE = TYPE_BEACON


def get_input() -> typing.List[TYPE_BEACON_MAP]:
    scanners: typing.List[TYPE_BEACON_MAP] = []
    with open('input') as f:
        all_scanner_reports = f.read().split('\n\n')
        for scanner in all_scanner_reports:
            beacons: typing.List[typing.Tuple[int, int, int]] = []
            for beacon in scanner.split("\n")[1:]:
                x, y, z = beacon.split(',')
                beacons.append((int(x), int(y), int(z)))
            scanners.append(set(beacons))
        return scanners


def get_all_possible_orientations(scanner: TYPE_BEACON_MAP) -> typing.Generator[TYPE_BEACON_MAP, None, None]:
    # Don't ask me, this is probably one of the core pieces of this puzzle
    # I know what it does and I've done matrix calculations years ago, but I've never
    # practically used it on my own (I'm bad a graphics)

    # every x, y, z accessed by index
    for perm in permutations((0, 1, 2)):
        # every combination of positive and negative values
        for sign_x, sign_y, sign_z in product((-1, 1), repeat=3):
            yield set([(
                x[perm[0]] * sign_x,
                x[perm[1]] * sign_y,
                x[perm[2]] * sign_z
            ) for x in scanner])


def recalculate_position_by_offset(coordinates: TYPE_BEACON_MAP, offset: TYPE_COORDINATE) -> TYPE_BEACON_MAP:
    return set(map(lambda pt: (pt[0] - offset[0], pt[1] - offset[1], pt[2] - offset[2]), coordinates))


def get_all_distance_pairs(beacon_map: TYPE_BEACON_MAP, other_scanner: TYPE_BEACON_MAP) \
        -> typing.Tuple[bool, typing.Optional[TYPE_COORDINATE], typing.Optional[TYPE_BEACON_MAP]]:
    # get all beacon's coordinates in all possible orientations...
    for other_scanner_rotated in get_all_possible_orientations(other_scanner):
        distances = Counter()
        # ... and try to match them with the known beacons in every possible combination
        for base_beacon, other_beacon in product(beacon_map, other_scanner_rotated):
            # calculate distances
            distance = (
                other_beacon[0] - base_beacon[0],
                other_beacon[1] - base_beacon[1],
                other_beacon[2] - base_beacon[2]
            )
            # increment the counter for the distance between the two beacons in the current orientation
            # The idea is, that we'll find multiple beacons with the same distance (at least 12) and
            # identify this as the correct values.
            distances[distance] += 1
        # get the distance with the most common beacons
        distance: TYPE_COORDINATE
        distance, num_common_beacons = distances.most_common(1)[0]
        if num_common_beacons >= 12:
            # recalculate the coordinates as seen from the base position (satellite 0)
            common_beacons = recalculate_position_by_offset(other_scanner_rotated, distance)
            return True, distance, common_beacons
    return False, None, None


def manhattan_distance(pos1: TYPE_COORDINATE, pos2: TYPE_COORDINATE) -> int:
    return sum(abs(p - q) for p, q in zip(pos1, pos2))


def calculate_distances(offsets: typing.Set[TYPE_COORDINATE]) -> typing.Set[int]:
    return set(manhattan_distance(pos1, pos2) for pos1, pos2 in product(offsets, repeat=2))


def part1and2():
    scanners = get_input()

    num_scanners = len(scanners)
    # initialize with satellite 0's data
    # beacon_map contains all beacons in sat0's orientation
    # it'll be updated with new beacons after every iteration if there were new beacons detected
    beacon_map: TYPE_BEACON_MAP = set(scanners[0])
    # offsets contains the offset (rotation) of every satellite
    # sat0 is the origin and turn point of everything, so it's (0,0,0)
    offsets = {(0, 0, 0)}
    scanner_idx_todo = set(range(1, len(scanners)))
    scanner_idx_found = {0}

    # try to complete the beacon map
    # once the 12 overlapping beacons were found, the satellite's position is considered as detected
    while num_scanners != len(offsets):
        for scanner_idx in set(scanner_idx_todo):
            found, distance, beacons = get_all_distance_pairs(beacon_map, scanners[scanner_idx])

            if found:
                # remove the scanner, to avoid reprocessing it
                scanner_idx_found.add(scanner_idx)
                scanner_idx_todo.remove(scanner_idx)
                # add the distance offset to the store for part2
                offsets.add(distance)
                # finally: add the newly detected beacons to the atlas
                beacon_map.update(beacons)
    print('Part 1 solution:', len(beacon_map))
    print('Part 2 solution:', max(calculate_distances(offsets)))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1and2, number=runs) / runs)
