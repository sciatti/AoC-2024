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
    num_seconds = 10000

    height, width = len(puzzle_input.grid), len(puzzle_input.grid[0])

    def reset_grid():
        puzzle_input.grid = []
        for _ in range(height):
            puzzle_input.grid.append(['.']*width)

    pattern_times = []
    for second in range(num_seconds):
        # reset the grid each iteration
        # reset_grid()
        robot_positions: list[tuple[int, int]] = []
        set_positions: set[tuple[int, int]] = set()
        for robot in puzzle_input.robots:
            x, y = (
                (robot['position'][0] + robot['velocity'][0] * second) % width,
                (robot['position'][1] + robot['velocity'][1] * second) % height
            )
            robot_positions.append((x,y))
            set_positions.add((x, y))
            # puzzle_input.grid[y][x] = '*'
        
        for rob in robot_positions:
            # check if this robot position can be the start of a tree
            if rob[0] > width - 1 - 5 or rob[0] < 5 or rob[1] > height - 1 - 5:
                continue
            found_pattern = True
            # check to see if there's a pattern with len == 5
            for k in range(1, 6):
                down_left = (rob[0] - k, rob[1] + k)
                down_right = (rob[0] + k, rob[1] + k)
                # remember to swap x and y as the y value is first
                if down_left not in set_positions or down_right not in set_positions:
                # if puzzle_input.grid[down_left[1]][down_left[0]] != "*" or puzzle_input.grid[down_right[1]][down_right[0]] != "*":
                    found_pattern = False
                    break
            if found_pattern:
                print(f"found pattern at: {second}")
                pattern_times.append(second)
                break
        if len(pattern_times) > 0:
            break
        if second % 10000 == 0:
            print(second)

    for pattern_time in [pattern_times[0]]:
        reset_grid()

        for robot in puzzle_input.robots:
            robot['position'] = (
                (robot['position'][0] + robot['velocity'][0] * pattern_time) % width,
                (robot['position'][1] + robot['velocity'][1] * pattern_time) % height
            )

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
            print(''.join(puzzle_input.grid[i]))

    solution = pattern_times[0]
    print(f"Solution: {solution} seconds")