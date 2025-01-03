from __future__ import annotations
from dataclasses import dataclass

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
                puzzle_input.robot = (len(puzzle_input.map) - 1, puzzle_input.map[-1].index('@'))
        else:
            puzzle_input.moves += list(line.rstrip())
    return puzzle_input

def check_box_push(map: list[list[str]], coords: tuple[int, int], dir: str) -> tuple[int, int] | None:
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

def solve(puzzle_input: PuzzleInput) -> None:
    print_map = False
    HEIGHT: int= len(puzzle_input.map)
    WIDTH: int = len(puzzle_input.map[0])

    # iterate through every move in the list of moves, evaluate each move
    for move in puzzle_input.moves:
        old_pos = puzzle_input.robot
        # get the next position's coordinates
        coords = (puzzle_input.robot[0] + Dirs[move][0], puzzle_input.robot[1] + Dirs[move][1])
        next_space = puzzle_input.map[coords[0]][coords[1]]
        # check if the robot is moving into a box
        if next_space == 'O':
            # check if the move is possible or if this box (or subsequent boxes are touching a wall)
            push_spot = check_box_push(puzzle_input.map, coords, move)
            if push_spot:
                # add a box to the end
                puzzle_input.map[push_spot[0]][push_spot[1]] = 'O'
                # move the robot over
                puzzle_input.robot = coords
                        
        # check if the robot is moving in free space
        elif next_space == '.':
            # move the robot over to the new space
            puzzle_input.robot = coords
        # else the robot is moving into a wall, do nothing to update the robot's position
        
        # set the robot's old position to an empty space
        puzzle_input.map[old_pos[0]][old_pos[1]] = '.'
        # set the robot's new position to the robot character
        puzzle_input.map[puzzle_input.robot[0]][puzzle_input.robot[1]] = '@'

        if print_map:
            print(f"Move: {move}")
            for line in puzzle_input.map:
                print("".join(line))
            print()

    # for line in puzzle_input.map:
    #     print("".join(line))
    # print()

    solution = 0
    for i in range(len(puzzle_input.map)):
        for j in range(len(puzzle_input.map[i])):
            if puzzle_input.map[i][j] == 'O':
                solution += (i * 100) + j
    print(f"Solution: {solution}")