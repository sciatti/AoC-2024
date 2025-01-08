from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass
from collections import defaultdict
from queue import PriorityQueue
import math

search_dirs: dict[str, tuple[int, int]] = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

horiz_set = set(['L', 'R'])
vert_set = set(['U', 'D'])

@dataclass
class Node():
    orientation: str # U/D/L/R for up/down/left/right
    indices: tuple[int, int]
    timestamp: int

    def __lt__(self, other: Node):
        return self.timestamp < other.timestamp
    def __eq__(self, other):
        return self.timestamp == other.timestamp
@dataclass
class PuzzleInput():
    grid: list[list[str]]
    start: tuple[int, int]
    end: tuple[int, int]

def parse_input(file_handler) -> PuzzleInput:
    puzzle_input: PuzzleInput = PuzzleInput(grid=[], start=(0, 0), end=(0, 0))
    for line in file_handler.readlines():
        puzzle_input.grid.append(list(line.rstrip()))
    puzzle_input.start = (len(puzzle_input.grid) - 2, 1)
    puzzle_input.end = (1, len(puzzle_input.grid[0]) - 2)

    return puzzle_input

def cost_heuristic(puzzle_input: PuzzleInput, current_node: Node) -> int:
    num_turns = 0
    # calculate the minimal turns required to get to the goal in a maze with no walls
    if current_node.orientation == 'R':
        # form a backwards L, 1 turn required
        # check for corner case where we're on the same row as the end-square and facing right, no turn required
        if puzzle_input.end[0] != current_node.indices[0]:
            num_turns = 1
    elif current_node.orientation == 'U':
        # forms an upside down L, 1 turn required
        # corner case where we're on the same col as the end-square and facing up, no turn required
        if puzzle_input.end[1] != current_node.indices[1]:
            num_turns = 1
    elif current_node.orientation == 'L':
        # forms an L turned clockwise 90 degrees, 
        # needs to turn right, move upwards, and then turn right again and move right, requires 2 turns
        # corner case where we're on the same col as the end-square, only needs 1 turn 
        if puzzle_input.end[1] != current_node.indices[1]:
            num_turns = 2
        else:
            num_turns = 1
    # must be facing down
    else:
        # forms an L that is reversed horizontally,
        # needs to turn left, move right, and then turn left again and move up, requires 2 turns
        # corner case exists where we're on the same row as the end-square, only needs 1 turn
        if puzzle_input.end[0] != current_node.indices[0]:
            num_turns = 2
        else:
            num_turns = 1
    return num_turns * 1000 + (current_node.indices[0] - puzzle_input.end[0]) + (puzzle_input.end[1] - current_node.indices[1])

def solve(puzzle_input: PuzzleInput) -> None:
    ts = 0
    def reconstruct_path(came_from: dict[tuple[int, int], Node], current: Node) -> list[Node]:
        total_path: list[Node] = [current]
        turns = 0
        while current.indices in came_from:
            prev_node = came_from[current.indices]
            turns += calc_dir_turns(current.orientation, prev_node)
            current = came_from[current.indices]
            total_path.append(current)
        return list(reversed(total_path)), turns
    
    def calc_dir_turns(dir: str, curr: Node) -> int:
        if curr.orientation == dir:
            return 0
        elif curr.orientation in horiz_set:
            # if we have a horizontal start
            if dir in horiz_set:
                # if there's a horizontal end, we have to turn 2 times
                return 2
            else:
                # otherwise there's a vertical end, we have to turn 1 time
                return 1
        else:
            # we must have a vertical start
            if dir in vert_set:
                # if we have a vertical end this must require 2 turns
                return 2
            else:
                # otherwise there's a horizontal end, we have to turn 1 time
                return 1
    
    def calc_neighbor_score(dir: str, curr: Node) -> int:
        return 1 + (1000 * calc_dir_turns(dir, curr))

    open_queue = PriorityQueue(maxsize=(len(puzzle_input.grid)-2)*(len(puzzle_input.grid[0])-2))
    start_node = Node(orientation='R', indices=puzzle_input.start, timestamp=ts)
    open_queue.put((0, start_node))
    ts += 1
    open_set: set[tuple[int, int]] = set([puzzle_input.start])

    previous_nodes: dict[tuple[int, int], Node] = {}

    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: math.inf)
    g_score[puzzle_input.start] = 0

    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: math.inf)
    f_score[puzzle_input.start] = cost_heuristic(puzzle_input, start_node)

    orient_dict: dict[str, str] = {'U': '^', 'D': 'v', 'L': '<', 'R': '>'}

    ending_node: Node | None = None
    while not open_queue.empty():
        current: Node = open_queue.get()[1]
        old_char: str = puzzle_input.grid[current.indices[0]][current.indices[1]]
        puzzle_input.grid[current.indices[0]][current.indices[1]] = orient_dict[current.orientation]
        open_set.remove(current.indices)

        if current.indices == puzzle_input.end:
            ending_node = current
            puzzle_input.grid[current.indices[0]][current.indices[1]] = old_char
            break

        for dir, dir_idx in search_dirs.items():
            nbr_index = (current.indices[0] + dir_idx[0], current.indices[1] + dir_idx[1])
            if puzzle_input.grid[nbr_index[0]][nbr_index[1]] == "#":
                continue
            
            nbr_char: str = puzzle_input.grid[nbr_index[0]][nbr_index[1]]
            puzzle_input.grid[nbr_index[0]][nbr_index[1]] = '?'

            tentative_g_score = g_score[current.indices] + calc_neighbor_score(dir, current)
            if tentative_g_score < g_score[nbr_index]:
                nbr_node = Node(indices=nbr_index, orientation=dir, timestamp=ts)
                ts += 1
                previous_nodes[nbr_index] = current
                g_score[nbr_index] = tentative_g_score
                f_score[nbr_index] = tentative_g_score + cost_heuristic(puzzle_input, nbr_node)
                if nbr_index not in open_set:
                    open_queue.put((f_score[nbr_index], nbr_node))
                    open_set.add(nbr_index)
            
            puzzle_input.grid[nbr_index[0]][nbr_index[1]] = nbr_char
        puzzle_input.grid[current.indices[0]][current.indices[1]] = old_char

    solution_path, num_turns = reconstruct_path(previous_nodes, ending_node)
    for point in solution_path:
        puzzle_input.grid[point.indices[0]][point.indices[1]] = orient_dict[point.orientation]
    
    for line in puzzle_input.grid:
        print("".join(line))

    solution = (len(solution_path) - 1) + 1000 * num_turns
    print(f"Solution: {solution}")