from output.colors import (BRIGHT_GREEN, BRIGHT_YELLOW,
                           BRIGHT_RED, RESET, BLUE)
from parsing.model import MazeConfig
import os
from mazegen import MazeGenerator, SolveMaze
from output.display_ascii_maze import DisplayMazeAscii
from output.display_dropbox_maze import DisplayMazeDropBox
import random


def create_maze(
        config: MazeConfig,
        cls_display: type[DisplayMazeAscii] | type[DisplayMazeDropBox],
        replace_maze: bool = False,
) -> tuple[DisplayMazeAscii | DisplayMazeDropBox, MazeConfig]:
    if not config.get("SEED") or replace_maze:
        config["SEED"] = random.randrange(2**32)
    maze = MazeGenerator(config)
    sv = SolveMaze(maze, config)
    display = cls_display(maze, sv)
    sv.write_solution()
    return display, config


def print_info(
        config: MazeConfig,
        color: bool,
        display: DisplayMazeAscii | DisplayMazeDropBox
) -> None:
    watermelon = f"{BRIGHT_RED}Watermelon{BRIGHT_GREEN}"
    theme = ""
    if color:
        theme = BRIGHT_GREEN
    print(f"\n\n{theme}╔═════════════════ Manual ═══════════════════════╗")
    print("  1. Re-generate a new maze.")
    print("  2. Show/Hide path from entry to exit.")
    print("  3. Rotate maze colors.")
    print("  4. Switch maze style (Dropbox / ASCII).")
    print("  5. Hide/Show info.")
    print("  6. Quit.\n\n")
    print("╔═════════════════ Status ═══════════════════════╗")
    print(f"  ==== Height: {config['HEIGHT']}, Width: {config['WIDTH']}")
    print(f"  ==== Entry: X: {config['ENTRY'][0]}, Y: {config['ENTRY'][1]}"
          f" ││ Exit: X: {config['EXIT'][0]}, Y: {config['EXIT'][1]}")
    print(f"  ==== Maze type: "
          f"{'Perfect Maze' if config['PERFECT'] else 'Imperfect Maze'}")
    print(f"  ==== Seed: {config['SEED']}")
    maze = 'ASCII' if display.__class__ is DisplayMazeAscii else 'DropBox'
    print(f"  ==== Maze style: "
          f"{maze}")
    print(f"  ==== Current Theme: {watermelon if color else 'Normal'}")
    print("╚════════════════════════════════════════════════╝\n")


def iterativity(
        display: DisplayMazeAscii | DisplayMazeDropBox,
        config: MazeConfig) -> None:
    path = False
    show_info = True
    color = False
    display.display(path, color)
    while True:
        if show_info:
            print_info(config, color, display)
        else:
            print(f"{BRIGHT_YELLOW}Info hidden. "
                  f"Press 5 to show it again.{RESET}")
        choice = input(f"{BLUE}Choice? (1-6): {RESET}")
        if choice not in ("1", "2", "3", "4", "5", "6"):
            os.system("clear")
            display.display(path, color)
            print(f"{BRIGHT_YELLOW}\nError: Enter a number "
                  f"between 1 and 6!\n{RESET}")
        elif choice == "1":
            os.system("clear")
            path = False
            display, config = create_maze(config, display.__class__,
                                          replace_maze=True)
            display.display(path, color)
        elif choice == "2":
            os.system("clear")
            path = not path
            display.display(path, color)
        elif choice == "3":
            os.system("clear")
            color = not color
            display.display(path, color)
        elif choice == "4":
            os.system("clear")
            cls = (DisplayMazeDropBox
                   if display.__class__ == DisplayMazeAscii
                   else DisplayMazeAscii)
            display, config = create_maze(config, cls)
            display.display(path, color)
        elif choice == "5":
            os.system("clear")
            show_info = not show_info
            display.display(path, color)
        elif choice == "6":
            exit(0)
