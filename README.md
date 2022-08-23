# sudoku-solver-visualization
Sudoku game with auto-solving visualization

To run this application, simply run main.py, make sure you have Tkinter and Pygame installed.

In the Pygame window, to automatically solve the board, or to check your solution, press the space bar.
To edit a cell's value, click on it and type in the new value, or backspace to clear it.

The term "size" refers to the number of boxes per row/column in the board.

How this works:
- A random board is generated from an external source, using web scraping
- The board is displayed in a Pygame GUI
- A backtracking algorithim is used to automatically solve the board
