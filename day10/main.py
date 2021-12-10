from collections import deque
from statistics import median
import typing

SCORES_ERROR = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

SCORES_AUTOCOMPLETE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

TOKEN_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
REVERSE_PAIRS = {v: k for k, v in TOKEN_PAIRS.items()}


def get_input() -> typing.List[str]:
    with open('input') as f:
        return list(map(str.rstrip, f))


def part1():
    score = 0
    for line in get_input():
        token_stack = deque()
        for token in line:
            # if it's an opener, add it to the stack
            if token in TOKEN_PAIRS:
                token_stack.append(token)
            else:
                # check if the token matches the last opening token
                if token_stack[-1] == REVERSE_PAIRS[token]:
                    token_stack.pop()
                else:
                    # syntax error! SCORE!
                    score += SCORES_ERROR[token]
                    break
    print(score)


def part2():
    scores = []
    for line in get_input():
        token_stack = deque()
        for token in line:
            # if it's an opener, add it to the stack
            if token in TOKEN_PAIRS:
                token_stack.append(token)
            else:
                # check if the token matches the last opening token
                if token_stack[-1] == REVERSE_PAIRS[token]:
                    token_stack.pop()
                else:
                    # syntax error! Discard
                    break
        else:
            score = 0
            while token_stack:
                score = score * 5 + SCORES_AUTOCOMPLETE[TOKEN_PAIRS[token_stack.pop()]]
            scores.append(score)
    # middle score of sorted scores
    print(int(median(scores)))


if __name__ == '__main__':
    part1()
    part2()
