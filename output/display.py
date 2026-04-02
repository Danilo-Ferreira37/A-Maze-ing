from collections.abc import Callable
from parsing.config_parser import ConfigParser
from maze.generator import Maze
from maze.solver import solve_maze
from maze.generator import Cell


def solve_wrapper(maze: Maze) -> list[str]:
    config = ConfigParser("config.txt").parse()
    return solve_maze(maze, config)


class Display_Maze:
    def __init__(
        self,
        maze: Maze,
        solver: Callable[[Maze], list[str]] = solve_wrapper
    ) -> None:
        self.maze = maze
        self.solver = solver

    def build_path_coords(self, directions: list[str]) -> set[tuple[int, int]]:
        x, y = self.maze.entry
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

    def display(self, show_path: bool = False,
                change_color: bool = False) -> None:
        directions = self.solver(self.maze)
        path_coords = self.build_path_coords(directions)

        for row in self.maze.grid:
            print(self.upper_line(row))
            print(self.middle_line(row, path_coords, show_path, change_color))
        print(self.lower_line(self.maze.grid[-1]))

    def upper_line(self, row: list["Cell"]) -> str:
        line = "+"
        for cell in row:
            line += "---+" if cell.direction["N"] else "   +"
        return line

    def middle_line(self, row: list["Cell"],
                    path_coords: set[tuple[int, int]],
                    show_path: bool = False,
                    change_color: bool = False) -> str:
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CIANE = "\033[36m"
        RESET = "\033[0m"
        entry = f"{GREEN}E{RESET}"
        exit = f"{RED}X{RESET}"
        path = f"{BLUE} {RESET}"
        cell_close = f"{PURPLE} {RESET}"

        if change_color:
            entry = f"{CIANE}E{RESET}"
            exit = f"\033[35mX{RESET}"
            path = f"\033[42m {RESET}"
            cell_close = f"{ORANGE} {RESET}"
        line = ""
        for cell in row:
            line += "|" if cell.direction["W"] else " "
            if cell.entry:
                symbol = entry
            elif cell.exit:
                symbol = exit
            elif (cell.x, cell.y) in path_coords and show_path:
                symbol = path
            elif cell.closed:
                symbol = cell_close
            else:
                symbol = " "

            line += f" {symbol} "

        line += "|" if row[-1].direction["E"] else " "
        return line

    def lower_line(self, row: list["Cell"]) -> str:
        line = "+"
        for cell in row:
            line += "---+" if cell.direction["S"] else "   +"
        return line
