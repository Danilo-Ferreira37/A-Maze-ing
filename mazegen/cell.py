class Cell:
    def __init__(
              self, y: int,
              x: int,
              y_len: int,
              x_len: int) -> None:
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
