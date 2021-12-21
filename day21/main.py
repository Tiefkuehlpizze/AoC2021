import itertools
import typing

from functools import cache


def get_input() -> typing.List[int]:
    with open('input') as f:
        return [int(line.split()[-1]) for line in f]


def throw_die(start_position: int, die: itertools.cycle, count=3) -> int:
    position = start_position + sum(next(die) for _ in range(count))
    score = position % 10
    return score if score > 0 else 10


@cache
def split_universe(scores: typing.Tuple[int], positions: typing.Tuple[int]) -> typing.Tuple[int, int]:
    win, lose = 0, 0
    # for every possible dice result out of 3 dice with values 1,2,3
    for die in itertools.product([1, 2, 3], repeat=3):
        # calculate new position and score
        new_position = (positions[0] + sum(die)) % 10
        new_position = new_position if new_position > 0 else 10
        new_score = scores[0] + new_position

        # if the score leads to a win, count it... Game ends
        if new_score >= 21:
            win += 1
        else:
            # ... if not: Swap positions, scores, win and lose counter and play another turn
            recursion_lose, recursion_win = split_universe((scores[1], new_score), (positions[1], new_position))
            win += recursion_win
            lose += recursion_lose
    # if all combinations were played, return the win and loss counters
    return win, lose


def part1():
    dice_per_turn = 3
    start_positions = get_input()
    die = itertools.cycle(range(1, 101))

    scores = [0, 0]
    positions = list(start_positions)
    dice_thrown = 0

    game_running = True
    while game_running:
        for player, position in enumerate(positions):
            positions[player] = throw_die(position, die, dice_per_turn)
            scores[player] += positions[player]
            dice_thrown += dice_per_turn
            if scores[player] >= 1000:
                game_running = False
                break
    print(min(scores) * dice_thrown)


def part2():
    start_positions = tuple(get_input())
    scores = (0, 0)
    print(max(split_universe(scores, start_positions)))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
