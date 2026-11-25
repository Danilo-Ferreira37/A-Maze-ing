from collections import deque
from mazegen import MazeGenerator
from mazegen.cell import Cell
from typing import Any, Deque
from parsing.model import MazeConfig
import random


class SolveMaze:
    def __init__(self, maze: "MazeGenerator", config: MazeConfig) -> None:
        self.maze = maze
        self.config = config
        self.grid: list[list[Cell]] = maze.grid
        self.dfs_backtracing: Any = maze.dfs_backtracing

    @staticmethod
    def get_neighbors(
        position: tuple[int, int],
        maze: 'MazeGenerator'
    ) -> list[tuple[str, tuple[int, int]]]:
        x, y = position
        cell = maze.grid[y][x]
        directions: list[tuple[str, tuple[int, int]]] = []
        if cell.direction["N"] == 0:
            directions.append(("N", (x, y - 1)))
        if cell.direction["E"] == 0:
            directions.append(("E", (x + 1, y)))
        if cell.direction["S"] == 0:
            directions.append(("S", (x, y + 1)))
        if cell.direction["W"] == 0:
            directions.append(("W", (x - 1, y)))
        valid_neighbors: list[tuple[str, tuple[int, int]]] = []
        for direction, (nx, ny) in directions:
            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                valid_neighbors.append((direction, (nx, ny)))
        return valid_neighbors

    def solve_maze(self) -> list[str]:
        entry: tuple[int, int] = self.config["ENTRY"]
        exit: tuple[int, int] = self.config["EXIT"]
        queue: Deque[tuple[tuple[int, int], list[str]]] = deque()
        queue.append((entry, []))
        visited: set[tuple[int, int]] = {entry}
        while queue:
            current_position, path = queue.popleft()
            if current_position == exit:
                return path
            for direction, neighbor in self.get_neighbors(
                current_position,
                self.maze
            ):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [direction]))
        return []

    @staticmethod
    def build_path_coords(
        entry: tuple[int, int],
        directions: list[str]
    ) -> set[tuple[int, int]]:
        x, y = entry
        path: list[tuple[int, int]] = [(x, y)]
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

    def write_solution(self) -> None:
        path = self.solve_maze()
        solution = "".join(path) if path else ""
        with open(self.config["OUTPUT_FILE"], "a") as f:
            f.write(solution)

    def find_paths(self, x: int, y: int, path: list[str]) -> None:
        self.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        while True:
            if self.grid[y][x].exit:
                return
            if not directions:
                return
            dir_choice = random.choice(directions)
            directions.remove(dir_choice)
            if dir_choice == "N" and not self.grid[y][x].direction["N"]:
                if not self.grid[y - 1][x].visited:
                    path.append("N")
                    self.dfs_backtracing(x, y - 1, path)
            elif dir_choice == "E" and not self.grid[y][x].direction["E"]:
                if not self.grid[y][x + 1].visited:
                    path.append("E")
                    self.dfs_backtracing(x + 1, y, path)
            elif dir_choice == "S" and not self.grid[y][x].direction["S"]:
                if not self.grid[y + 1][x].visited:
                    path.append("S")
                    self.dfs_backtracing(x, y + 1, path)
            elif dir_choice == "W" and not self.grid[y][x].direction["W"]:
                if not self.grid[y][x - 1].visited:
                    path.append("W")
                    self.dfs_backtracing(x - 1, y, path)
