from typing import TypedDict

class FileData(TypedDict):
    fileblocks: list[int]
    spaces: list[int]
    line: list[str]

def parse_input(file_handler):
    input: FileData = { 'fileblocks': [], 'spaces': [], 'line': [] }
    id_count = 0
    for line in file_handler.readlines():
        print(len(line))
        for i in range(len(list(line))):
            curr_num = int(line[i])
            if i % 2 == 0:
                input['fileblocks'].append(curr_num)
                input['line'] += [str(id_count)] * curr_num
                id_count += 1
            else:
                input['spaces'].append(curr_num)
                input['line'] += list('.' * curr_num)
    return input

def solve(input: FileData):
    l_index, r_index = input['line'].index('.'), len(input['line']) - 1
    while l_index < r_index:
        left, right = input['line'][l_index], input['line'][r_index]
        # if you can swap (need to see a '.' on the left and a num on the right):
        if left == '.' and right.isnumeric():
            # Do a swap!
            input['line'][l_index], input['line'][r_index] = input['line'][r_index], input['line'][l_index]
            l_index += 1
            r_index -= 1
        # otherwise you have 1 of 2 cases
        else:
            # there's a dot on the left and a dot on the right...
            if left == '.' and right == '.':
                # need to decrement the right index
                r_index -= 1
            # otherwise, there's NOT a dot on the left, so we increment that first before we check the right again
            else:
                l_index += 1

    #print(''.join(input['line']))
    print(input['line'].index('.'))
    solution = sum([int(input['line'][i])*i for i in range(input['line'].index('.'))])
    print(f"Solution: {solution}")
    # answer of 89859464970 is too low...
    # the answer is: 6330095022244