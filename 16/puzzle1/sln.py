from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue

search_dirs: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Node(TypedDict):
    orientation: str # U/D/L/R for up/down/left/right
    indices: tuple[int, int]

@dataclass
class PuzzleInput():
    grid: list[list[str]]
    start: tuple[int, int]
    end: tuple[int, int]

def parse_input(file_handler) -> PuzzleInput:
    puzzle_input: PuzzleInput = PuzzleInput(grid=[], start=(0, 0), end=(0, 0), graph=[])
    for line in file_handler.readlines():
        puzzle_input.grid.append(list(line.rstrip()))
    puzzle_input.start = (len(puzzle_input.grid) - 2, 1)
    puzzle_input.end = (1, len(puzzle_input.grid[0]) - 2)

    return puzzle_input

def cost_heuristic(puzzle_input: PuzzleInput, current_node: Node) -> int:
    num_turns = 0
    # calculate the minimal turns required to get to the goal in a maze with no walls
    if current_node['orientation'] == 'R':
        # form a backwards L, 1 turn required
        num_turns = 1
    elif current_node['orientation'] == 'U':
        # forms an upside down L, 1 turn required
        num_turns = 1
    # corner case where we're on the same row as the end-square
    if puzzle_input.end[0] == current_node['indices'][0]:
        return num_turns * 1000 + (puzzle_input.end[1] - current_node['indices'][1])
    # corner case where we're on the same col as the end-square and facing 
    if puzzle_input.end[0] == current_node['indices'][0]:
        return num_turns * 1000 + (puzzle_input.end[1] - current_node['indices'][1])

def solve(puzzle_input: PuzzleInput) -> None:
    solution = None
    print(f"Solution: {solution}")