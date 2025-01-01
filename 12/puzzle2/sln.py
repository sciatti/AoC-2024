from __future__ import annotations
from typing import TypedDict
from collections import deque

DIR_DICT: dict[str, tuple[int, int]] = {
    'north': (-1, 0),
    'east': (0, 1),
    'south': (1, 0),
    'west': (0, -1)
}

class Plant(TypedDict):
    plant_type: str
    walls: set[str]

def parse_input(file_handler) -> list[list[Plant]]:
    input: list[list[Plant]] = []
    i = 0
    for line in file_handler.readlines():
        input.append([])
        j = 0
        for char in line.rstrip():
            input[-1].append(
                Plant(
                    plant_type=char,
                    walls=set(['north', 'south', 'east', 'west'])
                )
            )
            j += 1
    i += 1
    return input

def check_bounds(grid: list[list[int]], indices: tuple[int, int]) -> bool:
    if indices[0] < 0 or indices[0] > len(grid) - 1:
        return False
    if indices[1] < 0 or indices[1] > len(grid[0]) - 1:
        return False
    return True

def get_regions(grid: list[list[Plant]]) -> tuple[dict[str, dict[tuple[int, int], int]], dict[int, set[tuple[int, int]]]]:
    # create an inverted mapping of indices to their regions?
    # make it hierarchical, mapping regions first by plant_type,
    # then using a counter to make a key for each unique region encountered
    # and then take all indices and map them to that counter
    # EX:   AABAA
    #       BBBBB
    # ie: { 'A' : { (0,0): 0, (0,1): 0, (0,3): 2, (0,4): 2 } 
    #       'B' : { (0,2): 1, (1,0): 1, (1,1): 1, (1,2): 1, (1,3): 1, (1,4): 1 }
    # also map regions to lists of indices once you finish
    region_key = 0
    regions: dict[str, dict[tuple[int, int], int]] = {}
    regions_by_key: dict[int, set[tuple[int, int]]] = {}
    for i in range((len(grid))):
        for j in range(len(grid[i])):
            # calculate the regions for each given index,
            # we can skip the current item if it's found in the dict
            plant_type = grid[i][j]['plant_type']
            # setup and empty dict if we've not seen this plant type yet
            if plant_type not in regions:
                regions[plant_type] = {}
            # if we have not seen this plant indices for this type...
            # do a search until we iterate through the current region
            if (i,j) not in regions[plant_type]:
                # use a bfs...
                search_queue: deque[tuple[int, int]] = deque()
                search_pos = (i, j)
                while search_pos:
                    # add the current search position to the dict and regions_by_key dict
                    regions[plant_type][search_pos] = region_key
                    if region_key not in regions_by_key:
                        regions_by_key[region_key] = set([search_pos])
                    else:
                        regions_by_key[region_key].add(search_pos)
                    for dir in DIR_DICT.values():
                        new_pos = (dir[0] + search_pos[0], dir[1] + search_pos[1])
                        # if we have an invalid position, skip
                        if not check_bounds(grid, new_pos):
                            continue
                        check_plant = grid[new_pos[0]][new_pos[1]]['plant_type']
                        # if char matches, and it has not been seen before...
                        if check_plant == plant_type and new_pos not in regions[plant_type]:
                            # add it to the queue
                            search_queue.append(new_pos)
                            regions[plant_type][new_pos] = region_key
                    search_pos = search_queue.popleft() if len(search_queue) > 0 else None                
                # increment region key since we just added a new region
                region_key += 1

    return regions, regions_by_key
    
def calculate_walls(grid: list[list[Plant]], regions: dict[str, dict[tuple[int, int], int]]) -> list[list[Plant]]:
    # use the inverted mapping to accurately map the walls
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            plant_type = grid[i][j]['plant_type']
            for dir_name, dir_idx in DIR_DICT.items():
                check_dir = (i + dir_idx[0], j + dir_idx[1])
                # if we find that the current wall and its neighbor are in the same region...
                if check_dir in regions[plant_type]:
                    # remove the wall between them
                    grid[i][j]['walls'].remove(dir_name)
                    # only need to do it on the current item since we iterate over all items
    return grid

def solve(input):
    regions, key_regions = get_regions(input)
    input = calculate_walls(input, regions)
    solution = 0

    # iterate through each region
    # for each region:
    #    iterate through each plant in current region
    #    for each plant in current region:
    #       for each wall that this plant has:
    #           if this plant's wall & index combo has not been added to the sides dict:
    #               # (we have found a new wall that hasn't been looked at yet...)
    #               create a new entry in the sides dict (assign it the current key)
    #               iterate along this wall (if the wall is north/south iterate east/west and vice versa...)
    #               while the next neighbor has a matching wall to this one:
    #                   add the next neighbor to the sides dict (assign it the current key)
    #               increment the current key

    for region_key in key_regions:
        sides: dict[str, dict[tuple[int, int], int]] = {
            # each region MUST have a north, east, south, west side...
            'north': {},
            'east': {},
            'south': {},
            'west': {}
        }
        sides_key = 0
        region = key_regions[region_key]
        # iterate through all plants in the current region...
        for index in region:
            # get the current plant
            plant = input[index[0]][index[1]]
            # iterate through all of its walls...
            for wall_name in plant['walls']:
                # if this plant's wall & index combo has not been added to the sides dict...
                if index not in sides[wall_name]:
                    # found a new side, add it and then find all neighbors which connect to it...
                    #   connected walls will have matching directions with a neighbor...
                    sides[wall_name][index] = sides_key
                    neighbor_check = (0, -1)
                    if wall_name == 'east' or wall_name == 'west':
                        neighbor_check = (-1, 0)
                    # search in positive direction and then negative direction from current index
                    for operand in [1, -1]:
                        neighbor_index = ((operand * neighbor_check[0]) + index[0], (operand * neighbor_check[1]) + index[1])
                        # check if this neighbor is a valid location and in the current region...
                        while check_bounds(input, neighbor_index) and neighbor_index in region:
                            neighbor = input[neighbor_index[0]][neighbor_index[1]]
                            # does our neighbor have a matching wall to this one?
                            if wall_name in neighbor['walls']:
                                # add the neighbor to the sides dict...
                                sides[wall_name][neighbor_index] = sides_key
                                # keep search going in this direction...
                                neighbor_index = ((operand * neighbor_check[0]) + neighbor_index[0], (operand * neighbor_check[1]) + neighbor_index[1])
                            else:
                                break
                    # increment sides key after we found and added the new side
                    sides_key += 1

        solution += len(key_regions[region_key]) * sides_key
    print(f"Solution: {solution}")

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
        # create a sides set which maps the wall-dir and its parallel index value to a wall
        # ie:   a north wall would need the row's index value
        #       since a northern side runs along the row of the region

        # this has a bug where if a region makes a bowing pattern it will count as 1 wall ie:
        # | C  C  C |  
        # +--+   +--+
        #    | C |  
        #    |   +--+
        #    | C  C |
        # In this example the rightmost C plants comprise two distinct walls, but both are counted under the current wall-finding system
        # New wall-finding system should create an inverted mapping of wall sides to dicts of indices mapping to wall id's
        # Essentially the same data structure as what I did to make regions in get_regions
        # ie: { 'north' : { (0,0): 0, (0,1): 0, (0,2): 0 }
        # a structure like this will make checking each individual plant in a region to see if its walls connect to a neighbor's very easy
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################