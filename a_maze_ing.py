from parsing.config_parser import ConfigParser
from maze.generator import Maze
from maze.solver import solve_maze, write_solution
from output.display import Display_Maze
import sys
import os


def main(color: bool = False) -> None:
    try:
        config_parser = ConfigParser(sys.argv[1])
        config = config_parser.parse()
    except IndexError:
        print("ERROR: The program has to be executes: "
              "'python3 a_maze_ing.py config.txt'")
        exit(1)
    maze = Maze(
        config["HEIGHT"],
        config["WIDTH"],
        config["ENTRY"],
        config["EXIT"],
        config["OUTPUT_FILE"],
        config["PERFECT"]
    )

    display = Display_Maze(
        maze,
        lambda m: solve_maze(m, config)
    )

    display.display(False, color)
    write_solution(maze)
    show_hide = 2
    path = False
    while (1):
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        if choice not in ("1", "2", "3", "4"):
            os.system("clear")
            display.display(path, color)
            print("\nError: Enter a number between 1 and 4!\n")

        elif choice == "1":
            main(color)
        elif choice == "2":
            if show_hide % 2 != 0 and not color:
                path = False
                display.display(path, color)
            elif show_hide % 2 != 0 and color:
                path = False
                display.display(path, color)
            else:
                if color:
                    path = True
                    display.display(path, color)
                else:
                    path = True
                    display.display(path, color)
            show_hide += 1
        elif choice == "3":
            if not color:
                color = True
            elif color:
                color = False
            display.display(path, color)
        elif choice == "4":
            exit(0)


if __name__ == "__main__":
    main()
