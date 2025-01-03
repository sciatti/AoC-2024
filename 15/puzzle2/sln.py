from __future__ import annotations
from dataclasses import dataclass
from collections import deque, OrderedDict

@dataclass
class PuzzleInput():
    map: list[list[str]]
    moves: list[str]
    robot: tuple[int, int]

Dirs: dict[str, tuple[int, int]] = { '^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1) }

def parse_input(file_handler) -> PuzzleInput:
    puzzle_input: PuzzleInput = PuzzleInput(map=[], moves=[], robot=(0,0))
    parsing_map = True
    for line in file_handler.readlines():
        if line == "\n":
            parsing_map = False
        if parsing_map:
            puzzle_input.map.append(list(line.rstrip()))
            if '@' in puzzle_input.map[-1]:
                puzzle_input.robot = (len(puzzle_input.map) - 1, 2* puzzle_input.map[-1].index('@'))
        else:
            puzzle_input.moves += list(line.rstrip())
    new_map = []
    for i in range(len(puzzle_input.map)):
        new_map.append([])
        for j in range(len(puzzle_input.map[i])):
            char = puzzle_input.map[i][j]
            if char == "O":
                new_map[-1].append("[")
                new_map[-1].append("]")
            elif char == "@":
                new_map[-1].append("@")
                new_map[-1].append(".")
            else:
                new_map[-1].append(char)
                new_map[-1].append(char)
    puzzle_input.map = new_map

    return puzzle_input

def check_horiz_box_push(map: list[list[str]], coords: tuple[int, int], dir: str) -> tuple[int, int] | None:
    end_coords: tuple[int, int] = (coords[0] + (Dirs[dir][0] * (len(map) - 1)), (coords[1] + Dirs[dir][1] * (len(map[0]) - 1)))
    end_coords = (max(min(end_coords[0], len(map) - 1), 0), max(min(end_coords[1], len(map[0]) - 1), 0))
    num_iterations = abs(end_coords[0] - coords[0]) + abs(end_coords[1] - coords[1])
    # iterate until the wall is found
    for i in range(1, num_iterations + 1):
        curr_pos = ((Dirs[dir][0] * i) + coords[0], (Dirs[dir][1] * i) + coords[1])
        # if there's a space before the wall, return true and the coordinates of this space
        if map[curr_pos[0]][curr_pos[1]] == '.':
            return curr_pos
        # if there's a wall before the end of the map (map is surrounded by walls) return None
        if map[curr_pos[0]][curr_pos[1]] == '#':
            return None
    # at this point return None: the wall was found and this box can't be moved
    return None

def check_vert_box_push(map: list[list[str]], coords: tuple[int, int], dir: str) -> OrderedDict[tuple[int, int], int] | None:
    box_char = map[coords[0]][coords[1]]
    other_side = (coords[0], coords[1]+1) if box_char == "[" else (coords[0], coords[1]-1)

    c = 1 
    # create a set of each box's left side coordinates
    connected_boxes = OrderedDict([(coords, 0) if box_char == "[" else (other_side, 0)])
    # create a deque of each individual side of a box, need to search the top or bottom of the 
    # coordinate of each side of the box and check to see if we hit a box, what side of it do we hit
    search_queue = deque([coords, other_side] if box_char == "[" else [other_side, coords])
    while len(search_queue) > 0:
        curr_side = search_queue.popleft()
        curr_char = map[curr_side[0]][curr_side[1]]
        # get the new row index (either up or down)
        search_idx = (curr_side[0] + Dirs[dir][0], curr_side[1])
        search_char = map[search_idx[0]][search_idx[1]]
        # check the search char
        if search_char == "#":
            # if the search finds a wall the boxes can't move in their connected set
            return None
        elif search_char == "[" or search_char == "]":
            test_index, next_index = None, None
            # found a connecting box half
            if search_char == curr_char:
                # if the search char has the same side orientation as the starting char
                if search_char == "[":
                    # if the search char is a left side bracket, collect the bracket on its right
                    test_index, next_index = search_idx, (search_idx[0], search_idx[1] + 1)
                else:
                    # if the search char is a right side bracket, collect the closing bracket on its left
                    test_index, next_index = (search_idx[0], search_idx[1] - 1), search_idx
            else:
                # the search char has the opposite side orientation as the starting char
                # this means the search is branching left or right, because a misalignment is only caused this way
                if search_char == "]":
                    # if the search character is a right side bracket, the rest of the box resides to its left
                    test_index, next_index = (search_idx[0], search_idx[1] - 1), search_idx
                else:
                    # otherwise the search character is a left side bracket and the rest of the box resides to its right
                    test_index, next_index = search_idx, (search_idx[0], search_idx[1] + 1)
            
            if test_index and next_index and test_index not in connected_boxes:
                connected_boxes[test_index] = c
                c += 1
                search_queue.append(test_index)
                search_queue.append(next_index)
    return connected_boxes

def solve(puzzle_input: PuzzleInput) -> None:
    print_map = False
    HEIGHT: int= len(puzzle_input.map)
    WIDTH: int = len(puzzle_input.map[0])

    BOX_CHARS = { "[", "]" }
    HORIZONTAL = { "<", ">" }

    print("Initial state:")
    for line in puzzle_input.map:
        print("".join(line))
    print()

    # iterate through every move in the list of moves, evaluate each move
    for move in puzzle_input.moves:
        old_robot_pos = puzzle_input.robot
        # get the next position's coordinates
        coords = (puzzle_input.robot[0] + Dirs[move][0], puzzle_input.robot[1] + Dirs[move][1])
        next_space = puzzle_input.map[coords[0]][coords[1]]
        # check if the robot is moving into a box
        if next_space in BOX_CHARS:
            # check to see if the pushing is horizontal (can treat it the same as puzzle 1)
            if move in HORIZONTAL:
                # check if the move is possible or if this box (or subsequent boxes are touching a wall)
                push_spot = check_horiz_box_push(puzzle_input.map, coords, move)
                if push_spot:
                        num_iterations = abs(push_spot[0] - coords[0]) + abs(push_spot[1] - coords[1])
                        # create new horizontal list that gets swapped into the map
                        new_row: list[str] = [elt for elt in puzzle_input.map[coords[0]]]
                        # iterate over the number of iterations and complete the swap in the new_row list
                        for i in range(num_iterations):
                            old_row_pos = (coords[0] + Dirs[move][0] * i, coords[1] + Dirs[move][1] * i)
                            new_row_pos = old_row_pos[1] + Dirs[move][1]
                            new_row[new_row_pos] = puzzle_input.map[old_row_pos[0]][old_row_pos[1]]
                        # assign new_row to the old row in the map
                        puzzle_input.map[coords[0]] = new_row
                        # move the robot over
                        puzzle_input.robot = coords
            # otherwise this input is pushing upwards and collision detection needs to happen...
            else:
                pushed_boxes = check_vert_box_push(puzzle_input.map, coords, move)
                if pushed_boxes is not None:
                    for left_side in reversed(pushed_boxes.keys()):
                        v_dir = Dirs[move][0]
                        # starting from the end of the set of connected boxes
                        # move each side of the box into its new space, then clean up its old space
                        puzzle_input.map[left_side[0] + v_dir][left_side[1]] = puzzle_input.map[left_side[0]][left_side[1]]
                        puzzle_input.map[left_side[0]][left_side[1]] = '.'

                        puzzle_input.map[left_side[0] + v_dir][left_side[1] + 1] = puzzle_input.map[left_side[0]][left_side[1] + 1]
                        puzzle_input.map[left_side[0]][left_side[1] + 1] = '.'
                    puzzle_input.robot = coords
        # check if the robot is moving in free space
        elif next_space == '.':
            # move the robot over to the new space
            puzzle_input.robot = coords
        # else the robot is moving into a wall, do nothing to update the robot's position
        
        # set the robot's old position to an empty space
        puzzle_input.map[old_robot_pos[0]][old_robot_pos[1]] = '.'
        # set the robot's new position to the robot character
        puzzle_input.map[puzzle_input.robot[0]][puzzle_input.robot[1]] = '@'

        if print_map:
            print(f"Move: {move}")
            for line in puzzle_input.map:
                print("".join(line))
            print()

    for line in puzzle_input.map:
        print("".join(line))
    print()

    solution = 0
    for i in range(len(puzzle_input.map)):
        for j in range(len(puzzle_input.map[i])):
            if puzzle_input.map[i][j] == '[':
                solution += (i * 100) + j
    print(f"Solution: {solution}")