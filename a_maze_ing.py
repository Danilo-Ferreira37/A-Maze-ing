from parsing.config_parser import ConfigParser
from output.iterativity import iterativity, create_maze
from parsing.model import MazeConfig
from output.display_dropbox_maze import DisplayMazeDropBox
import sys
import os
from output.colors import BRIGHT_BLUE, YELLOW, BRIGHT_RED


def main() -> None:
    try:
        os.system("clear")
        config_parser = ConfigParser(sys.argv[1])
        config: MazeConfig = config_parser.parse()
    except IndexError:
        print("ERROR: The program has to be executes: "
              "'python3 a_maze_ing.py config.txt'")
        exit(1)
    display, config = create_maze(config, DisplayMazeDropBox)
    iterativity(display, config)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print(f"{BRIGHT_BLUE}User exited the program!")
        exit(0)
    except (EOFError, KeyboardInterrupt):
        print(f"{YELLOW}\nUser kill the program with EOF")
        exit(1)
    except BaseException:
        print(f"{BRIGHT_RED}Fatal error!")
        exit(1)
