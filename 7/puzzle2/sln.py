from dataclasses import dataclass

@dataclass
class Equation:
    solution: int
    values: list[int]

def parse_input(file_handler) -> list[Equation]:
    input: list[Equation] = []
    for line in file_handler.readlines():
        equation = line.rstrip().split(':')
        solution, values = equation[0], equation[1].lstrip().split(" ")
        input.append(Equation(solution=int(solution), values=[int(val) for val in values]))
    return input

def check_perm(sol: int, currTot: int, values: list[int]):
    val = values[0]
    addSol = currTot + val
    mulSol = currTot * val if currTot > 0 else val
    concatSol = int(str(currTot) + str(val)) if currTot > 0 else val
    # if we are on the last possible value:
    if len(values) == 1:
        if (sol == addSol or mulSol == sol or sol == concatSol):
            return True
        else:
            return False
    # if we are not on the last possible value:
    else:
        # we must only continue if our current operation creates a new total value < sol
        if (mulSol <= sol):
            check_mul_perm = check_perm(sol, mulSol, values[1:])
            if check_mul_perm:
                return True
        if (addSol <= sol):
            check_add_perm = check_perm(sol, addSol, values[1:])
            if check_add_perm:
                return True
        if (concatSol <= sol):
            check_concat_perm = check_perm(sol, concatSol, values[1:])
            if check_concat_perm:
                return True
        return False

def solve(input: list[Equation]) -> None:
    valid_inputs: list[int] = []
    for equation in input:
        perm_check = check_perm(equation.solution, 0, equation.values)
        # iterate through the values and start checking each permutation for each number
        if perm_check:
            valid_inputs.append(equation.solution)
            
    solution = sum(valid_inputs)
    print(f"Solution: {solution}")
    #print(valid_inputs)
 
    # answer is: 91377448644679

# EX:
# 1   2
# 1 + 2
# 1 * 2

# 1   2   3
# 1 + 2 + 3
# 1 * 2 + 3
# 1 + 2 * 3
# 1 * 2 * 3

# 1   2   3   4
# 1 + 2 + 3 + 4
# 1 * 2 + 3 + 4
# 1 + 2 * 3 + 4
# 1 * 2 * 3 + 4
# 1 + 2 + 3 * 4
# 1 * 2 + 3 * 4
# 1 + 2 * 3 * 4
# 1 * 2 * 3 * 4

# 1   2   3   4   5
# 1 + 2 + 3 + 4 + 5
# 1 * 2 + 3 + 4 + 5
# 1 + 2 * 3 + 4 + 5
# 1 * 2 * 3 + 4 + 5
# 1 + 2 + 3 * 4 + 5
# 1 * 2 + 3 * 4 + 5
# 1 + 2 * 3 * 4 + 5
# 1 * 2 * 3 * 4 + 5
# -----------------
# 1 + 2 + 3 + 4 * 5
# 1 * 2 + 3 + 4 * 5
# 1 + 2 * 3 + 4 * 5
# 1 * 2 * 3 + 4 * 5
# 1 + 2 + 3 * 4 * 5
# 1 * 2 + 3 * 4 * 5
# 1 + 2 * 3 * 4 * 5
# 1 * 2 * 3 * 4 * 5

# 1   2   3   4   5   6
# 1 + 2 + 3 + 4 + 5 + 6
# 1 * 2 + 3 + 4 + 5 + 6
# 1 + 2 * 3 + 4 + 5 + 6
# 1 * 2 * 3 + 4 + 5 + 6
# 1 + 2 + 3 * 4 + 5 + 6
# 1 * 2 + 3 * 4 + 5 + 6
# 1 + 2 * 3 * 4 + 5 + 6
# 1 * 2 * 3 * 4 + 5 + 6
# ---------------------
# 1 + 2 + 3 + 4 * 5 + 6
# 1 * 2 + 3 + 4 * 5 + 6
# 1 + 2 * 3 + 4 * 5 + 6
# 1 * 2 * 3 + 4 * 5 + 6
# 1 + 2 + 3 * 4 * 5 + 6
# 1 * 2 + 3 * 4 * 5 + 6
# 1 + 2 * 3 * 4 * 5 + 6
# 1 * 2 * 3 * 4 * 5 + 6
# =====================
# 1 + 2 + 3 + 4 + 5 * 6
# 1 * 2 + 3 + 4 + 5 * 6
# 1 + 2 * 3 + 4 + 5 * 6
# 1 * 2 * 3 + 4 + 5 * 6
# 1 + 2 + 3 * 4 + 5 * 6
# 1 * 2 + 3 * 4 + 5 * 6
# 1 + 2 * 3 * 4 + 5 * 6
# 1 * 2 * 3 * 4 + 5 * 6
# ---------------------
# 1 + 2 + 3 + 4 * 5 * 6
# 1 * 2 + 3 + 4 * 5 * 6
# 1 + 2 * 3 + 4 * 5 * 6
# 1 * 2 * 3 + 4 * 5 * 6
# 1 + 2 + 3 * 4 * 5 * 6
# 1 * 2 + 3 * 4 * 5 * 6
# 1 + 2 * 3 * 4 * 5 * 6
# 1 * 2 * 3 * 4 * 5 * 6

