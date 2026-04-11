*This project has been created as part of the 42 curriculum by dosorio-, rmendonca.*

# Description

This project implements a fully configurable **maze generator and solver**, capable of producing valid mazes based on a user‑defined configuration file. The program reads the configuration, validates all parameters, generates the maze, solves it, and outputs the result. The focus is on **procedural generation**, **clean modular design**, and **reusable components**.

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
- Install development tools (`flake8`, `mypy`)  

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

To run the program using the Python debugger (pdb):

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

To check code style and typing:

```
make lint
```

To run strict linting and typing rules:

```
make lint-strict
```

# Config File Structure

The configuration file must follow this exact structure:

```
WIDTH=<int>
HEIGHT=<int>
ENTRY=(x: int, y: int)
EXIT=(x: int, y: int)
OUTPUT_FILE="string.txt"
PERFECT=bool
```

### Field descriptions
- **WIDTH / HEIGHT** — Maze dimensions  
- **ENTRY** — Starting position  
- **EXIT** — Ending position  
- **OUTPUT_FILE** — File where the maze seed, solution path, and status will be saved  
- **PERFECT** — Indicates whether the maze must be perfect (no loops)  

# Maze Generation Algorithm

## Depth‑First Search (DFS) Backtracking

DFS Backtracking was chosen as the maze generation algorithm.

### Summary of the method
- Select an initial cell  
- Mark it as visited  
- Choose a random unvisited neighbor  
- Remove the wall between both cells  
- Move to the neighbor and repeat  
- When no neighbors remain, backtrack  

### Why this algorithm
- Simple and intuitive  
- Produces long, interesting paths  
- Low computational cost  
- Great for visualization and teaching algorithmic concepts  
- Flexible and easy to adapt  

# Maze Solving Algorithm

## Breadth‑First Search (BFS)

BFS was used to solve the maze by finding the shortest possible path from the entry to the exit.

### How BFS works in this project
- BFS starts at the entry cell and places it in a queue  
- It explores all reachable neighbors level by level  
- Each visited cell stores its predecessor  
- When the exit is reached, the algorithm reconstructs the shortest path  
- BFS guarantees the optimal solution in terms of number of steps  

### Why BFS was chosen
- Guarantees the shortest path  
- Simple and efficient using a queue  
- Works extremely well on grid‑based mazes  

# Reusable Code

### Configuration Parser
Reads key=value pairs, validates types and ranges, and can be reused in any project requiring simple configuration files.

### Grid Structure
Generic 2D matrix representation with boundary checks and cell manipulation utilities. Useful for games, simulations, and pathfinding algorithms.

### Randomization Module
Handles seeded pseudo‑random generation to ensure reproducibility.

### Logging System
Provides debug, info, and error messages. Easily reusable in other Python projects.

# Team and Project Management

## Team Members

### dosorio-
**Roles:**
- DFS algorithm implementation  
- Grid structure and cell manipulation  
- Terminal visualization  
- Documentation  
- Output file generation (maze seed, shortest path, status)  

### rmendonca
**Roles:**
- Configuration parser implementation  
- Terminal display  
- BFS algorithm implementation for maze solving  
- Project organization and structure  
- Flake8 compliance  

# Resources

## Classic references
- Red Blob Games — Maze generation algorithms  
- Articles on DFS, BFS, and backtracking  

## Use of AI in the project
AI was used strictly as an auxiliary tool for:
- Improving technical explanations  
- Generating documentation examples  
- Suggesting modular organization  
- Reviewing the README text  

No code was generated automatically; all implementation was done manually.
