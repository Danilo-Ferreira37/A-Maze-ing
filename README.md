*This project has been created as part of the 42 curriculum by dosorio-.*

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Build](https://img.shields.io/badge/Build-Makefile-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green)
![Typing](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet)
![Algorithms](https://img.shields.io/badge/Algorithms-DFS%20%7C%20BFS-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)
![Language](https://img.shields.io/badge/Language-Python-blue)

# Description

---

This project implements a fully configurable **maze generator and solver**, capable of producing valid mazes based on a user-defined configuration file. The program reads the configuration, validates all parameters, generates the maze, solves it, displays it in the terminal and writes the result to an output file.

After the maze is displayed, an **interactive menu** lets the user regenerate the maze, show or hide the solution, change the colors and switch between two visual styles (Dropbox and ASCII).

The focus is on **procedural generation**, **clean modular design**, and **reusable components**.

# Features

- Configurable maze generation (size, entry, exit, perfect / imperfect)
- Randomized generation, with a **seed** that can be fixed to reproduce a maze
- Shortest-path solving using BFS
- Two terminal rendering styles:
  - **Dropbox** — box-drawing characters (`┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼`)
  - **ASCII** — plain characters (`+ - |`)
- Colored terminal output with two themes (Normal and Watermelon)
- Interactive menu to control the maze while the program runs
- Output file containing the maze and the solution directions

---

# Display Styles

## Dropbox style

Walls are drawn with box-drawing characters, and every cell is 4 characters wide.
Blocked (closed) cells are filled with `█` and the solution path is drawn with `■`.

```
┌──────────────┐
│ E    ■     ■ │
│    ╶────┐    │
│         │ X  │
└─────────┴────┘
```

## ASCII style

Walls are drawn with `+`, `-` and `|`. In the terminal, blocked cells and the solution path are drawn with a colored background (the path is shown as `*` below for illustration).

```
+---+---+---+
| E   *   * |
+   +---+   +
|       | X |
+---+---+---+
```

Legend: `E` — entry, `X` — exit.

---

# Instructions

## Installation

The project uses a **Python virtual environment** managed through a Makefile.

To install all dependencies and prepare the environment, run:

```
make install
```

This will:
- Create a virtual environment (`venv/`) if it does not exist  
- Upgrade `pip`  
- Install development tools:
  - `flake8`
  - `mypy`

> Note: The project has no external runtime dependencies.

---

## Running the Program

To generate and solve a maze using the default configuration file:

```
make run
```

This executes:

```
python3 a_maze_ing.py config.txt
```

## Debug Mode

To run the program using the Python debugger:

```
make debug
```

## Cleaning Temporary Files

To remove caches and temporary Python files:

```
make clean
```

This deletes:
- `__pycache__/`
- `.mypy_cache/`
- `.pyc` files

## Linting and Static Analysis

To check code style (flake8) and typing (mypy):

```
make lint
```

To run strict linting and typing rules:

```
make lint-strict
```

---

# Interactive Menu

After the maze is displayed, the program shows a menu and waits for a choice:

| Option | Action |
|--------|--------|
| `1` | Re-generate a new maze (new random seed) |
| `2` | Show / hide the path from entry to exit |
| `3` | Rotate the maze colors (Normal / Watermelon) |
| `4` | Switch the maze style (Dropbox / ASCII) |
| `5` | Hide / show the info panel |
| `6` | Quit |

The info panel shows the maze height and width, the entry and exit coordinates, the maze type (perfect or imperfect), the seed, the current maze style and the current color theme.

Any other input prints an error message and the maze is displayed again.

---

# Config File Structure

The configuration file must follow this format:

```
WIDTH=<int>
HEIGHT=<int>
ENTRY=x,y
EXIT=x,y
OUTPUT_FILE=string.txt
PERFECT=bool
SEED=<int>        (optional)
```
## Example

```
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=output.txt
PERFECT=True
```

### Field descriptions

- **WIDTH / HEIGHT** — Maze dimensions
- **ENTRY** — Starting position
- **EXIT** — Ending position
- **OUTPUT_FILE** — File where the maze data is saved, including:
  - Maze representation in hexadecimal
  - Solution path (N, S, E, W)
  - Entry coordinates
  - Exit coordinates
- **PERFECT** — If True, the maze has no cycles (only one unique path between any two points)
- **SEED** — Optional. Seed of the random generator; using the same seed reproduces the same maze. If it is missing, a random seed is generated, and it is always shown in the info panel.

---

# Output Format

The output file contains:

- Maze representation in hexadecimal format  
- Entry coordinates  
- Exit coordinates  
- Solution path as a sequence of directions  

## Directions

- N → North
- S → South
- E → East
- W → West

## Example

```
NSESEW
```

This represents the shortest path from ENTRY to EXIT.

---

# Maze Generation Algorithm

## Depth‑First Search (DFS) Backtracking

DFS Backtracking was chosen as the maze generation algorithm.

### Summary of the method
- Select an initial cell  
- Mark it as visited  
- Choose a random unvisited neighbor  
- Remove the wall between both cells  
- Move to the neighbor and repeat  
- Backtrack when no neighbors remain

### Why DFS

- Simple and intuitive  
- Produces long, interesting paths  
- Low computational cost  
- Easy to implement and adapt  

---

# Maze Solving Algorithm

## Breadth‑First Search (BFS)

BFS was used to solve the maze by finding the shortest possible path from the entry to the exit.

### How it works

- Starts from ENTRY  
- Explores neighbors level by level  
- Stores predecessors  
- Stops when EXIT is found  
- Reconstructs shortest path   

### Why BFS was chosen

- Guarantees shortest path  
- Efficient for grid-based problems  
- Deterministic and reliable  

---

# Algorithm Complexity

- DFS (Generation): **O(N)**  
- BFS (Solving): **O(V + E)**  

Both scale linearly with the number of cells.

---

# Project Structure

```
mazegen/
    mazegen.py              # MazeGenerator (DFS generation)
    solve_maze.py           # SolveMaze (BFS solving, solution file)
    cell.py                 # Cell (walls, entry, exit, closed)

parsing/
    config_parser.py        # Reads and validates the config file
    model.py                # MazeConfig definition

output/
    colors.py               # ANSI color constants
    display_ascii_maze.py   # DisplayMazeAscii  (+ - |)
    display_dropbox_maze.py # DisplayMazeDropBox (box-drawing characters)
    iterativity.py          # Interactive menu and maze creation

a_maze_ing.py               # Program entry point
Makefile
config.txt
```

---

# Reusable Code

## mazegen
- The `MazeGenerator` class, which generates the maze, the `SolveMaze` class, which solves it (and writes the solution), and the `Cell` class, which represents a cell.

```python
from mazegen import MazeGenerator, SolveMaze

maze = MazeGenerator(config)
solver = SolveMaze(maze, config)
directions = solver.solve_maze()   # e.g. ["E", "E", "S"]
```

The display classes in `output/` are independent of the algorithms: both `DisplayMazeAscii` and `DisplayMazeDropBox` receive a `MazeGenerator` and a `SolveMaze`, so a new rendering style only needs a new class with the same `display(show_path, change_color)` method.

### How to reuse the code?
- **Install the build if you hasn't installed with:**  
pip install build  

- **Then executes the build:**  
python3 -m build

- **The build will make two files:**   
mazegen-1.0.0.tar.gz and mazegen-1.0.0-py3-none-any.whl

- **To install the mazegen module enter:**  
pip install mazegen-1.0.0-py3-none-any.whl

- **And to extract(view) the module files enter:**  
tar -xzf mazegen-1.0.0.tar.gz 

# Testing

The project was manually tested to ensure:
- Invalid configurations  
- Boundary conditions  
- Different maze sizes  
- Entry/Exit edge cases  
- Both display styles and both color themes  

Frameworks like `pytest` can be used but are not included.

---

# .gitignore

The project includes a `.gitignore` file excluding:

- `venv/`  
- `__pycache__/`  
- `*.pyc`  
- `.mypy_cache/`  


# Resources

## References

- Red Blob Games — Maze generation algorithms  
- DFS, BFS, and backtracking articles  

## Use of AI

AI was used strictly as an auxiliary tool for:
- Improving technical explanations  
- Generating documentation examples  
- Suggesting modular organization  
- Reviewing the README text  

All code was written manually.
