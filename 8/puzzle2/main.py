import sys
from sln import parse_input, solve

def get_input(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return parse_input(fh)

def main():
    input = get_input(sys.argv[1])
    import timeit
    print(timeit.timeit(lambda: solve(input), number=1))

if __name__ == "__main__":
    main()