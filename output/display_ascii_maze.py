from mazegen import MazeGenerator, SolveMaze
from mazegen.cell import Cell
from output.colors import (BG_BLUE, BG_BRIGHT_RED, BG_BRIGHT_YELLOW,
                           BG_MAGENTA, BRIGHT_GREEN, BRIGHT_RED,
                           BRIGHT_WHITE, GREEN, MAGENTA, RED, RESET)


class DisplayMazeAscii:
    def __init__(
        self,
        maze: MazeGenerator,
        solver: SolveMaze,
    ) -> None:
        self.maze = maze
        self.solver = solver

    def build_path_coords(self, directions: list[str]) -> set[tuple[int, int]]:
        x, y = self.maze.entry
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

    def display(self, show_path: bool = False,
                change_color: bool = False) -> None:
        directions = self.solver.solve_maze()
        path_coords = self.build_path_coords(directions)

        for row in self.maze.grid:
            print(self.upper_line(row, change_color))
            print(self.middle_line(row, path_coords, show_path, change_color))
        print(self.lower_line(self.maze.grid[-1], change_color))

    def upper_line(self, row: list[Cell],
                   change_color: bool = False) -> str:
        color = BRIGHT_WHITE
        if change_color:
            color = BRIGHT_GREEN
        line = f"{color}+{RESET}"
        for cell in row:
            line += (f"{color}---+{RESET}"
                     if cell.direction["N"]
                     else f"{color}   +{RESET}")
        return line

    def middle_line(self, row: list[Cell],
                    path_coords: set[tuple[int, int]],
                    show_path: bool = False,
                    change_color: bool = False) -> str:

        entry = f"{GREEN}E{RESET}"
        exit = f"{RED}X{RESET}"
        path = f"{BG_BLUE} {RESET}"
        cell_close = f"{BG_MAGENTA} {RESET}"
        bar = f"{BRIGHT_WHITE}|{RESET}"
        if change_color:
            entry = f"{BRIGHT_RED}E{RESET}"
            exit = f"{MAGENTA}X{RESET}"
            path = f"{BG_BRIGHT_RED} {RESET}"
            cell_close = f"{BG_BRIGHT_YELLOW} {RESET}"
            bar = f"{BRIGHT_GREEN}|{RESET}"
        line = ""
        for cell in row:
            line += bar if cell.direction["W"] else " "
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

        line += bar if row[-1].direction["E"] else " "
        return line

    def lower_line(self, row: list[Cell],
                   change_color: bool = False) -> str:
        color = BRIGHT_WHITE
        if change_color:
            color = BRIGHT_GREEN
        line = f"{color}+{RESET}"
        for cell in row:
            line += (f"{color}---+{RESET}"
                     if cell.direction["S"]
                     else f"{color}   +{RESET}")
        return line
