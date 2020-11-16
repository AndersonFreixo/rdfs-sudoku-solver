"""A Graphical User Interface for my
Recursive Depth-First-Search Sudoku Solver algorithm using Tkinter"""

__author__ = 'Anderson Freixo <anderson.freixo@gmail.com>'

import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from StateController import *

class SudokuSquare():
    """Represents a square with its respective button widget
    and related functions."""
    def __init__(self, parent, position, state):
        self.button = tk.Button(parent, text = "0", fg = "grey")
        self.button.bind("<Button>", self.on_click)
        self.position = position
        self.state = state

    def inc(self):
        """Increments the value of the button by one or set
        it to 0 if its value is 9."""
        current = int(self.button["text"])
        current = (current+1) % 10
        self.button["text"] = str(current)
        row, col = self.position
        self.state.board[row][col] = current

    def dec(self):
        """Decrements the value of the button by one or set
        it to 9 if its value is 0."""
        current = int(self.button["text"])
        if current <= 0:
            current = 9
        else:
            current-=1
        self.button["text"] = str(current)
        row, col = self.position
        self.state.board[row][col] = current

    def on_click(self, event):
        """Button command callback function. Calls inc() or dec()
        depending on the mouse button."""
        #Do nothing if the search is running
        if self.state.get_state() != "run":
            self.button["fg"] = "blue"

            if event.num == 1:
                self.inc()

            elif event.num == 2 or event.num == 3:
                self.dec()


    def get_value(self):
        return int(self.button["text"])

class BoardView(tk.Frame):
    """Manages the button widgets"""
    def __init__(self, parent, state):
        super().__init__(parent)
        self.board_view = {}
        self.state = state
        self.init_board_buttons();

    def init_board_buttons(self):
        for row in range(9):
            for col in range(9):
                square = SudokuSquare(self, (row, col), self.state)

                square.button.grid(row=row, column=col)
                self.board_view[(row, col)] = square

    def change_square_setting(self, position, setting, value):
        self.board_view[position].button[setting] = value

    def update_view(self, solution = None):
        """Updates the values within the sudoku square buttons
        based on the solution found by the search or a loaded board.
        Values set by the user or loaded from file
        remain blue, and the values found by the search
        are set to red. If 'solution' == None, squares with 0 value
        in the board_controller are set to 0 in the view again."""

        for row in range(9):
            for col in range(9):
                board = self.state.board
                button = self.board_view[(row, col)].button

                #If the function was called with a solution argument
                #update the value and change its font to red.
                if solution:
                    if board[row][col] != solution[row][col]:
                        button["text"] = str(solution[row][col])
                        button["fg"] = "red"

                #Otherwise, paint values from 1 to 9 blue
                #and 0 values grey
                else:
                    number = board[row][col]
                    button["text"] = str(number)

                    if number == 0:
                        button["fg"] = "grey"
                    else:
                        button["fg"] = "blue"


    def reset_board_view(self):
        """Turns all square buttons to 0"""
        for row in range(9):
            for col in range(9):
                button = self.board_view[(row, col)].button
                button["text"] = "0"
                button["fg"] = "grey"

