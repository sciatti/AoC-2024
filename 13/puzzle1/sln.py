from dataclasses import dataclass

@dataclass
class ClawMachineData:
    A_Button: tuple[int, int]
    B_Button: tuple[int, int]
    Prize: tuple[int, int]

def parse_input(file_handler) -> list[ClawMachineData]:
    puzzle_input: list[ClawMachineData] = []
    def button_parse(line: str) -> tuple[int, int]:
        x_indices = (line.find('+') + 1, line.find(','))
        y_index = line.find('+', x_indices[1]) + 1
        return (int(line[x_indices[0]:x_indices[1]]), int(line[y_index:]))
    def target_parse(line: str) -> tuple[int, int]:
        x_indices = (line.find('=') + 1, line.find(','))
        y_index = line.find('=', x_indices[1]) + 1
        return (int(line[x_indices[0]:x_indices[1]]), int(line[y_index:]))

    line = file_handler.readline().rstrip()
    while line:
        # parse the buttons
        a_button = button_parse(line)
        line = file_handler.readline().rstrip()
        b_button = button_parse(line)
        line = file_handler.readline().rstrip()
        target = target_parse(line)
        # create and append a button
        puzzle_input.append(ClawMachineData(A_Button=a_button, B_Button=b_button, Prize=target))
        # try reading the next button
        line = file_handler.readline()
        if line != "":
            line = file_handler.readline()
    return puzzle_input

def solve(puzzle_input: list[ClawMachineData]) -> None:
    def calculatePresses(machine: ClawMachineData) -> tuple[int, int] | None:
        prize = machine.Prize
        a_button, b_button = machine.A_Button, machine.B_Button
        a_press_denom = a_button[1] * b_button[0] - a_button[0] * b_button[1]
        b_press_denom = a_button[0] * b_button[1] - a_button[1] * b_button[0]
        if a_press_denom == 0 or b_press_denom == 0:
            return None
        
        a_press_numer = prize[1] * b_button[0] - prize[0] * b_button[1]
        b_press_numer = prize[1] * a_button[0] - prize[0] * a_button[1]
        if a_press_numer % a_press_denom != 0 or b_press_numer % b_press_denom != 0:
            return None
        
        return (a_press_numer // a_press_denom, b_press_numer // b_press_denom)
    
    solution = 0
    for machine in puzzle_input:
        num_presses = calculatePresses(machine)
        if num_presses:
            solution += 3* num_presses[0] + num_presses[1]
    print(f"Solution: {solution}")