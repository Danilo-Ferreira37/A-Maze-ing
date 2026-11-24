from collections.abc import Callable
from mazegen import MazeGenerator
from mazegen.cell import Cell
from output.colors import *

CELL_WIDTH = 4

# (cima, baixo, esquerda, direita) -> caracter box-drawing
CORNERS: dict[tuple[bool, bool, bool, bool], str] = {
    (False, False, False, False): " ",
    (False, False, True, True): "─",
    (False, False, True, False): "╴",
    (False, False, False, True): "╶",
    (True, True, False, False): "│",
    (True, False, False, False): "╵",
    (False, True, False, False): "╷",
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, True, True): "┼",
}


class DisplayMazeDropBox:
    def __init__(
        self,
        maze: MazeGenerator,
        solver: Callable[[], list[str]],
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
        directions = self.solver()
        path_coords = self.build_path_coords(directions)

        prev_row = None
        for row in self.maze.grid:
            print(self.upper_line(row, prev_row, change_color))
            print(self.middle_line(row, path_coords, show_path, change_color))
            prev_row = row
        print(self.lower_line(self.maze.grid[-1], change_color))

    def upper_line(self, row: list[Cell],
                   prev_row: list[Cell] | None = None,
                   change_color: bool = False) -> str:
        """Linha de cima da linha atual (paredes N de cada celula).

        A primeira linha usa ┌ ┬ ┐; as seguintes usam ├ ┼ ┤ (ou o que
        corresponder as paredes verticais da linha de cima e da atual).
        """
        n = len(row)
        wall = "─" * CELL_WIDTH
        gap = " " * CELL_WIDTH
        if not change_color:
            line = ""
            for i in range(n + 1):
                left = i > 0 and row[i - 1].direction["N"]
                right = i < n and row[i].direction["N"]
                down = ((i > 0 and row[i - 1].direction["E"])
                        or (i < n and row[i].direction["W"]))
                up = False
                if prev_row is not None:
                    up = ((i > 0 and prev_row[i - 1].direction["E"])
                          or (i < n and prev_row[i].direction["W"]))
                line += f"{BRIGHT_WHITE}{CORNERS[(up, down, left, right)]}{RESET}"
                if i < n:
                    line += (f"{BRIGHT_WHITE}{wall}{RESET}"
                             if row[i].direction["N"]
                             else f"{BRIGHT_WHITE}{gap}{RESET}")
            return line
        line = ""
        for i in range(n + 1):
            left = i > 0 and row[i - 1].direction["N"]
            right = i < n and row[i].direction["N"]
            down = ((i > 0 and row[i - 1].direction["E"])
                    or (i < n and row[i].direction["W"]))
            up = False
            if prev_row is not None:
                up = ((i > 0 and prev_row[i - 1].direction["E"])
                      or (i < n and prev_row[i].direction["W"]))
            line += f"{BRIGHT_GREEN}{CORNERS[(up, down, left, right)]}{RESET}"
            if i < n:
                line += (f"{BRIGHT_GREEN}{wall}{RESET}"
                         if row[i].direction["N"]
                         else f"{BRIGHT_GREEN}{gap}{RESET}")
        return line

    def middle_line(self, row: list[Cell],
                    path_coords: set[tuple[int, int]],
                    show_path: bool = False,
                    change_color: bool = False) -> str:

        left_pad = (CELL_WIDTH - 1) // 2
        right_pad = CELL_WIDTH - 1 - left_pad

        entry = f"{GREEN}E{RESET}"
        exit = f"{RED}X{RESET}"
        path = f"{BLUE}■{RESET}"
        cell_close = f"{MAGENTA}█{RESET}"
        bar = f"{BRIGHT_WHITE}│{RESET}"
        if change_color:
            entry = f"{BRIGHT_RED}E{RESET}"
            exit = f"{MAGENTA}X{RESET}"
            path = f"{BRIGHT_RED}■{RESET}"
            cell_close = f"{BRIGHT_YELLOW}█{RESET}"
            bar = f"{BRIGHT_GREEN}│{RESET}"
        line = ""
        for cell in row:
            line += bar if cell.direction["W"] else " "
            if cell.entry:
                body = " " * left_pad + entry + " " * right_pad
            elif cell.exit:
                body = " " * left_pad + exit + " " * right_pad
            elif (cell.x, cell.y) in path_coords and show_path:
                body = " " * left_pad + path + " " * right_pad
            elif cell.closed:
                body = cell_close * CELL_WIDTH
            else:
                body = " " * CELL_WIDTH

            line += body

        line += bar if row[-1].direction["E"] else " "
        return line

    def lower_line(self, row: list[Cell],
                   change_color: bool = False) -> str:
        """Ultima linha do labirinto (paredes S), terminando em └ ┴ ┘."""
        n = len(row)
        wall = "─" * CELL_WIDTH
        gap = " " * CELL_WIDTH
        if not change_color:
            line = ""
            for i in range(n + 1):
                left = i > 0 and row[i - 1].direction["S"]
                right = i < n and row[i].direction["S"]
                up = ((i > 0 and row[i - 1].direction["E"])
                      or (i < n and row[i].direction["W"]))
                line += f"{BRIGHT_WHITE}{CORNERS[(up, False, left, right)]}{RESET}"
                if i < n:
                    line += (f"{BRIGHT_WHITE}{wall}{RESET}"
                             if row[i].direction["S"]
                             else f"{BRIGHT_WHITE}{gap}{RESET}")
            return line
        line = ""
        for i in range(n + 1):
            left = i > 0 and row[i - 1].direction["S"]
            right = i < n and row[i].direction["S"]
            up = ((i > 0 and row[i - 1].direction["E"])
                  or (i < n and row[i].direction["W"]))
            line += f"{BRIGHT_GREEN}{CORNERS[(up, False, left, right)]}{RESET}"
            if i < n:
                line += (f"{BRIGHT_GREEN}{wall}{RESET}"
                         if row[i].direction["S"]
                         else f"{BRIGHT_GREEN}{gap}{RESET}")
        return line