from collections.abc import Callable

from mazegen import MazeGenerator
from mazegen.cell import Cell

RESET = "\033[0m"

# Temas: cores das paredes, entrada, saida, caminho e celulas fechadas
THEMES: dict[str, dict[str, str]] = {
    "default": {
        "wall": "\033[97m",
        "entry": "\033[32m",
        "exit": "\033[31m",
        "path": "\033[44m",
        "closed": "\033[45m",
    },
    "alt": {
        "wall": "\033[92m",
        "entry": "\033[91m",
        "exit": "\033[35m",
        "path": "\033[101m",
        "closed": "\033[103m",
    },
}

# (up, down, left, right) -> caracter box-drawing
JUNCTIONS: dict[tuple[bool, bool, bool, bool], str] = {
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


class DisplayMazeBox:
    """Desenha o labirinto com caracteres box-drawing (┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼)."""

    def __init__(
        self,
        maze: MazeGenerator,
        solver: Callable[[], list[str]],
    ) -> None:
        self.maze = maze
        self.solver = solver

    # ------------------------------------------------------------------ path
    def build_path_coords(self, directions: list[str]) -> set[tuple[int, int]]:
        x, y = self.maze.entry
        path: list[tuple[int, int]] = [(x, y)]
        moves = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        for d in directions:
            dx, dy = moves[d]
            x, y = x + dx, y + dy
            path.append((x, y))
        return set(path)

    # ----------------------------------------------------------------- walls
    def _h_wall(self, vy: int, cx: int) -> bool:
        """Parede horizontal na linha de vertices vy, acima/abaixo da coluna cx."""
        grid = self.maze.grid
        h = len(grid)
        below = grid[vy][cx].direction["N"] if vy < h else False
        above = grid[vy - 1][cx].direction["S"] if vy > 0 else False
        return below or above

    def _v_wall(self, cy: int, vx: int) -> bool:
        """Parede vertical na coluna de vertices vx, ao lado da linha cy."""
        row = self.maze.grid[cy]
        w = len(row)
        right = row[vx].direction["W"] if vx < w else False
        left = row[vx - 1].direction["E"] if vx > 0 else False
        return right or left

    def _junction(self, vy: int, vx: int) -> str:
        h = len(self.maze.grid)
        w = len(self.maze.grid[0])
        up = vy > 0 and self._v_wall(vy - 1, vx)
        down = vy < h and self._v_wall(vy, vx)
        left = vx > 0 and self._h_wall(vy, vx - 1)
        right = vx < w and self._h_wall(vy, vx)
        return JUNCTIONS[(up, down, left, right)]

    # ----------------------------------------------------------------- lines
    def horizontal_line(self, vy: int, theme: dict[str, str]) -> str:
        w = len(self.maze.grid[0])
        wall = theme["wall"]
        line = ""
        for vx in range(w + 1):
            line += self._junction(vy, vx)
            if vx < w:
                line += "───" if self._h_wall(vy, vx) else "   "
        return f"{wall}{line}{RESET}"

    def cell_line(
        self,
        cy: int,
        row: list[Cell],
        path_coords: set[tuple[int, int]],
        show_path: bool,
        theme: dict[str, str],
    ) -> str:
        wall = f"{theme['wall']}│{RESET}"
        line = ""
        for cx, cell in enumerate(row):
            line += wall if self._v_wall(cy, cx) else " "
            if cell.entry:
                body = f" {theme['entry']}E{RESET} "
            elif cell.exit:
                body = f" {theme['exit']}X{RESET} "
            elif show_path and (cell.x, cell.y) in path_coords:
                body = f"{theme['path']}   {RESET}"
            elif cell.closed:
                body = f"{theme['closed']}   {RESET}"
            else:
                body = "   "
            line += body
        line += wall if self._v_wall(cy, len(row)) else " "
        return line

    # --------------------------------------------------------------- display
    def display(self, show_path: bool = False,
                change_color: bool = False) -> None:
        theme = THEMES["alt" if change_color else "default"]
        path_coords = (
            self.build_path_coords(self.solver()) if show_path else set()
        )
        grid = self.maze.grid
        for cy, row in enumerate(grid):
            print(self.horizontal_line(cy, theme))
            print(self.cell_line(cy, row, path_coords, show_path, theme))
        print(self.horizontal_line(len(grid), theme))