from output.display_ascii_maze import (BRIGHT_GREEN, BRIGHT_YELLOW,
                                       BRIGHT_RED, RESET)
from parsing.model import MazeConfig
import os
from mazegen import MazeGenerator, SolveMaze
from output.display_ascii_maze import Display_Maze
from output.display_dropbox_maze import DisplayMazeDropBox

import random


def create_maze(
        config: MazeConfig,
        color: bool = False, replace_maze: bool = False
        ) -> tuple[Display_Maze, MazeConfig]:
    if not config.get("SEED") or replace_maze:
        config["SEED"] = random.randrange(2**32)
    maze = MazeGenerator(config)
    sv = SolveMaze(maze, config)
    display = DisplayMazeDropBox(
        maze,
        sv.solve_maze,
    )
    display.display(False, color)
    sv.write_solution()
    return display, config


def iterativity(display: Display_Maze, config: MazeConfig) -> None:
    show_hide = 2
    path = False
    color = False
    while True:
        watermelon = f"{BRIGHT_RED}Watermelon{BRIGHT_GREEN}"
        theme = ""
        if color:
            theme = BRIGHT_GREEN
        print(f"{theme}╔═════════════════ Manual ══════════════════╗")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit\n")
        print("╔═════════════════ Status ══════════════════╗")
        print(f"  ==== Height: {config['HEIGHT']}, Width: {config['WIDTH']}")
        print(f"  ==== Entry: x({config['ENTRY'][0]}), y({config['ENTRY'][1]}"
              f") ││ Exit: x({config['EXIT'][0]}), y({config['EXIT'][1]})")
        print(f"  ==== Maze type: "
              f"{'Perfect Maze' if config['PERFECT'] else 'Imperfect Maze'}")
        print(f"  ==== Seed: {config['SEED']}")
        print(f"  ==== Current Theme: {watermelon if color else 'Normal'}")

        print("╚═══════════════════════════════════════════╝")
        choice = input("Choice? (1-4): ")
        if choice not in ("1", "2", "3", "4"):
            os.system("clear")
            display.display(path, color)
            print(f"{BRIGHT_YELLOW}\nError: Enter a number "
                  f"between 1 and 4!\n{RESET}")

        elif choice == "1":
            os.system("clear")
            create_maze(config, color=color, replace_maze=True)
        elif choice == "2":
            os.system("clear")
            if show_hide % 2 != 0:
                path = False
                display.display(path, color)
            else:
                path = True
                display.display(path, color)
            show_hide += 1
        elif choice == "3":
            os.system("clear")
            color = not color
            display.display(path, color)
        elif choice == "4":
            exit(0)