# 1   2   3   4   5   6   7
# 1 + 2 + 3 + 4 + 5 + 6 + 7
# 1 * 2 + 3 + 4 + 5 + 6 + 7
# 1 + 2 * 3 + 4 + 5 + 6 + 7
# 1 * 2 * 3 + 4 + 5 + 6 + 7
# 1 + 2 + 3 * 4 + 5 + 6 + 7
# 1 * 2 + 3 * 4 + 5 + 6 + 7
# 1 + 2 * 3 * 4 + 5 + 6 + 7
# 1 * 2 * 3 * 4 + 5 + 6 + 7
# -------------------------
# 1 + 2 + 3 + 4 * 5 + 6 + 7
# 1 * 2 + 3 + 4 * 5 + 6 + 7
# 1 + 2 * 3 + 4 * 5 + 6 + 7
# 1 * 2 * 3 + 4 * 5 + 6 + 7
# 1 + 2 + 3 * 4 * 5 + 6 + 7
# 1 * 2 + 3 * 4 * 5 + 6 + 7
# 1 + 2 * 3 * 4 * 5 + 6 + 7
# 1 * 2 * 3 * 4 * 5 + 6 + 7
# =========================
# 1 + 2 + 3 + 4 + 5 * 6 + 7
# 1 * 2 + 3 + 4 + 5 * 6 + 7
# 1 + 2 * 3 + 4 + 5 * 6 + 7
# 1 * 2 * 3 + 4 + 5 * 6 + 7
# 1 + 2 + 3 * 4 + 5 * 6 + 7
# 1 * 2 + 3 * 4 + 5 * 6 + 7
# 1 + 2 * 3 * 4 + 5 * 6 + 7
# 1 * 2 * 3 * 4 + 5 * 6 + 7
# -------------------------
# 1 + 2 + 3 + 4 * 5 * 6 + 7
# 1 * 2 + 3 + 4 * 5 * 6 + 7
# 1 + 2 * 3 + 4 * 5 * 6 + 7
# 1 * 2 * 3 + 4 * 5 * 6 + 7
# 1 + 2 + 3 * 4 * 5 * 6 + 7
# 1 * 2 + 3 * 4 * 5 * 6 + 7
# 1 + 2 * 3 * 4 * 5 * 6 + 7
# 1 * 2 * 3 * 4 * 5 * 6 + 7
# =========================
# =========================
# 1 + 2 + 3 + 4 + 5 + 6 * 7
# 1 * 2 + 3 + 4 + 5 + 6 * 7
# 1 + 2 * 3 + 4 + 5 + 6 * 7
# 1 * 2 * 3 + 4 + 5 + 6 * 7
# 1 + 2 + 3 * 4 + 5 + 6 * 7
# 1 * 2 + 3 * 4 + 5 + 6 * 7
# 1 + 2 * 3 * 4 + 5 + 6 * 7
# 1 * 2 * 3 * 4 + 5 + 6 * 7
# -------------------------
# 1 + 2 + 3 + 4 * 5 + 6 * 7
# 1 * 2 + 3 + 4 * 5 + 6 * 7
# 1 + 2 * 3 + 4 * 5 + 6 * 7
# 1 * 2 * 3 + 4 * 5 + 6 * 7
# 1 + 2 + 3 * 4 * 5 + 6 * 7
# 1 * 2 + 3 * 4 * 5 + 6 * 7
# 1 + 2 * 3 * 4 * 5 + 6 * 7
# 1 * 2 * 3 * 4 * 5 + 6 * 7
# =========================
# 1 + 2 + 3 + 4 + 5 * 6 * 7
# 1 * 2 + 3 + 4 + 5 * 6 * 7
# 1 + 2 * 3 + 4 + 5 * 6 * 7
# 1 * 2 * 3 + 4 + 5 * 6 * 7
# 1 + 2 + 3 * 4 + 5 * 6 * 7
# 1 * 2 + 3 * 4 + 5 * 6 * 7
# 1 + 2 * 3 * 4 + 5 * 6 * 7
# 1 * 2 * 3 * 4 + 5 * 6 * 7
# -------------------------
# 1 + 2 + 3 + 4 * 5 * 6 * 7
# 1 * 2 + 3 + 4 * 5 * 6 * 7
# 1 + 2 * 3 + 4 * 5 * 6 * 7
# 1 * 2 * 3 + 4 * 5 * 6 * 7
# 1 + 2 + 3 * 4 * 5 * 6 * 7
# 1 * 2 + 3 * 4 * 5 * 6 * 7
# 1 + 2 * 3 * 4 * 5 * 6 * 7
# 1 * 2 * 3 * 4 * 5 * 6 * 7