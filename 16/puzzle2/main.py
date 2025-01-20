import sys
from sln import parse_input, solve
import timeit

def get_input(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return parse_input(fh)

def main():
    input = get_input(sys.argv[1])
    print(f"Solution Time: {timeit.timeit(lambda: solve(input), number=1)}")
    print(f"Avg Solution Time: {timeit.timeit(lambda: solve(input, PRINT_SOL=False), number=100) / 100}, num runs: {100}")

if __name__ == "__main__":
    main()
