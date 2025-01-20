from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass
from collections import defaultdict, deque
from queue import PriorityQueue
import math

search_dirs: dict[str, tuple[int, int]] = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

horiz_set = set(['L', 'R'])
vert_set = set(['U', 'D'])

PATH_DEBUG = False
COST_DEBUG = False
SEARCH_DEBUG = False

@dataclass
class Node():
    orientation: str # U/D/L/R for up/down/left/right
    indices: tuple[int, int]
    timestamp: int
    parent: Node | None

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

def solve(puzzle_input: PuzzleInput, PRINT_SOL: bool = True) -> None:
    ts = 0

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
    start_node = Node(orientation='R', indices=puzzle_input.start, timestamp=ts, parent=None)
    open_queue.put((0, (start_node, 0)))
    ts += 1
    open_set: set[tuple[int, int]] = set([(puzzle_input.start, 'R')])

    previous_nodes: dict[tuple[int, int], Node] = {}

    g_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: math.inf)
    g_score[puzzle_input.start] = 0

    f_score: defaultdict[tuple[int, int], int] = defaultdict(lambda: math.inf)
    f_score[puzzle_input.start] = cost_heuristic(puzzle_input, start_node)

    orient_dict: dict[str, str] = {'U': '^', 'D': 'v', 'L': '<', 'R': '>'}

    while not open_queue.empty():
        temp: tuple[Node, int] = open_queue.get()[1]
        current: Node = temp[0]
        parent_g_score: int = temp[1]

        if SEARCH_DEBUG:
            old_char: str = puzzle_input.grid[current.indices[0]][current.indices[1]]
            puzzle_input.grid[current.indices[0]][current.indices[1]] = orient_dict[current.orientation]
        if current.parent:
            open_set.remove((current.indices, current.parent.orientation))
        else:
            # check for first item
            open_set.remove((current.indices, 'R'))

        for dir, dir_idx in search_dirs.items():
            nbr_index = (current.indices[0] + dir_idx[0], current.indices[1] + dir_idx[1])
            if puzzle_input.grid[nbr_index[0]][nbr_index[1]] == "#":
                continue

            if SEARCH_DEBUG:
                nbr_char: str = puzzle_input.grid[nbr_index[0]][nbr_index[1]]
                puzzle_input.grid[nbr_index[0]][nbr_index[1]] = '?'

            tentative_g_score = parent_g_score + calc_neighbor_score(dir, current)
            if tentative_g_score < g_score[nbr_index]:
                nbr_node = Node(indices=nbr_index, orientation=dir, timestamp=ts, parent=current)
                ts += 1
                previous_nodes[nbr_index] = current
                
                g_score[nbr_index] = tentative_g_score
                
                f_score[nbr_index] = tentative_g_score + cost_heuristic(puzzle_input, nbr_node)
                
                if (nbr_index, current.orientation) not in open_set:
                    open_queue.put((f_score[nbr_index], (nbr_node, g_score[nbr_index])))
                    open_set.add((nbr_index, current.orientation))
            
            if SEARCH_DEBUG:
                puzzle_input.grid[nbr_index[0]][nbr_index[1]] = nbr_char
        if SEARCH_DEBUG:
            puzzle_input.grid[current.indices[0]][current.indices[1]] = old_char
    
    cost_grid = [list(line) for line in puzzle_input.grid]
    for point in g_score:
        cost_grid[point[0]][point[1]] = str(g_score[point])

    path_points: set[tuple[int, int]] = set([puzzle_input.end])
    search_queue: deque[tuple[int, int]] = deque()
    # start search from end of grid
    search_queue.append(puzzle_input.end)
    while len(search_queue) > 0:
        current = search_queue.pop()

        # iterate through every neighbor
        for nbr_dir in search_dirs.values():
            nbr: tuple[int, int] = (nbr_dir[0] + current[0], nbr_dir[1] + current[1])
            # if we find a wall, skip
            if cost_grid[nbr[0]][nbr[1]] == '#':
                continue
            nbr_score = int(cost_grid[nbr[0]][nbr[1]])
            current_score = int(cost_grid[current[0]][current[1]])
            # need to look 1 space behind for an edge case
            parent_char = cost_grid[(nbr_dir[0] * -1) + current[0]][(nbr_dir[1] * -1) + current[1]]
            # need to look 2 spaces ahead for an edge case
            nbr_child_char = cost_grid[nbr_dir[0] + nbr[0]][nbr_dir[1] + nbr[1]]
            parent_score, nbr_child_score = None, None
            if parent_char != '#':
                parent_score = int(cost_grid[(nbr_dir[0] * -1) + current[0]][(nbr_dir[1] * -1) + current[1]])
            if nbr_child_char != '#':
                nbr_child_score = int(cost_grid[nbr_dir[0] + nbr[0]][nbr_dir[1] + nbr[1]])

            # if we find a neighbor that's got a value == curr value - 1 then that's on the path in a straight line
            if nbr_score == current_score - 1:
                search_queue.append(nbr)
                path_points.add(nbr)
                puzzle_input.grid[nbr[0]][nbr[1]] = 'O'
            # if we find a neighbor that's got a value of curr value - 1000 - 1 then that's a turn on the path
            elif nbr_score == current_score - 1000 - 1:
                search_queue.append(nbr)
                path_points.add(nbr)
                puzzle_input.grid[nbr[0]][nbr[1]] = 'O'
            # standard branching case where the node preceding the current node aligns with the nbr node
            elif parent_score and nbr_score == current_score + 1000 - 1 and parent_score == nbr_score + 2:
                # if a neighbor has a value > the current value by 999 and the current node's parent 
                #   is in line with this node and its total == neighbor + 2 then you've hit a new branching path
                #   This comment outlines it well https://www.reddit.com/r/adventofcode/comments/1hfboft/comment/m4db7eh
                #   This edge case is shown in [7,4] to [7,6] in vo.txt where the value goes from 4009 -> 3010 -> 4011
                search_queue.append(nbr)
                path_points.add(nbr)
                puzzle_input.grid[nbr[0]][nbr[1]] = 'O'
            # rare branching case where the nbr node doesn't align but the one after the nbr node does
            elif nbr_child_score and nbr_score < current_score and nbr_child_score == current_score - 2:
                # don't add the nbr to the search queue, but add it to the valid path
                path_points.add(nbr)
                nbr_child = (nbr_dir[0] + nbr[0], nbr_dir[1] + nbr[1])
                # add the nbr's child to the search queue and continue
                search_queue.append(nbr_child)
                path_points.add(nbr_child)
                puzzle_input.grid[nbr[0]][nbr[1]] = 'O'
                puzzle_input.grid[nbr_child[0]][nbr_child[1]] = 'O'
            # curr_grid_section[nbr[0] - gtp[0]][nbr[1] - gtp[1]] = old_char

    if COST_DEBUG:
        for line in cost_grid:
            for char in line:
                if char == "#":
                    char = "###### "
                    #char = "       "
                elif char == ".":
                    char = "...... "
                print_str = "      "
                print(char + print_str[len(char)-1:], end="")
            print()

    if PATH_DEBUG:
        for line in puzzle_input.grid:
            print("".join(line))

    solution = len(path_points)
    if PRINT_SOL:
        print(f"Solution: {solution}")
    # answer of 589 is too low
    # answer of 590 is too low
    # answer of 650 is too low
    # the answer is 1024