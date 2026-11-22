from parsing.config_parser import ConfigParser
from output.iterativity import iterativity, create_maze
from parsing.model import MazeConfig
import sys
import os


def main() -> None:
    try:
        os.system("clear")
        config_parser = ConfigParser(sys.argv[1])
        config: MazeConfig = config_parser.parse()
    except IndexError:
        print("ERROR: The program has to be executes: "
              "'python3 a_maze_ing.py config.txt'")
        exit(1)
    display, config = create_maze(config)
    iterativity(display, config)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nUser kill the program with EOF")
        exit(1)
