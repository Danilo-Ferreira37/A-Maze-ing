import random


class Cell:
    def __init__(self, y: int, x: int, y_len: int, x_len: int) -> None:
        self.direction = {
                     "N": 1,
                     "E": 1,
                     "S": 1,
                     "W": 1}
        self.maze_limit = {
                     "N": 0,
                     "E": 0,
                     "S": 0,
                     "W": 0}
        self.x = x
        self.y = y
        self.visited = False
        self.entry = False
        self.exit = False
        self.closed = False
        if y == 0:
            self.maze_limit["N"] = 1
        if y == y_len - 1:
            self.maze_limit["S"] = 1
        if x == 0:
            self.maze_limit["W"] = 1
        if x == x_len - 1:
            self.maze_limit["E"] = 1

    def __repr__(self) -> str:
        return f"C({self.x},{self.y})"


class Maze:
    def __init__(self, height: int, width: int, entry: tuple[int, int],
                 exit: tuple[int, int], output_file: str,
                 perfect: bool) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.grid_creator()
        self.fourty_two()
        if perfect:
            self.dfs_backtracing(self.entry[0], self.entry[1])
        else:
            self.dfs_backtracing(self.entry[0], self.entry[1], False)
        self.output_hex()

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

        probably = 0.03
        if self.height < 15 or self.width < 15:
            probably = 0.15
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
