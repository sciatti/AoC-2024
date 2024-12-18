from dataclasses import dataclass
from typing import Tuple

@dataclass
class PathNode:
    idx: Tuple[int, int]
    dir: int

@dataclass
class WallNode:
    i: int
    j: int
    up: object
    right: object
    down: object
    left: object

def parse_input(file_handler):
    input = []
    for line in file_handler.readlines():
        input.append(list(line.rstrip()))
    return input

dir_list = [
    (-1, 0),    # up
    (0, 1),     # right
    (1, 0),     # down
    (0, -1)     # left
]

dir_char = [
    '^',
    '>',
    'v',
    '<'
]

def check_bounds(grid, indices):
    if indices[0] < 0 or indices[0] > len(grid) - 1:
        return False
    if indices[1] < 0 or indices[1] > len(grid[0]) - 1:
        return False
    return True

def calculate_escape_grid(input_grid):# -> list[list[list[bool, bool, bool, bool]]]:
    escape_grid = []
    for row in input_grid:
        escape_grid.append([])
        for _cell in row:
            escape_grid[-1].append(['Y', 'Y', 'Y', 'Y'])

    # iterate through each direciton and determine if a point can exit given a specific direction
    for dir_idx, dir in enumerate(dir_list):
        search_vert = True
        # searching the up direction, start at the top and move down
        range_args = { 'i': (0, len(input_grid), 1), 'j': (0, len(input_grid[0]), 1) }
        if dir == dir_list[1]:
            # searching the right direction, start on the right and move left
            range_args = { 'i': (0, len(input_grid), 1), 'j': (len(input_grid[0]) - 1, -1, -1) }
            search_vert = False
        elif dir == dir_list[2]:
            # searching the down direction, start on the bottom and move up
            range_args = { 'i': (len(input_grid) - 1, -1, -1), 'j': (0, len(input_grid[0]), 1) }
        elif dir == dir_list[3]:
            # searching the left direction, start on the left and move right
            range_args = { 'i': (len(input_grid) - 1, -1, -1), 'j': (0, len(input_grid[0]), 1) }
            search_vert = False
        
        for idx_1 in range(*range_args['j' if search_vert else 'i']):
            has_wall = False
            for idx_2 in range(*range_args['i' if search_vert else 'j']):
                i, j = (idx_2, idx_1) if search_vert else (idx_1, idx_2)
                curr_space = input_grid[i][j]
                # if current space is a wall
                if curr_space == '#':
                    # mark escape_grid as False as this is a wall
                    escape_grid[i][j][dir_idx] = 'N'
                    # we have encountered a wall, so all other paths can not lead out on the row/col
                    has_wall = True
                # otherwise this is a normal space 
                else:
                    # if we are on a normal space and have seen a wall in this row/col...
                    if has_wall:
                        escape_grid[i][j][dir_idx] = 'N'
                    # since spaces are automatically counted as True nothing to do
    return escape_grid

def calculate_walls_dict(input_grid):
    walls = {'row': {}, 'col': {}, 'walls': set()}
    for i in range(len(input_grid)):
        walls['row'][i] = []
        for j in range(len(input_grid[i])):
            if input_grid[i][j] == "#":
                walls['row'][i].append(j)
                walls['walls'].add((i,j))
    for j in range(len(input_grid[0])):
        walls['col'][j] = []
        for i in range(len(input_grid)):
            if input_grid[i][j] == '#':
                walls['col'][j].append(i)
    return walls

# def create_walls_graph(walls_dict):
#     for wall in walls_dict['walls']:
#         i, j = wall[0], wall[1]
#         # search left
#         if (i > 0 and j > 0):
#             # start at i-1 and j-1 from the current node, iterate left until you find a node
#             for search_col
#         # search right:
#         if (i < len(input_grid) - 1):

#         # search up

def solve(input):
    char_map = input

    guard_path: list[PathNode] = []
    guard_indices = set()

    start = (None, None)
    # get starting point
    for i, line in enumerate(char_map):
        if '^' in line and line.index('^') != -1:
            start = (i, line.index('^'))
            break


    def calc_next_idx(curr_idx: Tuple[int, int], dir_idx: int, char_map: list[list[str]]):
        # look ahead to the next space, if it's a '#' you need to turn
        next_idx = (curr_idx[0] + dir_list[dir_idx][0], curr_idx[1] + dir_list[dir_idx][1])
        if check_bounds(char_map, next_idx):
            # check if we are infront of a wall, make turn if that is true
            if char_map[next_idx[0]][next_idx[1]] == '#':
                dir_idx = (dir_idx + 1) % len(dir_list)
                next_idx = (curr_idx[0] + dir_list[dir_idx][0], curr_idx[1] + dir_list[dir_idx][1])
        return next_idx, dir_idx
    # escape_map = calculate_escape_grid(char_map)
    # walls_dict = calculate_walls_dict(char_map)

    guard_exited = False
    guard_indices.add(start)
    curr_idx, dir_idx = start, 0
    guard_path.append(PathNode(idx=curr_idx, dir=dir_idx))
    while not guard_exited:
        # increment the current index
        curr_idx = (curr_idx[0] + dir_list[dir_idx][0], curr_idx[1] + dir_list[dir_idx][1])
        # check if the current index is out of bounds (guard has exited)
        if not check_bounds(char_map, curr_idx):
            guard_exited = True
        else:
            # add current position to the path and indices datastructs
            guard_path.append(PathNode(idx=curr_idx, dir=dir_idx))
            guard_indices.add(curr_idx)

            _, dir_idx = calc_next_idx(curr_idx, dir_idx, char_map)

    loop_locations = set()
    # brute force attempt
    for i in range(len(guard_path) - 1):
        start_idx, start_dir = guard_path[i].idx, guard_path[i].dir
        temp_wall_idx = guard_path[i+1].idx
        #char_map[start_idx[0]][start_idx[1]] = dir_char[start_dir]
        # check if the temp_wall_index was found to have worked
        if temp_wall_idx not in loop_locations:
            # put a wall at the next pathnode index
            char_map[temp_wall_idx[0]][temp_wall_idx[1]] = '#'
            curr_path = set()
            looped, exited = False, False
            curr_idx, curr_dir = start_idx, start_dir
            while not looped and not exited:
                if not check_bounds(char_map, curr_idx):
                    exited = True
                    break
                #char_map[curr_idx[0]][curr_idx[1]] = dir_char[curr_dir]
                curr_hash = (curr_idx[0], curr_idx[1], curr_dir)
                # if the current idx and dir have been spotted, we have looped
                if curr_hash in curr_path:
                    looped = True
                # else if we have not looped, iterate to the next position
                else:
                    # add the current position + dir to the set
                    curr_path.add(curr_hash)
                    # calculate next position + dir, assign it to current
                    #char_map[curr_idx[0]][curr_idx[1]] = '.'
                    # this involves first peeking ahead to the next spot and checking if it's a wall
                    curr_idx, curr_dir = calc_next_idx(curr_idx, curr_dir, char_map)
            if looped and not exited:
                loop_locations.add(temp_wall_idx)
            # remove the temp wall at the next pathnode index
            char_map[temp_wall_idx[0]][temp_wall_idx[1]] = '.'
        #print(f"completed check of node: {i}")
        #char_map[start_idx[0]][start_idx[1]] = '.'

    solution = len(loop_locations)
    for wall in loop_locations:
        char_map[wall[0]][wall[1]] = '0'
    print(f"Solution: {solution}")
    # current solution of 1580 is too high

    for row in char_map:
        print(''.join(row))