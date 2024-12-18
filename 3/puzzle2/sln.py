from dataclasses import dataclass

@dataclass
class OccurrenceData:
    start: int
    end: int

program_str = ""

with open("input.txt", "r", encoding="utf-8") as program_file:
    for line in program_file.readlines():
        program_str += line

# find all potential occurrences
occurrences = []
start = 0
while True:
    start = program_str.find("mul(", start)
    if start == -1:
        break
    occurrences.append(OccurrenceData(start=start, end=-1))
    start += 1

# find all do() indices
do_indices = []
start = 0
while True:
    start = program_str.find("do()", start)
    if start == -1:
        break
    do_indices.append(start)
    start += 1

# find all don't() indices
dont_indices = []
start = 0
while True:
    start = program_str.find("don't()", start)
    if start == -1:
        break
    dont_indices.append(start)
    start += 1

print(len(occurrences))
temp_oc = []
# scan through occurrences and remove elements which don't have a closing ')' and a ','
for index in occurrences:
    # maximally, there can be at most 8 elements past the opening '('
    # ie: mul(123,456))
    start_index = index.start + len("mul(")
    end_index = start_index + 8
    substr = program_str[start_index:end_index]
    if ',' in substr and ')' in substr:
        close_paren_idx = substr.find(')')
        index.end = start_index + close_paren_idx
        temp_oc.append(index)

occurrences = temp_oc
print(len(occurrences))

# scan for the closing ')' before sending input to this function
def is_valid_mul(substr):
    # Every valid multiply call must start and end with a number and have a comma
    found_comma = False
    for i, char in enumerate(substr):
        if i == 0 and not str.isdigit(char):
            return False
        elif i == len(substr) - 1 and not str.isdigit(char):
            return False
        elif found_comma:
            if not str.isdigit(char):
                return False
        else:
            if not (char == ',' or str.isdigit(char)):
                return False
            if char == ",":
                found_comma = True
    return True

valid_muls = []
for test_occurrence in occurrences:
    test_string = program_str[test_occurrence.start+len("mul("):test_occurrence.end]
    if is_valid_mul(test_string):
        valid_muls.append(test_occurrence)
    else:
        print(test_occurrence)

for o in occurrences:
    if o not in valid_muls:
        print(program_str[o.start:o.start+12])

def convert_mul(substr):
    operands = substr.split(',')
    return int(operands[0]), int(operands[1])

do_idx, dont_idx = 0, 0
mul_sum = 0
do_enabled = True
for mul_op_indices in valid_muls:
    # first I need to determine the closest do() and don't() statements that are still behind the current index
    while do_idx < len(do_indices) - 1 and do_indices[do_idx+1] < mul_op_indices.start:
        # because the do() and dont() indices were found in order, I know that I only need to search
        # the next index and keep incrementing if it's smaller than the index of the current mul_op
        do_idx += 1
    while dont_idx < len(dont_indices) - 1 and dont_indices[dont_idx+1] < mul_op_indices.start:
        dont_idx += 1
    do_val, dont_val = do_indices[do_idx], dont_indices[dont_idx]
    # When the program starts multiplying, the first do and dont instructions may be infront
    # of the current mul() operation. This will stabilize as the program runs and the two
    # while loops above will find the nearest do() and dont() function that is behind the current mul() op.
    if do_val < mul_op_indices.start and dont_val < mul_op_indices.start:
        # determine if a do() or a dont() is the closest behind the current index...
        do_enabled = True if do_val > dont_val else False
    # Because we start with do() enabled, we only need to check the singular edge case where dont is behind
    # the current mul() op and do() is infront of that mul() op.
    elif dont_val < mul_op_indices.start and do_val > mul_op_indices.start:
        do_enabled = False
    
    if do_enabled:
        mul_op_str = program_str[mul_op_indices.start+len("mul("):mul_op_indices.end]
        mul_operands = convert_mul(mul_op_str)
        mul_sum += mul_operands[0] * mul_operands[1]

print(f"Sum: {mul_sum}")
