from typing import TypedDict

class FileData(TypedDict):
    fileblocks: list[int]
    spaces: list[int]
    line: list[str]

def parse_input(file_handler):
    input: FileData = { 'fileblocks': [], 'spaces': [], 'line': [] }
    id_count = 0
    line = file_handler.readline().rstrip()
    for i in range(len(list(line))):
        if line[i] != '0':
            curr_num = int(line[i])
            if i % 2 == 0:
                input['fileblocks'].append(curr_num)
                input['line'].append((str(id_count) * curr_num, curr_num, id_count))
                id_count += 1
            else:
                input['spaces'].append(curr_num)
                input['line'].append(('.' * curr_num, curr_num))
    return input

def solve(input: FileData):

    def print_line():
        print_line = ""
        for line_data in input['line']:
            print_line += line_data[0]
        print(''.join(print_line))

    #print_line()

    c = 0
    i = len(input['line'])-1
    while i > 0:
    #for i in range(len(input['line'])-1, -1, -1):
        right = input['line'][i]
        # if c == 29:
        #     print("30 hit")
        # if c > 35:
        #     exit(0)
        # if '998099809980998099809980998099809980' == right[0]:
        #     breakpoint()
        # if you're on a currently swappable index...
        if '.' not in right[0]:
            # search for a swap greedily, iterate from left to right and use the first available
            for j in range(i):
                left = input['line'][j]
                # if you can swap: (need to be >= size of right and empty, ie: '.')
                if '.' in left[0] and left[1] >= right[1]:
                    # Do a swap!
                    # need to do some book keeping though if sizes mismatch...
                    if left[1] > right[1]:
                        # split the current left into 2 parts so you can swap it around easy...
                        # need to account for multiple digit numbers in the string? No actually I dont think I need to
                        extra_left = (left[0][right[1]:], left[1] - right[1])
                        left = (left[0][:right[1]], right[1])
                        input['line'] = input['line'][:j] + [left, extra_left] + input['line'][j+1:]
                        # make sure i gets updated to an array that got resized to prev-size + 1!!!
                        i+=1
                    input['line'][j], input['line'][i] = input['line'][i], input['line'][j]
                    #print_line()
                    #print(input['line'][-50:], end="\n\n")
                    break
        c += 1
        i -= 1

    checksum = 0
    calc_array = []
    for i, line_data in enumerate(input['line']):
        for _num_elts in range(line_data[1]):
            if '.' not in line_data[0]:
                calc_array.append(line_data[2])
            else:
                calc_array.append('.')
    for i in range(len(calc_array)):
        if calc_array[i] != '.':
            checksum += i * calc_array[i]
    solution = checksum
    #print_line()
    print(f"Solution: {solution}")
    # answer of 6428224455282 is too high...