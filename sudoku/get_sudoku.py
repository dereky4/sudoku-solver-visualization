import requests
from bs4 import BeautifulSoup


def get_sudoku(sudoku_link: str) -> list[list[int]]:
    """Generate a random sudoku board

    Args:
        sudoku_link (str): webpage to fetch the board from

    Returns:
        list[list[int]]: sudoku board, 0 represents an empty cell
    """
    soup = BeautifulSoup(requests.get(sudoku_link).content, 'html.parser')
    rows = soup.find_all('tr', {'class': 'grid'})

    sudoku = []
    for row in rows:
        sudoku_row = []
        for cell in row.find_all('td'):
            sudoku_row.append(int(cell.text) if cell.text != '\xa0' else 0)
        sudoku.append(sudoku_row)
        if len(sudoku_row) == len(sudoku):  # to avoid loading multiple boards
            break

    return sudoku
