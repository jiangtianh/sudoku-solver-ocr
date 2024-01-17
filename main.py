from sudoku_solver_gui import SudokuGUI
from tkinter import Tk
from grid import Grid

if __name__ == "__main__":
    root = Tk()
    grid = Grid()
    s = SudokuGUI(root, grid)

    root.mainloop()