char_grid = []
with open("input.txt", "r", encoding="utf-8") as input_file:
    for line in input_file.readlines():
        char_grid.append([])
        for char in line:
            char_grid[-1].append(char)

def search_pattern(start_idx, grid):
    match_count = 0
    match_list = ['X', 'M', 'A', 'S']

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

    left_bounds = lambda i, j : (i, j - 3)
    right_bounds = lambda i, j : (i, j + 3)
    up_bounds = lambda i, j : (i - 3, j)
    down_bounds = lambda i, j : (i + 3, j)
    up_left_bounds = lambda i, j : (i - 3, j - 3)
    up_right_bounds = lambda i, j : (i - 3, j + 3)
    down_left_bounds = lambda i, j : (i + 3, j - 3)
    down_right_bounds = lambda i, j : (i + 3, j + 3)

    pattern_funcs = [
            search_left,
            search_right,
            search_up,
            search_down,
            search_up_left,
            search_up_right,
            search_down_left,
            search_down_right
    ]

    bounds_funcs = [
            left_bounds,
            right_bounds,
            up_bounds,
            down_bounds,
            up_left_bounds,
            up_right_bounds,
            down_left_bounds,
            down_right_bounds
    ]

    match_indices = []
    for func_idx, search_func in enumerate(pattern_funcs):
        bounds_func = bounds_funcs[func_idx]
        matches = True
        # if start_idx[0] == 9 and start_idx[1] == 3:
        #     breakpoint()
        bounds = bounds_func(start_idx[0], start_idx[1])
        trace = []
        if (bounds[0] > -1 and bounds[0] < len(grid)) and (bounds[1] > -1 and bounds[1] < len(grid[0])): 
            for i in range(4):
                search_result = search_func(start_idx, char_grid, i)
                if not search_result[0]:
                    matches = False
                    break
                else:
                    #breakpoint()
                    trace.append(search_result[1])
        match_count += matches
        if matches and len(trace) == 4:
            #breakpoint()
            match_indices.append(trace)

    return match_count, match_indices

xmas_patterns = 0
# print_data = set()
print_data = []
for i, row in enumerate(char_grid):
    for j, char in enumerate(row):
        if char == 'X':
            temp, xmas_indices = search_pattern((i, j), char_grid)
            #breakpoint()
            xmas_patterns += temp
            for indices_list in xmas_indices:
                #print_data.add(indices_list)
                print_data.append(indices_list)

print(f"Number of XMAS patterns found: {xmas_patterns}")
# current output of 3485 is too high
# other output of 2350 from the print statement below is too low
# other output of 2420 is not right either?
# currently getting 2350 again, but this doesn't pass the test case
# fixed the bounds function, it needed to be +/- 3 instead of +/- 4, now getting 2401 for output

print(len(print_data))

def sign(x):
    if x == 0:
        return 0
    if x < 0:
        return -1
    if x > 0:
        return 1
    #return 0 if abs(x) == 0 else x // abs(x)

print_grid = []
for row in char_grid:
    print_grid.append(['.']*len(char_grid[0]))

# print(len(char_grid), len(char_grid[0]))
# print(len(print_grid), len(print_grid[0]))


xmas_list = ['X', 'M', 'A', 'S']
for index_list in print_data:
    for i in range(4):
        try:
            print_grid[index_list[i][0]][index_list[i][1]] = xmas_list[i]
        except Exception as EX:
            print("error ", EX)
            #exit()
            #print(index_list)
            #print(index_list[i][0],index_list[i][1])
    #start, stop = index_pair[0], index_pair[1]
    #idir, jdir = sign(stop[0] - start[0]), sign(stop[1] - start[1])
    #for i, char in enumerate(xmas_list):
        #try:
            #print_grid[i * idir + start[0]][j * jdir + start[1]] = char
        #except Exception as ex:
            #print(start, stop)
            #print(f'bad index data:\n\ti: {i}, idir: {idir}, start: {start[0]}\n\tj: {j}, jdir: {jdir}, start: {start[1]}')

# this print lineup isn't even matching up with the actual input
for lin in print_grid:
    print(''.join(lin))
