from __future__ import annotations
from typing import TypedDict
from collections import deque

class Node(TypedDict):
    indices: tuple[int, int]
    value: int
    edges: Edges

class Edges(TypedDict):
    up: Node | None
    right: Node | None
    down: Node | None
    left: Node | None

class Dirs(TypedDict):
    up: tuple[int, int]
    right: tuple[int, int]
    down: tuple[int, int]
    left: tuple[int, int]

class Trail(TypedDict):
    rating: int
    peaks: set[tuple[int, int]]

SEARCH_DIRS: Dirs = Dirs(up=(-1, 0), right=(0, 1), down=(1, 0), left=(0, -1))

def check_bounds(grid: list[list[int]], indices: tuple[int, int]) -> bool:
    if indices[0] < 0 or indices[0] > len(grid) - 1:
        return False
    if indices[1] < 0 or indices[1] > len(grid[0]) - 1:
        return False
    return True

def parse_input(file_handler) -> list[list[int]]:
    input: list[list[int]] = []
    for line in file_handler.readlines():
        input.append([int(char) for char in line.rstrip()])
    return input

def create_graph(input_grid: list[list[int]]) -> list[list[Node]]:
    graph_list: list[list[Node]] = []
    for i in range(len(input_grid)):
        graph_list.append([])
        for j in range(len(input_grid[i])):
            edges: Edges = Edges()
            graph_list[-1].append(Node(indices=(i,j), value=input_grid[i][j], edges=edges))

    for i in range(len(graph_list)):
        for j in range(len(graph_list[i])):
            curr_node: Node = graph_list[i][j]
            for dir_key in SEARCH_DIRS:
                dir = SEARCH_DIRS[dir_key]
                check_indices = (dir[0] + i, dir[1] + j)
                if check_bounds(graph_list, check_indices):
                    check_node: Node = graph_list[check_indices[0]][check_indices[1]]
                    if check_node['value'] - curr_node['value'] == 1:
                        curr_node['edges'][dir_key] = check_node

    return graph_list

def get_start_and_ends(graph_list: list[list[Node]]):
    trailheads = set()
    peaks = set()
    for i in range(len(graph_list)):
        for j in range(len(graph_list[i])):
            curr_node: Node = graph_list[i][j]
            if curr_node['value'] == 0:
                trailheads.add((i, j))
            elif curr_node['value'] == 9:
                peaks.add((i, j))
    return trailheads, peaks

def solve(input):
    graph = create_graph(input)
    trailheads, peaks = get_start_and_ends(graph)
    trails: dict[tuple[int, int], Trail] = {}
    for trailhead in trailheads:
        trails[trailhead] = {'rating': 0, 'peaks': {}}
        paths: dict[tuple[int, int], int] = {}
        stack: deque[Node] = deque()
        curr_node = graph[trailhead[0]][trailhead[1]]
        while curr_node:
            if curr_node['value'] == 9:
                if curr_node['indices'] not in trails[trailhead]['peaks']:
                    trails[trailhead]['peaks'][curr_node['indices']] = 1
                else:
                    trails[trailhead]['peaks'][curr_node['indices']] += 1
            else:
                for edge_key in curr_node['edges']:
                    stack.append(curr_node['edges'][edge_key])
            
            if curr_node['indices'] not in paths:
                paths[curr_node['indices']] = 1
            else:
                paths[curr_node['indices']] += 1

            curr_node = stack.pop() if len(stack) > 0 else None

        if len(trails[trailhead]['peaks']) > 0:
            for times_peak_reached in trails[trailhead]['peaks'].values():
                trails[trailhead]['rating'] += times_peak_reached

    solution = 0
    for trail in trails.values():
        solution += trail['rating']

    print(f"Solution: {solution}")