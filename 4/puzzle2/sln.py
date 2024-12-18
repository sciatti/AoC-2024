char_grid = []
with open("input.txt", "r", encoding="utf-8") as input_file:
    for line in input_file.readlines():
        char_grid.append([])
        for char in line:
            char_grid[-1].append(char)

def search_pattern(start_idx, grid):
    match_list = ['M', 'A', 'S']

    def search_left(idx, grid, i):
        return (match_list[i] == grid[idx[0]][idx[1] - i], (idx[0], idx[1] - i))
    def search_right(idx, grid, i):
        return (match_list[i] == grid[idx[0]][idx[1] + i], (idx[0], idx[1] + i))
    def search_up(idx, grid, i):
        return (match_list[i] == grid[idx[0] - i][idx[1]], (idx[0] - i, idx[1]))
    def search_down(idx, grid, i):
        return (match_list[i] == grid[idx[0] + i][idx[1]], (idx[0] + i, idx[1]))
    def search_up_left(idx, grid, i):
        return (match_list[i] == grid[idx[0] - i][idx[1] - i], (idx[0] - i, idx[1] - i))
    def search_up_right(idx, grid, i):
        return (match_list[i] == grid[idx[0] - i][idx[1] + i], (idx[0] - i, idx[1] + i))
    def search_down_left(idx, grid, i):
        return (match_list[i] == grid[idx[0] + i][idx[1] - i], (idx[0] + i, idx[1] - i))
    def search_down_right(idx, grid, i):
        return (match_list[i] == grid[idx[0] + i][idx[1] + i], (idx[0] + i, idx[1] + i))

    bounds_size = len(match_list) -1
    left_bounds = lambda i, j : (i, j - bounds_size)
    right_bounds = lambda i, j : (i, j + bounds_size)
    up_bounds = lambda i, j : (i - bounds_size, j)
    down_bounds = lambda i, j : (i + bounds_size, j)
    up_left_bounds = lambda i, j : (i - bounds_size, j - bounds_size)
    up_right_bounds = lambda i, j : (i - bounds_size, j + bounds_size)
    down_left_bounds = lambda i, j : (i + bounds_size, j - bounds_size)
    down_right_bounds = lambda i, j : (i + bounds_size, j + bounds_size)

    pattern_funcs = [
            # search_left,
            # search_right,
            # search_up,
            # search_down,
            search_up_left,
            search_up_right,
            search_down_left,
            search_down_right
    ]

    bounds_funcs = [
            # left_bounds,
            # right_bounds,
            # up_bounds,
            # down_bounds,
            up_left_bounds,
            up_right_bounds,
            down_left_bounds,
            down_right_bounds
    ]

    match_indices = []
    for func_idx, search_func in enumerate(pattern_funcs):
        bounds_func = bounds_funcs[func_idx]
        matches = True
        bounds = bounds_func(start_idx[0], start_idx[1])
        trace = []
        if (bounds[0] > -1 and bounds[0] < len(grid)) and (bounds[1] > -1 and bounds[1] < len(grid[0])): 
            for i in range(len(match_list)):
                search_result = search_func(start_idx, char_grid, i)
                if not search_result[0]:
                    matches = False
                    break
                else:
                    trace.append(search_result[1])
        if matches and len(trace) == len(match_list):
            match_indices.append(trace)

    return match_indices

match_data = []
for i, row in enumerate(char_grid):
    for j, char in enumerate(row):
        if char == 'M':
            match_data += search_pattern((i, j), char_grid)

print(f"Number of MAS patterns found: {len(match_data)}")
# PUZZLE1 Comments:
#   current output of 3485 is too high
#   other output of 2350 from the print statement below is too low
#   other output of 2420 is not right either?
#   currently getting 2350 again, but this doesn't pass the test case
#   fixed the bounds function, it needed to be +/- 3 instead of +/- 4, now getting 2401 for output

# PUZZLE2 Comments:
#   I have all the MAS's that appear in the file, now I need to put them into a dict
#   Dict will allow quick lookups of middle 'A' point of diagonal MAS strings
#   The dict needs to hash the middle index pair of every diagonal MAS string found
#   I will map the middle 'A' index pair to a list of diagonal MAS strings
#   After that I can iterate through the dict and include all hashed index pairs that have 2 elements

midpoint_dict = {}
for index_list in match_data:
    midpoint_index = index_list[(len(index_list)//2)]
    if midpoint_index not in midpoint_dict:
        midpoint_dict[midpoint_index] = [index_list]
    else:
        midpoint_dict[midpoint_index].append(index_list)

count = 0
print_data = []
for _midpoint, indices_list in midpoint_dict.items():
    if len(indices_list) == 2:
        print_data += indices_list
        count += 1

print(f"Number of X-MAS cross-patterns found: {count}")

print_grid = []
for row in char_grid:
    print_grid.append(['.']*len(char_grid[0]))

char_list = ['M', 'A', 'S']
for index_list in print_data:
    for i in range(len(char_list)):
        print_grid[index_list[i][0]][index_list[i][1]] = char_list[i]

for lin in print_grid:
    print(''.join(lin))
