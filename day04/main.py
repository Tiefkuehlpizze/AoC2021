import typing
from pprint import pprint, pformat


class Board:
    _game_field: typing.List[typing.List[int]]
    _marks: typing.List[typing.List[bool]]

    def __init__(self, game_field: typing.List[typing.List[int]]):
        self._game_field = game_field
        self._marks = [[False] * len(game_field) for _ in range(len(game_field[0]))]

    def mark_number(self, number: int):
        for y, row in enumerate(self._game_field):
            try:
                x = row.index(number)
                self._marks[y][x] = True
            except ValueError:
                pass

    def check_bingo(self):
        for y in range(len(self._marks[0])):
            col = [self._marks[x][y] for x in range(len(self._marks[y]))]
            if all(self._marks[y]) or all(col):
                return True
        return False

    def calc_score(self, number: int):
        unchecked_sum = 0
        for y in range(len(self._game_field)):
            for x in range(len(self._game_field[y])):
                if not self._marks[y][x]:
                    unchecked_sum += self._game_field[y][x]
        print(unchecked_sum, '*', number, '=', unchecked_sum * number)
        return unchecked_sum * number

    def __repr__(self):
        return pformat(self._marks)


def read_bingo_field(f) -> typing.List[typing.List[int]]:
    current_game_field = []
    for line in f:
        if line.isspace():
            if len(current_game_field) == 5:
                yield current_game_field
                current_game_field = []
                continue
            else:
                continue
        current_game_field.append(list(map(int, line.rstrip().split())))
    yield current_game_field


def part1():
    with open('input') as f:
        numbers = map(int, f.readline().split(','))
        game_fields = [Board(field) for field in list(read_bingo_field(f))]
    for number in numbers:
        print('draw', number)
        for game_field in game_fields:
            game_field.mark_number(number)
            if game_field.check_bingo():
                print(game_fields.index(game_field), 'wins with score', game_field.calc_score(number))
                break
        else:
            continue
        break


def part2():

    with open('input') as f:
        numbers = map(int, f.readline().split(','))
        game_fields = [Board(field) for field in list(read_bingo_field(f))]
    for number in numbers:
        print('draw', number)
        to_remove = []
        for game_field in game_fields:
            game_field.mark_number(number)
            if game_field.check_bingo():
                winning_score = game_field.calc_score(number)
                print(game_fields.index(game_field), 'wins with score', winning_score)
                to_remove.append(game_field)
        [game_fields.remove(g) for g in to_remove]
    print('last score', winning_score)


if __name__ == '__main__':
    part1()
    part2()
