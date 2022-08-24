import math
from typing import Optional
import pygame
from cell_state import CellState


class Display:
    __BG_COLOR = 255, 255, 255
    __COLORS = {
        CellState.EMPTY: (255, 255, 255),
        CellState.LOCKED: (0, 0, 0),
        CellState.FILLED_IN: (255, 0, 0)
    }
    __PAD = 0.25
    __LINE_WIDTH = 1
    __THICK_LINE_WIDTH = 3
    __TITLE = 'Sudoku Solver Visualization'
    __DELAY = 50

    def __init__(self, sudoku_size: int,
                 window_width: int, window_height: int):
        """Initialize display object

        Args:
            sudoku_size (int): board size (number of boxes per row/column)
            window_width (int): width of display window
            window_height (int): height of display window
        """
        self.__sudoku_size = sudoku_size
        self.__row_len = sudoku_size * sudoku_size
        pygame.init()
        self.__surface = pygame.display.set_mode((window_width, window_height))
        self.__surface.fill(Display.__BG_COLOR)
        pygame.display.set_caption(Display.__TITLE)

        avg_line_width = (Display.__LINE_WIDTH * self.__row_len +
                          (Display.__THICK_LINE_WIDTH - Display.__LINE_WIDTH) *
                          (self.__sudoku_size + 1)) / self.__row_len

        # length of one side of a cell
        self.__cell_size = ((min(window_width, window_height) *
                            (1 - Display.__PAD) / self.__row_len)
                            - avg_line_width)

        self.__left_margin = (window_width - self.__cell_size *
                              self.__row_len) // 2
        self.__top_margin = (window_height - self.__cell_size *
                             self.__row_len) // 2

        self.__font = pygame.font.SysFont('comicsansms',
                                          math.floor(self.__cell_size / 3))

    @staticmethod
    def get_title() -> str:
        """Get window title

        Returns:
            str: window title
        """
        return Display.__TITLE

    def __draw_line(self, i: int, start: tuple[int, int],
                    end: tuple[int, int], highlighted: bool) -> None:
        """Draw line in the ith row/column from point start to end

        Args:
            i (int): row or column
            start (tuple[int, int]): starting point (x, y)
            end (tuple[int, int]): ending point (x, y)
            highlighted (bool): if line should be highlighted
        """
        pygame.draw.line(self.__surface,
                         Display.__COLORS[CellState.EMPTY], start,
                         end, width=Display.__THICK_LINE_WIDTH)

        if not highlighted and i % self.__sudoku_size:
            line_width = Display.__LINE_WIDTH
        else:
            line_width = Display.__THICK_LINE_WIDTH
        state = CellState.FILLED_IN if highlighted else CellState.LOCKED
        pygame.draw.line(self.__surface,
                         Display.__COLORS[state], start,
                         end, width=line_width)

    def __draw_box(self, i: int, j: int, highlighted: bool):
        """Draw a box around this cell

        Args:
            i (int): row
            j (int): column
            highlighted (bool): if box should be highlighted
        """
        left, top = self.__get_cell_coordinates(i, j)
        right, bottom = left + self.__cell_size, top + self.__cell_size
        self.__draw_line(i, (left, top), (right, top), highlighted)
        self.__draw_line(i + 1, (left, bottom), (right, bottom), highlighted)
        self.__draw_line(j, (left, top), (left, bottom), highlighted)
        self.__draw_line(j + 1, (right, top), (right, bottom), highlighted)

    def draw_sudoku(self, sudoku: list[list[int]],
                    sudoku_state: list[list[CellState]]) -> None:
        """Draw entire sudoku board

        Args:
            sudoku (list[list[int]]): sudoku board, 0 represents an empty cell
            sudoku_state (list[list[CellState]]): sudoku board state,
                                                  of the same size as sudoku
        """
        for i in range(self.__row_len):
            for j in range(self.__row_len):
                self.__draw_cell(i, j, sudoku[i][j], sudoku_state[i][j], False)

        pygame.display.update()

    def __get_cell_coordinates(self, i: int, j: int) -> tuple[int, int]:
        """Get the top left coordinates of this cell

        Args:
            i (int): row
            j (int): column

        Returns:
            tuple[int, int]: (x, y) coordinates of the top left of this cell
        """
        return (self.__left_margin + j*self.__cell_size,
                self.__top_margin + i*self.__cell_size)

    def get_cell(self, x: int, y: int) -> tuple[Optional[int], Optional[int]]:
        """Get the cell coordinates of this (x, y) coordinate

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            tuple[Optional[int], Optional[int]]: (row, col) or (None, None)
                                                 if (x, y) is not in any cell
        """
        print(x, y)
        i = math.floor((y - self.__top_margin) / self.__cell_size)
        j = math.floor((x - self.__left_margin) / self.__cell_size)
        if (i < 0 or i >= self.__row_len or
                j < 0 or j >= self.__row_len):
            return None, None
        return i, j

    def __draw_cell(self, i: int, j: int, val: int,
                    state: CellState, highlighted: bool) -> None:
        """Draw this cell

        Args:
            i (int): row
            j (int): column
            val (int): cell value
            state (CellState): cell state
            highlighted (bool): if cell should be highlighted
        """
        cell_x, cell_y = self.__get_cell_coordinates(i, j)

        # cover cell with background color
        pygame.draw.rect(self.__surface, Display.__BG_COLOR,
                         (cell_x, cell_y, self.__cell_size, self.__cell_size))

        self.__draw_box(i, j, highlighted)
        val = str(val) if val else ''
        text = self.__font.render(val, True,
                                  Display.__COLORS[state],
                                  Display.__BG_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (cell_x + self.__cell_size // 2,
                            cell_y + self.__cell_size // 2)
        self.__surface.blit(text, text_rect)

    def draw_cell_and_update(self, i: int, j: int, val: int,
                             state: CellState, highlighted: bool) -> None:
        """Draw this cell and update the display

        Args:
            i (int): row
            j (int): column
            val (int): cell value
            state (CellState): cell state
            highlighted (bool): if cell should be highlighted

        Raises:
            SystemExit: if user chooses to exit pygame window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
        pygame.time.wait(Display.__DELAY)
        self.__draw_cell(i, j, val, state, highlighted)
        pygame.display.update()
