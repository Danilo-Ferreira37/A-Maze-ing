"""
MazeGenerator – Reusable Maze Generation Module
==============================================

This module provides the MazeGenerator class used in the A‑Maze‑Ing project.
It is a standalone, importable maze generator suitable for packaging as
mazegen-* and installation via pip. The generator supports configurable size,
entry/exit coordinates, perfect/non‑perfect generation, optional random seed,
and exposes both the internal maze structure and a shortest‑path solution.

Basic Usage
-----------

    from mazegen import MazeGenerator

    mg = MazeGenerator(
        height=10,
        width=10,
        entry=(0, 0),
        exit=(9, 9),
        output_file="maze.txt",
        perfect=True,
        seed=42
    )                          # Maze generation (DFS)
    maze = mg.get_maze()       # Internal structure
    path = mg.get_path()       # Shortest path (BFS)

Parameters
----------

height : int
    Number of rows in the maze.
width : int
    Number of columns in the maze.
entry : (int, int)
    Starting cell coordinates (x, y).
exit : (int, int)
    Ending cell coordinates (x, y).
output_file : str
    File where the hexadecimal maze representation is written.
perfect : bool
    If True, the maze contains no cycles.
seed : int, optional
    Optional seed for reproducible maze generation.

Public Methods
--------------

get_maze()
    Returns the internal maze representation.
get_solution()
    Returns the shortest path from entry to exit (computed via BFS).

Notes
-----

• This module only provides reusable generation and solving logic.
  Rendering, ASCII display, configuration parsing, and direction output
  belong to the main A‑Maze‑Ing project.

• The internal structure format does not need to match the output file format.
"""
import random
from typing import TYPE_CHECKING
from .cell import Cell
from parsing.model import MazeConfig


