from typing import TypedDict


class MazeConfig(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    SEED: int
    OUTPUT_FILE: str
