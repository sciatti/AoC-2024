def parse_input(file_handler):
    input = []
    for line in file_handler.readlines():
        input.append(list(line.rstrip()))
    return input

def check_bounds(grid, indices):
    if indices[0] < 0 or indices[0] > len(grid) - 1:
        return False
    if indices[1] < 0 or indices[1] > len(grid[0]) - 1:
        return False
    return True

def solve(input):
    char_map = input

    guard_path = []
    guard_indices = set()

    start = (None, None)
    # get starting point
    for i, line in enumerate(char_map):
        if '^' in line and line.index('^') != -1:
            start = (i, line.index('^'))
            break
    
    guard_exited = False
    guard_indices.add(start)
    guard_path.append(start)
    curr_idx, dir_idx = start, 0   
    dir_list = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    while not guard_exited:
        # increment the current index
        curr_idx = (curr_idx[0] + dir_list[dir_idx][0], curr_idx[1] + dir_list[dir_idx][1])
        # check if the current index is out of bounds (guard has exited)
        if not check_bounds(char_map, curr_idx):
            guard_exited = True
        else:
            # add current position to the path and indices datastructs
            guard_path.append(curr_idx)
            guard_indices.add(curr_idx)

            # look ahead to the next space, if it's a '#' you need to turn
            next_idx = (curr_idx[0] + dir_list[dir_idx][0], curr_idx[1] + dir_list[dir_idx][1])
            if check_bounds(char_map, next_idx):
                # check if we are infront of a wall, make turn if that is true
                if char_map[next_idx[0]][next_idx[1]] == '#':
                    dir_idx = (dir_idx + 1) % len(dir_list)

    solution = len(guard_indices)
    print(f"Solution: {solution}")