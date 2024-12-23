from __future__ import annotations
from typing import TypedDict
import math

class PuzzleInput(TypedDict):
    iterations: int
    firstStone: Stone

class Stone(TypedDict):
    num: int
    next: Stone | None

def parse_input(file_handler) -> PuzzleInput:
    puzzle_input: PuzzleInput = {'iterations': 0, 'stones': []}
    iterations = int(file_handler.readline().rstrip())
    starting_arrangement = [int(num) for num in (file_handler.readline().rstrip()).split(' ')]

    starting_stone = Stone(num=starting_arrangement[0], next=None)
    prev_stone = starting_stone
    for stone_num in range(1, len(starting_arrangement)):
        curr_stone = Stone(num=starting_arrangement[stone_num], next=None)
        prev_stone['next'] = curr_stone
        prev_stone = curr_stone

    puzzle_input['iterations'] = iterations
    puzzle_input['firstStone'] = starting_stone
    return puzzle_input

def print_stones(iter_num: int, firstStone: Stone) -> None:
    stones = []
    cs = firstStone
    while cs is not None:
        stones.append(cs['num'])
        cs = cs['next']

    print(f"After {iter_num} blinks:\n{" ".join([str(stone) for stone in stones])}")

def solve(puzzle_input: PuzzleInput) -> None:

    def get_num_digits(n: int) -> int:
        if n > 0:
            return int(math.log10(n))+1
        elif n == 0:
            return 1
        else:
            return int(math.log10(-n))+2 # +1 if you don't count the '-'

    def first_n_digits(num: int, n: int) -> int:
        return int(str(num)[:n])
    def last_n_digits(num: int, n: int) -> int:
        return int(str(num)[n:])

    # print_stones(0, puzzle_input['firstStone'])
    # print()

    for iter_num in range(1, puzzle_input['iterations'] + 1):
        curr_stone: Stone = puzzle_input['firstStone']
        while curr_stone is not None:
            stone_digits: int = get_num_digits(curr_stone['num'])
            if curr_stone['num'] == 0:
                curr_stone['num'] = 1
            elif stone_digits % 2 == 0:
                # split the stone into two 
                #   ie: reassign the num of the current stone and make a new one which links into the next of current
                old_num = curr_stone['num']
                curr_stone['num'] = first_n_digits(old_num, stone_digits // 2)
                right_stone = Stone(num=last_n_digits(old_num, stone_digits // 2), next=curr_stone['next'])
                # reassign current stone's next pointer to the right stone
                curr_stone['next'] = right_stone
                # iterate to the right_stone to prevent operating on a stone added in this iteration
                curr_stone = right_stone
            else:
                curr_stone['num'] = curr_stone['num'] * 2024
            curr_stone = curr_stone['next']
        # print_stones(iter_num, puzzle_input['firstStone'])
        # print()
        print(f"finished iteration: {iter_num}")
    solution = 0
    stone = puzzle_input['firstStone']
    while stone is not None:
        solution += 1
        stone = stone['next']
    print(f"Solution: {solution}")