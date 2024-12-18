from dataclasses import dataclass

@dataclass
class Index:
    row: int
    col: int

def parse_input(file_handler) -> list[list[str]]:
    input = []
    for line in file_handler.readlines():
        input.append(list(line.rstrip()))
    return input

def check_bounds(grid, indices: Index):
    if indices.row < 0 or indices.row > len(grid) - 1:
        return False
    if indices.col < 0 or indices.col > len(grid[0]) - 1:
        return False
    return True

def get_antenna_dict(char_map: list[list[str]]) -> dict[str, list[Index]]:
    antennas: dict[str, list[Index]] = {}
    for row in range(len(char_map)):
        for col in range(len(char_map[row])):
            curr_char = char_map[row][col]
            if curr_char.isalnum():
                if curr_char not in antennas:
                    antennas[curr_char] = [Index(row=row, col=col)]
                else:
                    antennas[curr_char].append(Index(row=row, col=col))
    return antennas

# There should be an edge case where you have two different antinodes at the same location, that *should* count as 2 antinodes I think.
def solve(input: list[list[str]]) -> None:
    antinodes = set()
    antennas_dict = get_antenna_dict(input)

    def calculate_antinode_pos(antenna_vec: Index, antenna_pos: Index) -> Index:
        return Index(row=(antenna_vec.row+antenna_pos.row), col=(antenna_vec.col+antenna_pos.col))

    def calculate_vector(antenna_1: Index, antenna_2: Index) -> Index:
        return Index(row=(antenna_1.row-antenna_2.row), col=(antenna_1.col-antenna_2.col))

    for antenna_type in antennas_dict:
        antennas_list = antennas_dict[antenna_type]
        for antenna_1 in antennas_list:
            for antenna_2 in antennas_list:
                if antenna_1 == antenna_2:
                    continue
                antenna_vector = calculate_vector(antenna_1, antenna_2)
                antinode_pos = calculate_antinode_pos(antenna_vector, antenna_1)
                while check_bounds(grid=input, indices=antinode_pos):
                    antinodes.add((antinode_pos.row, antinode_pos.col))
                    antinode_pos = calculate_antinode_pos(antenna_vector, antinode_pos)
                
                # add the current antenna as an antinode position, it is an edge case
                antinodes.add((antenna_1.row, antenna_1.col))

    solution = len(antinodes)
    print(f"Solution: {solution}")
    # answer is: 905