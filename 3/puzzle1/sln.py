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

print(len(occurrences))
temp_oc = []
# scan through occurrences and remove elements which don't have a closing ')' and a ','
for index in occurrences:
    # maximally, we can have at most 8 elements past the opening '('
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

mul_sum = 0
for mul_op_indices in valid_muls:
    mul_op_str = program_str[mul_op_indices.start+len("mul("):mul_op_indices.end]
    mul_operands = convert_mul(mul_op_str)
    mul_sum += mul_operands[0] * mul_operands[1]

print(f"Sum: {mul_sum}")
# current answer: 161696529 is too low?
