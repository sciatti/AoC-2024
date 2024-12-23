from __future__ import annotations
from typing import TypedDict
from collections import defaultdict
import math

class PuzzleInput(TypedDict):
    iterations: int
    stones: dict[int, int]

class Stone(TypedDict):
    num: int

def parse_input(file_handler) -> PuzzleInput:
    # create a dict that auto-initializes unfound keys to 0 so you can add to it without ugly and verbose code
    puzzle_input: PuzzleInput = {'iterations': 0, 'stones': defaultdict(lambda: 0)}
    iterations = int(file_handler.readline().rstrip())
    starting_arrangement = [int(num) for num in (file_handler.readline().rstrip()).split(' ')]

    for stone_num in starting_arrangement:
        puzzle_input['stones'][stone_num] += 1

    puzzle_input['iterations'] = iterations
    return puzzle_input

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

    operation_table: dict[int, tuple[int, int | None]] = {0 : (1, None)}

    # use a dictionary to keep track of every stone number you've seen before,
    # calculate it if you have not seen it before, otherwise use its data
    for iter_num in range(1, puzzle_input['iterations'] + 1):
        new_stones: defaultdict[int, int] = defaultdict(lambda: 0)
        for stone_key, frequency in puzzle_input['stones'].items():
            # if we find a result we have seen already...
            if stone_key in operation_table:
                result_1, result_2 = operation_table[stone_key]
                new_stones[result_1] += frequency
                # if we split the input number, result_2 will not be none
                if result_2 is not None:
                    new_stones[result_2] += frequency
            elif get_num_digits(stone_key) % 2 == 0:
                num_dig = get_num_digits(stone_key)
                size = num_dig // 2
                # split the stone into two
                left_stone = first_n_digits(stone_key, size)
                right_stone = last_n_digits(stone_key, size)
                # assign the left and right stones into the new_stones dict
                new_stones[left_stone] += frequency
                new_stones[right_stone] += frequency
                # add this operation to the table for future lookups
                operation_table[stone_key] = (left_stone, right_stone)
            else:
                # calculate the result
                result = stone_key * 2024
                # udpdate the new stones dict
                new_stones[result] += frequency
                # store this operation in the table for future lookups
                operation_table[stone_key] = (result, None)
        puzzle_input['stones'] = new_stones

        print(f"finished iteration: {iter_num} with {sum([x for x in puzzle_input['stones'].values()])} stones")

    solution = 0
    for frequency in puzzle_input['stones'].values():
        solution += frequency

    print(f"Solution: {solution}")