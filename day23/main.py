from __future__ import annotations
import dataclasses
import heapq
import typing

TYPE_ROOMS = typing.List[str]

MOVEMENT_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

DOOR_POSITIONS = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}
LETTERS = list(MOVEMENT_COST)


@dataclasses.dataclass
class State:
    energy: int
    hallway: str
    rooms: TYPE_ROOMS

    def __hash__(self):
        hash_str = self.hallway + ''.join(self.rooms)
        return hash(hash_str)

    def __eq__(self, other: State):
        return hash(self) == hash(other)

    def __lt__(self, other: State):
        return self.energy < other.energy


def get_input(add_part2=False):
    part2_contents = ['DD', 'CB', 'BA', 'AC']
    with open('input') as f:
        raw_board = f.readlines()
        hallway = raw_board[1].count('.') * '.'
        rooms: typing.List[str] = ['', '', '', '']
        for line in raw_board[2:-1]:
            cleaned_line = line[3:-2]
            for room_idx, letter in enumerate(filter(
                    lambda c: c in MOVEMENT_COST.keys(),
                    cleaned_line.rstrip().split('#', maxsplit=4)
            )):
                rooms[room_idx] += letter
        if add_part2:
            for i in range(len(part2_contents)):
                rooms[i] = rooms[i][:1] + part2_contents[i] + rooms[i][1:]
        return hallway, rooms


def set_index(s: str, index: int, c: str) -> str:
    """
    Replaces a letter in a str because strings are immutable
    :param s: the string to replace the character
    :param index: the index of the letter to replace in the string
    :param c: the character to set in the array
    :return: the string with the index replaced
    """
    return s[:index] + c + s[index + 1:]


def calculate_next_moves(current_state: State) -> typing.List[State]:
    next_states = []

    for room_idx in range(len(current_state.rooms)):
        # check if the room is done
        if all([c == LETTERS[room_idx] or c == '.' for c in current_state.rooms[room_idx]]):
            continue

        rooms = list(current_state.rooms)
        letter = '.'
        room_position = 0

        # move an amphipod out of the room
        for room_position, letter in enumerate(current_state.rooms[room_idx]):
            if letter != '.':
                rooms[room_idx] = set_index(rooms[room_idx], room_position, '.')
                break

        for direction in (-1, 1):
            bound = -1 if direction == -1 else len(current_state.hallway)
            for hallway_idx in range(DOOR_POSITIONS[LETTERS[room_idx]], bound, direction):

                # check if the path is blocked
                if current_state.hallway[hallway_idx] != '.':
                    break

                # skip space in front of the "doors"
                if hallway_idx in DOOR_POSITIONS.values():
                    continue

                # closing this state with a new movement to the hallway
                hallway = set_index(current_state.hallway, hallway_idx, letter)
                cost = (room_position + 1 + abs(DOOR_POSITIONS[LETTERS[room_idx]] - hallway_idx)) * MOVEMENT_COST[
                    letter]
                next_states.append(State(cost + current_state.energy, hallway, rooms))

    # move amphipod into a room
    for hallway_idx in range(len(current_state.hallway)):
        if current_state.hallway[hallway_idx] == '.':
            continue
        letter = current_state.hallway[hallway_idx]
        target_room_idx = LETTERS.index(letter)

        # check if all amphipods in the destination room are correct
        if not all([c == letter or c == '.' for c in current_state.rooms[target_room_idx]]):
            continue

        # check if an amphipod blocks the path to the correct room
        direction = 1 if (DOOR_POSITIONS[letter] - hallway_idx) >= 0 else -1
        if any([current_state.hallway[i] != '.' for i in range(
                hallway_idx + direction,
                DOOR_POSITIONS[current_state.hallway[hallway_idx]] + direction,
                direction)]):
            continue

        # search for the right room and the position in it where the amphipod can go
        for room_idx in range(len(current_state.rooms[target_room_idx])):
            if current_state.rooms[target_room_idx][room_idx] == letter:
                break
        else:
            room_idx = len(current_state.rooms[target_room_idx])

        # enter the room
        hallway = set_index(current_state.hallway, hallway_idx, '.')
        rooms = list(current_state.rooms)
        rooms[target_room_idx] = set_index(rooms[target_room_idx], room_idx - 1, letter)

        # store the state
        cost = (abs(DOOR_POSITIONS[letter] - hallway_idx) + room_idx) * MOVEMENT_COST[letter]
        next_states.append(State(cost + current_state.energy, hallway, rooms))

    return next_states


def is_done(state: State) -> bool:
    if any(state.rooms[i] != LETTERS[i] * len(state.rooms[i]) for i in range(len(LETTERS))):
        return False

    if state.hallway.count('.') != len(state.hallway):
        return False
    return True


def part1():
    initial_hallway, initial_rooms = get_input()
    states = [State(0, initial_hallway, initial_rooms)]

    seen_states = set()
    state = None

    while len(states):
        state = heapq.heappop(states)

        if state in seen_states:
            continue
        seen_states.add(state)

        if is_done(state):
            break

        next_moves = calculate_next_moves(state)

        for new_state in next_moves:
            heapq.heappush(states, new_state)
    print(state)


# copy'n'paste again
def part2():

    initial_hallway, initial_rooms = get_input(add_part2=True)
    states = [State(0, initial_hallway, initial_rooms)]

    seen_states = set()
    state = None

    while len(states):
        state = heapq.heappop(states)

        if state in seen_states:
            continue
        seen_states.add(state)

        if is_done(state):
            break

        next_moves = calculate_next_moves(state)

        for new_state in next_moves:
            heapq.heappush(states, new_state)
    print(state)


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs, ) / runs)
    print(timeit(part2, number=runs) / runs)
