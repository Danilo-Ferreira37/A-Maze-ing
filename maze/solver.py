from collections import deque
from typing import Deque
from maze.generator import Maze
from parsing.config_parser import ConfigParser


def get_neighbors(position: tuple[int, int],
                  maze: Maze) -> list[tuple[str, tuple[int, int]]]:
    x, y = position
    cell = maze.grid[y][x]
    directions = []
    if cell.direction["N"] == 0:
        directions.append(("N", (x, y - 1)))
    if cell.direction["E"] == 0:
        directions.append(("E", (x + 1, y)))
    if cell.direction["S"] == 0:
        directions.append(("S", (x, y + 1)))
    if cell.direction["W"] == 0:
        directions.append(("W", (x - 1, y)))
    valid_neighbors = []
    for direction, neighbor in directions:
        nx, ny = neighbor
        if 0 <= nx < maze.width and 0 <= ny < maze.height:
            valid_neighbors.append((direction, neighbor))
    return valid_neighbors


def solve_maze(maze: Maze, config: dict) -> list[str]:
    entry = config["ENTRY"]
    exit = config["EXIT"]

    queue: Deque[tuple[tuple[int, int], list[str]]] = deque()
    queue.append((entry, []))

    visited = set([entry])

    while queue:
        current_position, path = queue.popleft()

        if current_position == exit:
            return path

        for direction, neighbor in get_neighbors(current_position, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [direction]))

    return []


def build_path_coords(
    entry: tuple[int, int],
    directions: list[str]
) -> set[tuple[int, int]]:
    x, y = entry
    path = [(x, y)]

    for d in directions:
        if d == "N":
            y -= 1
        elif d == "S":
            y += 1
        elif d == "E":
            x += 1
        elif d == "W":
            x -= 1

        path.append((x, y))

    return set(path)


def write_solution(maze: Maze) -> None:
    config = ConfigParser("config.txt").parse()

    path = solve_maze(maze, config)

    if not path:
        solution = ""
    else:
        solution = "".join(path)

    with open(config["OUTPUT_FILE"], "a") as f:
        f.write(solution)
