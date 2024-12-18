reports = []

with open("input.txt", "r", encoding="utf-8") as input_file_handler:
    for line in input_file_handler.readlines():
        reports.append([int(num) for num in line.split()])

num_safe_reports = 0

for report in reports:
    safe, increasing = True, True
    # set expected count mode from first 2 elements
    if report[0] > report[1]:
        increasing = False
    for i in range(1, len(report)):
        curr = report[i-1]
        nxt = report[i]
        if increasing:
            if curr > nxt:
                safe = False
                break
        else:
            if curr < nxt:
                safe = False
                break
        diff = abs(curr - nxt)
        if diff < 1 or diff > 3:
            safe = False
            break
    num_safe_reports += safe * 1

print(f"Number of Safe Reports: {num_safe_reports}")
