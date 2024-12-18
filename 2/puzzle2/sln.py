reports = []
possible_reports = []

with open("input.txt", "r", encoding="utf-8") as input_file_handler:
    for line in input_file_handler.readlines():
        reports.append([int(num) for num in line.split()])

num_safe_reports = 0

for index, report in enumerate(reports):
    safe, increasing = True, True
    num_errors, error_indices = 0, set()
    # set expected count mode from first 2 elements
    if report[0] > report[1]:
        increasing = False
    for i in range(1, len(report)):
        curr = report[i-1]
        nxt = report[i]
        if increasing:
            if curr > nxt:
                safe = False
                num_errors += 1
                error_indices.add(i-1)
                error_indices.add(i)
        else:
            if curr < nxt:
                safe = False
                num_errors += 1
                error_indices.add(i-1)
                error_indices.add(i)
        diff = abs(curr - nxt)
        if diff < 1 or diff > 3:
            safe = False
            num_errors += 1
            error_indices.add(i-1)
            error_indices.add(i)
        if num_errors > 2:
            break
    num_safe_reports += safe * 1
    if not safe:# num_errors <= 3 and num_errors > 0:
        possible_reports.append((index, error_indices))

print(len(possible_reports))

def check_safe(report):
    increasing = True
    # set expected count mode from first 2 elements
    if report[0] > report[1]:
        increasing = False
    for i in range(1, len(report)):
        curr = report[i-1]
        nxt = report[i]
        if increasing:
            if curr > nxt:
                return False
        else:
            if curr < nxt:
                return False
        diff = abs(curr - nxt)
        if diff < 1 or diff > 3:
            return False
    return True

print(len(possible_reports))
# there's a case where an input with 2 errors will have both fixed by removing 1 element
for index, indices in possible_reports:
    test_report = reports[index]
    #print(f"testing report: {test_report}")
    for test_index in range(len(test_report)):
        new_report = None
        if test_index == len(test_report) - 1:
            new_report = test_report[:test_index]
        else:
            new_report = test_report[:test_index] + test_report[test_index+1:]
        #print(f"\tchecking input: {new_report}")
        if check_safe(new_report):
            num_safe_reports += 1
            #print("^^^^^^^^^^^^^^^ Valid Report ^^^^^^^^^^^^^^^")
            break

print(f"Number of Safe Reports: {num_safe_reports}")
