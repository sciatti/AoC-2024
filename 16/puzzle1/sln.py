from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass
from collections import deque

class Node(TypedDict):
    indices: tuple[int, int]
    edges: list[Edge]

class Edge(TypedDict):
    value: int

@dataclass
class PuzzleInput():
    grid: list[list[str]]
    start: tuple[int, int]
    end: tuple[int, int]
    graph: list[Node]

def parse_input(file_handler):
    puzzle_input: PuzzleInput = PuzzleInput(grid=[], start=(0, 0), end=(0, 0), graph=[])
    for line in file_handler.readlines():
        puzzle_input.grid.append(list(line.rstrip()))
    puzzle_input.start = (len(puzzle_input.grid) - 2, 1)
    puzzle_input.end = (1, len(puzzle_input.grid[0]) - 2)
    
    # up/right/down/left
    search_dirs: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    stack: deque[tuple[int, int]] = deque([puzzle_input.start])
    added_nodes: set[tuple[int, int]] = set([puzzle_input.start])
    puzzle_input.graph.append({'indices': puzzle_input.start, 'edges': []})
    while len(stack) > 0:
        curr_node = stack.pop()
        for dir in search_dirs:
            search_char = curr
    return puzzle_input

def solve(puzzle_input):
    solution = None
    print(f"Solution: {solution}")