class HeaderView(tk.Frame):
    """Frame with labels containing information about the program"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title_label = tk.Label(
            self,
            text="DFS Sudoku Solver 1.0",
            font=("TkDefaultFont", 14),
            fg="blue"
            )

        self.author_label = tk.Label(
            self,
            text="Anderson S. Freixo <anderson.freixo@gmail.com>",
            font=("TkDefaultFont", 8),
            fg="blue"
            )
        self.title_label.grid(row=0, column=0, sticky=(tk.E+tk.W))
        self.author_label.grid(row=1, column=0, sticky=(tk.E+tk.W))


class Application(tk.Tk):
    """Main tkinter application"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Depth First Search Sudoku Solver")
        self.resizable(width=False, height=False)
        self.option_add('*font', 'Helvetica -12')

        self.state = StateController()

        self.board_view = BoardView(self, self.state)

        #####    Control pannel setup #########
        self.control_view = tk.Frame(self)

        self.run_button = tk.Button(
            self.control_view,
            text = "Run!",
            command = self.run
        )

        self.next_button = tk.Button(
            self.control_view,
            text = "Next",
            command = self.next,
            state = "disabled"
        )

        self.restart_button = tk.Button(
            self.control_view,
            text = "Restart",
            command = self.restart
        )

        self.empty_button = tk.Button(
            self.control_view,
            text = "Empty",
            command = self.empty
        )

        self.run_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)
        self.restart_button.grid(row=0, column=2)
        self.empty_button.grid(row=0, column=3)

        #### End of control pannel setup ####

        ####          Menu setup         ####
        self.menu = tk.Menu(self)

        self.menu.add_command(
            label = "Load board",
            command = self.menu_load)
        self.menu.add_command(
            label = "Save board",
            command = self.menu_save_board)
        self.menu.add_command(
            label = "Save solution",
            command = self.menu_save_solution)
        self.menu.add_command(
            label = "Help",
            command = self.menu_help)

        ####      End of menu setup      ####


       #####        App setup         #####
        self.config(menu = self.menu)
        HeaderView(self).grid(row=1, column=0)
        self.board_view.grid(row=2, column=0)
        self.control_view.grid(row = 3, column = 0)

       #####  Menu callback functions ######

    def menu_load(self):
        file = tkfd.askopenfile(mode="r")
        self.state.load_board_from_file(file)
        self.board_view.update_view()
        self.run_button['state'] = "normal"
        self.next_button['state'] = "disabled"

    def menu_save_board(self):
        file = tkfd.asksaveasfile(mode="w")
        self.state.save_board_to_file(file)

    def menu_save_solution(self):
        if self.state.current_solution:
            file = tkfd.asksaveasfile(mode="w")
            self.state.save_solution_to_file(file)
        else:
            tkmb.showerror(title="Error!", message="There's no solution to save!")
    def menu_help(self):
        help_message = ("Instructions:\n"
            "*Left click a board button to increment it's value.\n"
            "*Right click a board button to decrement it's value.\n"
            "<Run!>Runs the search on a new board configuration.\n"
            "<Next>Search for the next possible valid solution.\n"
            "<Restart>Restores the state of the board before search\n"
            "<Empty>Resets all values of the board.")

        tkmb.showinfo(title="Help", message=help_message)

    ##### Command pannel callback functions #####

    def run(self):
        """Callback function that triggers the search algorithm"""
        for square in self.board_view.board_view.keys():
            self.board_view.change_square_setting(square, "bg", "lightgrey")
        irregular = self.state.check_board_consistency()
        if len(irregular):
            for square in irregular:
                self.board_view.change_square_setting(square, "bg", "red")
            tkmb.showerror(title="Error!",
                message="Please check conflicts on the board!\n"
                    "Nobody likes infinite recursion.")
            return
        self.state.set_state("run")
        self.run_button['state'] = "disabled"
        self.next_button['state'] = "normal"
        board = self.state.board
        self.state.init_solution_iter()
        solution = self.state.get_next_solution()
        if solution:
            self.board_view.update_view(solution)
        else:
            #TODO: Alert message
            pass

    def next(self):
        """Callback function that iterates over the search algorithm"""
        solution = self.state.get_next_solution()
        if solution:
            self.board_view.update_view(solution)
        else:
            #TODO: Alert message
            self.next_button['state']="disabled"

    def empty(self):
        """Callback function that empties both the board and board view"""
        self.state.set_state("stop")
        self.state.reset_board()
        self.board_view.reset_board_view()
        self.run_button['state'] = "normal"
        self.next_button['state']= "disabled"

    def restart(self):
        """Callback function that restores the board view to the state
        it was before the search was ran"""
        self.state.set_state("stop")
        self.board_view.update_view()
        self.run_button['state'] = "normal"
        self.next_button['state'] = "disabled"


if __name__ == '__main__':
    app = Application()
    app.mainloop()
