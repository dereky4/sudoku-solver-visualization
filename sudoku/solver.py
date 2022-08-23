import math
from cell_state import CellState
from typing import Callable, Optional


class Solver:

    def __init__(self, sudoku: list[list[int]],
                 update_display_func: Callable[[int, int, CellState, bool],
                                               None]):
        """Initialize solver object

        Args:
            sudoku (list[list[int]]): sudoku board, 0 represents an empty cell
            update_display_func (Callable[[int, int, CellState, bool], None]):
            function to update the board display
        """
        self.__sudoku = [row[:] for row in sudoku]
        self.__update_display_func = update_display_func
        self.__row_len = len(sudoku)
        self.__size = round(math.sqrt(self.__row_len))

        self.__empty_cells = []
        self.__rows = [set() for _ in range(self.__row_len)]
        self.__cols = [set() for _ in range(self.__row_len)]
        self.__boxes = [set() for _ in range(self.__row_len)]

        for i, row in enumerate(sudoku):
            for j, val in enumerate(row):
                if val:
                    self.__update_cell(i, j, val)
                else:
                    self.__empty_cells.append((i, j))

    def solve(self) -> Optional[list[list[int]]]:
        """Solve the board

        Returns:
            Optional[list[list[int]]]: solved board if the board could be
                                       solved
        """
        if not self.__backtrack(0):
            return None
        return [row[:] for row in self.__sudoku]

    def __backtrack(self, empty_idx: int) -> bool:
        """Backtrack to solve the board

        Args:
            empty_idx (int): index of the first currently empty cell

        Returns:
            bool: if board was succesfully solved
        """
        if empty_idx == len(self.__empty_cells):
            return True

        i, j = self.__empty_cells[empty_idx]
        for val in range(1, self.__row_len + 1):
            if not self.__is_valid_placement(i, j, val):
                continue
            self.__update_cell(i, j, val)
            self.__update_display_func(i, j, val, CellState.FILLED_IN, False)
            if self.__backtrack(empty_idx + 1):
                return True
            self.__clear_cell(i, j)
            self.__update_display_func(i, j, 0, CellState.EMPTY, False)

        return False

    def __is_valid_placement(self, i: int, j: int, val: int) -> bool:
        """Check if val can be placed at this cell coordinate

        Args:
            i (int): row
            j (int): column
            val (int): val

        Returns:
            bool: if val can be placed at this cell coordinate
        """
        return (val not in self.__rows[i] and
                val not in self.__cols[j] and
                val not in self.__boxes[self.__get_box_number(i, j)])

    def __update_cell(self, i: int, j: int, val: int) -> None:
        """Set this cell to contain val

        Args:
            i (int): _row
            j (int): column
            val (int): val
        """
        self.__sudoku[i][j] = val
        self.__rows[i].add(val)
        self.__cols[j].add(val)
        self.__boxes[self.__get_box_number(i, j)].add(val)

    def __clear_cell(self, i: int, j: int) -> None:
        """Clear this cell

        Args:
            i (int): row
            j (int): column
        """
        val, self.__sudoku[i][j] = self.__sudoku[i][j], 0
        self.__rows[i].remove(val)
        self.__cols[j].remove(val)
        self.__boxes[self.__get_box_number(i, j)].remove(val)

    def __get_box_number(self, i: int, j: int) -> int:
        """Get the box number of this cell

        Args:
            i (int): row
            j (int): column

        Returns:
            int: box number
        """
        return i // self.__size + (j - j % self.__size)
