"""Sudoku Valid Boards Generator - 2017
(slightly modified in November, 2020)

This module is using a recursive depth-first search approach
to generate every valid board from a starting template.
"""

__author__ = 'Anderson Freixo <anderson.freixo@gmail.com>'
__credits__ = '''Contributors:
 * Mathias Ettinger (https://codereview.stackexchange.com/users/84718/mathias-ettinger)
'''

import copy
import itertools


# List of indices (line, column) for each cell in each
# 3×3 block of a sudoku grid.
BLOCKS = [
    list(itertools.product(
        range(3*n, 3*(n+1)),
        range(3*m, 3*(m+1)),
    )) for n, m in itertools.product(range(3), repeat=2)
]

def is_valid(num, board, line, column):
    """Test if the given number lies in the given line, column or block"""
    return not (is_in_line(num, board, line) or
            is_in_column(num, board, column) or
            is_in_block(num, board, line, column))


def is_in_line(num, board, line):
    """Test if the given number lies in the given line of the given board"""
    return num in board[line]


def is_in_column(num, board, column):
    """Test if the given number lies in the given column of the given board"""
    for line in board:
        if line[column] == num:
            return True
    return False


def is_in_block(num, board, line, column):
    """Test if the given number lies in the given block of the given board"""
    for l, c in find_block(line, column):
        if board[l][c] == num:
            return True
    return False

def find_block(line, column):
    """Retrieve the block which contain the cell at the given line and column"""
    cell = (line, column)
    for block in BLOCKS:
        if cell in block:
            return block


def initialize(board):
    """Ensure a board has at least 9 lines and 9 columns"""
    # Copy the parameter in order to not update it in place
    board = copy.deepcopy(board)
    while len(board) < 9:
        board.append([None] * 9)

    for line in board:
        line.extend([None] * (9 - len(line)))

    return board


def search(board):
    """Generate all valid solutions that can fit in the given board"""

    def _search_helper(board, line, column):
        """Recursivelly try all number for the cell at the
        given line and column and generate the solution if
        the grid has been filled.
        """

        if (line, column) == (9, 0):
            # Reached the end of the recursion so
            # this board must be complete.
            yield copy.deepcopy(board)
            return

        new_column = (column + 1) % 9
        new_line = line if new_column else line + 1
        if board[line][column]:
            # Skip cells that already have a number before the search
            yield from _search_helper(board, new_line, new_column)
            return

        for number in range(1, 10):
            if is_in_line(number, board, line):
                continue
            if is_in_column(number, board, column):
                continue
            if is_in_block(number, board, line, column):
                continue

            board[line][column] = number
            yield from _search_helper(board, new_line, new_column)
            # Reset cell so this number doesn't interact
            # with subsequent recursive searches
            board[line][column] = None

    yield from _search_helper(initialize(board), 0, 0)


if __name__ == '__main__':

    from pprint import pprint

    # Solve a given grid
    grid = [
            [3, 4, 0, 8, 2, 6, 0, 7, 1],
            [0, 0, 8, 0, 0, 0, 9, 0, 0],
            [7, 6, 0, 0, 9, 0, 0, 4, 3],
            [0, 8, 0, 1, 0, 2, 0, 3, 0],
            [0, 3, 0, 0, 0, 0, 0, 9, 0],
            [0, 7, 0, 9, 0, 4, 0, 1, 0],
            [8, 2, 0, 0, 4, 0, 0, 5, 9],
            [0, 0, 7, 0, 0, 0, 3, 0, 0],
            [4, 1, 0, 3, 8, 9, 0, 6, 2],
    ]
    for i, solution in enumerate(search(grid)):
        print('Solution n°{}:'.format(i))
        pprint(solution)
