from get_sudoku import get_sudoku
from display import Display
from cell_state import CellState
import pygame
from solver import Solver
import tkinter
from tkinter import messagebox


def main() -> None:
    """Setup a sudoku board and handle events on the board"""
    tkinter.Tk().withdraw()
    size = ''
    MIN_SIZE, MAX_SIZE = 2, 3
    while not size.isdigit() or int(size) < MIN_SIZE or int(size) > MAX_SIZE:
        size = (input(
            f'Enter a board size in the range [{MIN_SIZE}, {MAX_SIZE}]: ')
            .strip())

    sudoku_link = f'http://www.menneske.no/sudoku/{size}/eng/random.html'
    sudoku = get_sudoku(sudoku_link)

    # state of each cell in the board
    sudoku_state = [[CellState.LOCKED if val else CellState.EMPTY
                     for val in row] for row in sudoku]

    solution = Solver(sudoku, lambda *args: None).solve()
    CORRECT_SOLUTION_MESSAGE = 'Board successfully solved!'
    INCORRECT_SOLUTION_MESSAGE = 'Some cell(s) contain incorrect values.'

    KEYS = {
        pygame.K_0: 0, pygame.K_KP0: 0,
        pygame.K_BACKSPACE: 0, pygame.K_DELETE: 0,
        pygame.K_1: 1, pygame.K_KP1: 1,
        pygame.K_2: 2, pygame.K_KP2: 2,
        pygame.K_3: 3, pygame.K_KP3: 3,
        pygame.K_4: 4, pygame.K_KP4: 4,
        pygame.K_5: 5, pygame.K_KP5: 5,
        pygame.K_6: 6, pygame.K_KP6: 6,
        pygame.K_7: 7, pygame.K_KP7: 7,
        pygame.K_8: 8, pygame.K_KP8: 8,
        pygame.K_9: 9, pygame.K_KP9: 9
    }

    selected_i = selected_j = None
    display = Display(int(size), 1300, 800)
    display.draw_sudoku(sudoku, sudoku_state)

    def update_selected(highlighted: bool) -> None:
        """Highlight or unhighlight the selected cell

        Args:
            highlighted (bool): highlight if true, unhighlight is false
        """
        display.draw_cell_and_update(selected_i, selected_j,
                                     sudoku[selected_i][selected_j],
                                     sudoku_state[selected_i][selected_j],
                                     highlighted)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                new_i, new_j = display.get_cell(x, y)

                # if selection is invalid
                if (new_i is None or
                        sudoku_state[new_i][new_j] == CellState.LOCKED):
                    continue

                if selected_i is not None:
                    update_selected(False)

                selected_i, selected_j = new_i, new_j
                update_selected(True)
                continue

            elif event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_SPACE:
                # if any user entered values are incorrect
                if any(sudoku_val and sudoku_val != solution_val
                       for rows in zip(sudoku, solution)
                       for sudoku_val, solution_val in zip(*rows)):
                    messagebox.showerror(Display.get_title(),
                                         INCORRECT_SOLUTION_MESSAGE)
                    continue

                sudoku = Solver(sudoku, display.draw_cell_and_update).solve()
                for i, row in enumerate(sudoku_state):
                    for j, state in enumerate(row):
                        if state == CellState.EMPTY:
                            sudoku_state[i][j] = CellState.FILLED_IN

                messagebox.showinfo(Display.get_title(),
                                    CORRECT_SOLUTION_MESSAGE)

            # if any cell is selected and user pressed a key to update the cell
            elif selected_i is not None and event.key in KEYS:
                val = KEYS[event.key]
                sudoku[selected_i][selected_j] = val
                state = CellState.FILLED_IN if val else CellState.EMPTY
                sudoku_state[selected_i][selected_j] = state
                update_selected(True)


if __name__ == '__main__':
    main()
