from enum import Enum, auto


class CellState(Enum):
    EMPTY = auto()
    LOCKED = auto()
    FILLED_IN = auto()