if TYPE_CHECKING:
    from . import SolveMaze


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        random.seed(config["SEED"])
        self.config = config
        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        self.grid_creator()
        self.fourty_two()

        self.dfs_backtracing(self.entry[0], self.entry[1], perfect=self.perfect)
        self.output_hex()
        SolveMaze = self.get_class()
        sv = SolveMaze(self, config)
        self.path = sv.solve_maze()

    @staticmethod
    def get_class() -> type["SolveMaze"]:
        from . import SolveMaze
        return SolveMaze

    def close_cell(self, y: int, x: int) -> None:
        if self.grid[y][x].entry or self.grid[y][x].exit:
            print("Error: The coordinades of entry and"
                  " exit cannot be in a closed cell.")
            exit(1)
        self.grid[y][x].maze_limit.update({"N": 1, "E": 1, "S": 1, "W": 1})
        self.grid[y - 1][x].maze_limit["S"] = 1
        self.grid[y + 1][x].maze_limit["N"] = 1
        self.grid[y][x + 1].maze_limit["W"] = 1
        self.grid[y][x - 1].maze_limit["E"] = 1
        self.grid[y][x].closed = True

    def grid_creator(self) -> list[list[Cell]]:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(y, x, self.height, self.width))
            grid.append(row)
        self.grid = grid
        self.define_entry(self.entry[0], self.entry[1])
        self.define_exit(self.exit[0], self.exit[1])
        return grid

    def define_entry(self, x: int, y: int) -> None:
        self.grid[y][x].entry = True
        self.grid[y][x].visited = True

    def define_exit(self, x: int, y: int) -> None:
        self.grid[y][x].exit = True

    def remove_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        if x == nx and y > ny:
            self.grid[y][x].direction["N"] = 0
            self.grid[ny][nx].direction["S"] = 0
        elif x == nx and y < ny:
            self.grid[y][x].direction["S"] = 0
            self.grid[ny][nx].direction["N"] = 0
        elif y == ny and x < nx:
            self.grid[y][x].direction["E"] = 0
            self.grid[ny][nx].direction["W"] = 0
        elif y == ny and x > nx:
            self.grid[y][x].direction["W"] = 0
            self.grid[ny][nx].direction["E"] = 0

    def dfs_backtracing(self, x: int, y: int, perfect: bool = True) -> None:
        self.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        probably = 0.05
        if self.height <= 15 and self.width <= 15:
            probably = 0.10
        try:
            while (True):
                if len(directions) == 0:
                    return
                dir = random.choice(directions)
                directions.remove(dir)
                if dir == "N" and not self.grid[y][x].maze_limit["N"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x, y - 1)
                        if not self.grid[y - 1][x].visited:
                            self.dfs_backtracing(x, y - 1, False)
                            self.remove_wall(x, y, x, y - 1)

                    elif not self.grid[y - 1][x].visited:
                        self.remove_wall(x, y, x, y - 1)
                        self.dfs_backtracing(x, y - 1)

                elif dir == "E" and not self.grid[y][x].maze_limit["E"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x + 1, y)
                        if not self.grid[y][x + 1].visited:
                            self.dfs_backtracing(x + 1, y, False)
                            self.remove_wall(x, y, x + 1, y)

                    elif not self.grid[y][x + 1].visited:
                        self.remove_wall(x, y, x + 1, y)
                        self.dfs_backtracing(x + 1, y)

                elif dir == "S" and not self.grid[y][x].maze_limit["S"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x, y + 1)
                        if not self.grid[y + 1][x].visited:
                            self.dfs_backtracing(x, y + 1, False)
                            self.remove_wall(x, y, x, y + 1)

                    elif not self.grid[y + 1][x].visited:
                        self.remove_wall(x, y, x, y + 1)
                        self.dfs_backtracing(x, y + 1)

                elif dir == "W" and not self.grid[y][x].maze_limit["W"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x - 1, y)
                        if not self.grid[y][x - 1].visited:
                            self.dfs_backtracing(x - 1, y, False)
                            self.remove_wall(x, y, x - 1, y)

                    elif not self.grid[y][x - 1].visited:
                        self.remove_wall(x, y, x - 1, y)
                        self.dfs_backtracing(x - 1, y)
        except Exception:
            self.dfs_backtracing(x, y, perfect)

    def fourty_two(self) -> None:
        y = int(self.height / 2)
        x = int(self.width / 2)
        self.close_cell(y, x - 1)
        self.close_cell(y, x - 2)
        self.close_cell(y, x - 3)

        self.close_cell(y, x - 3)
        self.close_cell(y - 1, x - 3)
        self.close_cell(y - 2, x - 3)

        self.close_cell(y, x - 1)
        self.close_cell(y + 1, x - 1)
        self.close_cell(y + 2, x - 1)

        self.close_cell(y, x + 1)
        self.close_cell(y, x + 2)
        self.close_cell(y, x + 3)

        self.close_cell(y, x + 3)
        self.close_cell(y - 1, x + 3)
        self.close_cell(y - 2, x + 3)

        self.close_cell(y - 2, x + 1)
        self.close_cell(y - 2, x + 2)
        self.close_cell(y - 2, x + 3)

        self.close_cell(y, x + 1)
        self.close_cell(y + 1, x + 1)
        self.close_cell(y + 2, x + 1)

        self.close_cell(y + 2, x + 1)
        self.close_cell(y + 2, x + 2)
        self.close_cell(y + 2, x + 3)

    def output_hex(self) -> None:
        binarie = ""
        output = ""
        for row in self.grid:
            for cell in row:
                binarie = (str(cell.direction["N"]) +
                           str(cell.direction["E"]) +
                           str(cell.direction["S"]) +
                           str(cell.direction["W"])
                           )
                output += hex(int(binarie, 2))[2:].upper()
            output += '\n'
        output += f"\n{self.entry[0]}, {self.entry[1]}"
        output += f"\n{self.exit[0]}, {self.exit[1]}\n"
        with open(self.output_file, "w") as f:
            f.write(output)

    def get_path(self) -> list[str]:
        return self.path

    def get_maze(self) -> list[list[Cell]]:
        return self.grid
