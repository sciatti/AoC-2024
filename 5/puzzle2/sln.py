from io import TextIOBase
from dataclasses import dataclass

@dataclass
class ParsedInput:
    rules: list
    updates: list

def parse_input(file_handler: TextIOBase):
    data = ParsedInput(rules=[], updates=[])
    parse_updates = False
    for line in file_handler.readlines():
        if line == "\n":
            parse_updates = True
            continue
        pages, append_list = (line.rstrip().split(','), data.updates) if parse_updates else (line.rstrip().split('|'), data.rules)
        append_list.append([int(page) for page in pages])
    return data

def solve(input: ParsedInput):
    solution = [] # list of corrected updates
    correct_updates = []
    incorrect_updates = []

    def create_rules_dict(rules):
        # Create a dict mapping page number to its rules
        # each rule is input as a list of a list of ints
        mapping = {}
        for rule in rules:
            page1, page2 = rule[0], rule[1]
            if page1 not in mapping:
                mapping[page1] = {page2: rule}
            else:
                mapping[page1][page2] = rule
            if page2 not in mapping:
                mapping[page2] = {page1: rule}
            else:
                mapping[page2][page1] = rule
                    
        return mapping

    rules_map = create_rules_dict(input.rules)

    for update in input.updates:
        bad_update = False
        for curr_idx, curr_page in enumerate(update):
            # Iterate through all pages in an update and check if
            # anything infront of that page is violating any rules 
            if curr_page in rules_map:
                for previous_page in update[:curr_idx]:
                    if previous_page in rules_map[curr_page]:
                        rule = rules_map[curr_page][previous_page]
                        if curr_page == rule[0] and previous_page == rule[1]:
                            bad_update = True
                            break
            if bad_update: break
        if not bad_update:
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)
    
    corrected_updates = []
    for update in incorrect_updates:
        # breakpoint()
        i = 0
        while i < len(update) - 1:
        # for i in range(len(update) - 1):
            updated_i = False
            curr_page = update[i]
            # check if this guy is violating any rules
            j = i + 1
            while j < len(update):
                later_page = update[j]
                if (curr_page in rules_map) and (later_page in rules_map[curr_page]):
                    rule = rules_map[curr_page][later_page]
                    if later_page == rule[0] and curr_page == rule[1]:
                        update[i], update[j] = update[j], update[i]
                        updated_i = True
                        break
                j += 1
            if updated_i:
                i -= 1
            i += 1
        corrected_updates.append(update)

    solution = corrected_updates

    sum_answer = 0
    for update in solution:
        sum_answer += update[len(update)//2]
    print(f"Number of corrected rules: {len(solution)}")
    print(f"Sum of middle pages from corrected rules: {sum_answer}")