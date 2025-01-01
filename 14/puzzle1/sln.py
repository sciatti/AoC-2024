from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass

class Robot(TypedDict):
    position: tuple[int, int]
    velocity: tuple[int, int]

@dataclass
class PuzzleData():
    grid: list[list[str]]
    robots: list[Robot]

# @dataclass
# class QuadrantDict():
#     x: dict[int, set[tuple[int, int]]]
#     y: dict[int, set[tuple[int, int]]]

class QuadrantDict(TypedDict):
    top_left: int
    top_right: int
    bottom_left: int
    bottom_right: int

def parse_input(file_handler) -> PuzzleData:
    puzzle_input: PuzzleData = PuzzleData(grid=[], robots=[])
    dimensions = [int(dim) for dim in file_handler.readline().rstrip().split(',')]
    for _height in range(dimensions[0]):
        puzzle_input.grid.append(['.'] * dimensions[1])
    
    for line in file_handler.readlines():
        values = line.rstrip().split(' ')
        position = values[0].split('=')[1].split(',')
        position = (int(position[0]), int(position[1]))
        velocity = values[1].split('=')[1].split(',')
        velocity = (int(velocity[0]), int(velocity[1]))
        puzzle_input.robots.append(Robot(position=position, velocity=velocity))

    return puzzle_input

def solve(puzzle_input: PuzzleData) -> None:
    num_seconds = 100

    height, width = len(puzzle_input.grid), len(puzzle_input.grid[0])
    mid_x, mid_y = (width // 2), (height // 2)
    quadrants: QuadrantDict = {'top_left': 0, 'bottom_left': 0, 'top_right': 0, 'bottom_right': 0}
    for robot in puzzle_input.robots:
        robot['position'] = (
            (robot['position'][0] + robot['velocity'][0] * num_seconds) % width,
            (robot['position'][1] + robot['velocity'][1] * num_seconds) % height
        )
        x, y = robot['position'][0], robot['position'][1]
        if x == mid_x or y == mid_y:
            continue
        # if we have reached this point, deduce and assign a quadrant
        index_str = "_right"
        # if the point lies on the left half of the grid...
        if x < mid_x:
            index_str = "_left"
        # if the point lies on the top half of the grid...
        if y < mid_y:
            index_str = "top" + index_str
        # otherwise the point lies on the bottom half of the grid...
        else:
            index_str = "bottom" + index_str
        quadrants[index_str] += 1
    
    pos_dict = {}
    for robot in puzzle_input.robots:
        if robot['position'] not in pos_dict:
            pos_dict[robot['position']] = [robot['position']]
        else:
            pos_dict[robot['position']].append(robot['position'])

    for pos, num_robots in pos_dict.items():
        x, y = pos[0], pos[1]
        puzzle_input.grid[y][x] = str(len(num_robots))
    
    for i in range(len(puzzle_input.grid)):
        puzzle_input.grid[i][mid_x] = ' '
        if i == mid_y:
            puzzle_input.grid[i] = ''

    for i in range(len(puzzle_input.grid)):
        print(''.join(puzzle_input.grid[i]))

    solution = 1
    for quad in quadrants:
        if quadrants[quad] > 0:
            solution *= quadrants[quad]
    print(f"Solution: {solution}")
    # answer of 219771468 is too low
    #           221616000 is the answer, was calculating the quadrants with an off by 1 error