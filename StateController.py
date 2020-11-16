"""
StateController class to manage the state of the sudoku board and provide
utility functions
"""

import SudokuSolver as ss

class StateController():
    """Manages the board and stores the current state of the app"""
    def __init__(self):
        self.state = "stop"
        self.board = []
        self.solution_iter = None
        self.current_solution = None
        self.init_board()

    def set_state(self, state):
        state = state.lower()
        if state == "stop":
            self.state = "stop"
        elif state == "run":
            self.state = "run"
        else:
            print(state + "is not a valid state.")

    def get_state(self):
        return self.state

    def init_board(self):
        """Creates the rows and columns of the board
        and set all squares to 0"""
        for rows in range(9):
            row = []
            for col in range(9):
                row.append(0)
            self.board.append(row)

    def reset_board(self):
        """Zero all squares"""
        self.board = []
        self.init_board()

    def init_solution_iter(self):
        self.solution_iter = ss.search(self.board)

    def get_next_solution(self):
        if self.solution_iter:
            self.current_solution = next(self.solution_iter, None)
        else:
            self.current_solution = None
        return self.current_solution

    def load_board_from_file(self, bf):
        self.board = []
        for line in bf:
            line = line.strip()
            line = line.replace(" ", "")
            line_num = []
            for number in line:
                line_num.append(int(number))
            self.board.append(list(line_num))
        bf.close()

    def save_board_to_file(self, bf):
        for row in self.board:
            str_row = ""
            for col in row:
                str_row += str(col)
            str_row+="\n"
            bf.write(str_row)
        bf.close()

    def save_solution_to_file(self, bf):
        for row in self.current_solution:
            str_row = ""
            for col in row:
                str_row += str(col)
            str_row+="\n"
            bf.write(str_row)
        bf.close()

    def check_board_consistency(self):
        """Return a list of all squares that conflict with other squares"""
        irregular = []
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if num != 0:
                    self.board[row][col] = 0
                    if not ss.is_valid(num, self.board, row, col):
                        irregular.append((row, col))
                    self.board[row][col] = num
        return irregular
