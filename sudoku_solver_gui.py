import tkinter as tk
from tkinter import Tk, filedialog
from grid import Grid
import ocr_preprocessing
import ocr

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9



'''
This class is the GUI for the sudoku solver
It is responsible for drawing the grid, the numbers, the cursor, and the buttons
It also handles the key press events
'''
class SudokuGUI(tk.Frame):
    '''
    Constructor for the SudokuGUI class
    input:  parent -> Tk object
            grid -> the grid object that the GUI will be working with
    '''
    def __init__(self, parent, grid):
        self.grid = grid 
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.__initUI()

    '''
    Initialize the UI
    '''
    def __initUI(self):
        self.parent.title("Sudoku Solver")
        self.pack(fill=tk.BOTH, expand=1)
        
        self.parent.geometry(f"{WIDTH}x{HEIGHT + 100}")
        self.parent.config(bg="white")

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tk.BOTH, side=tk.TOP)

        solve_button = tk.Button(self, text="Solve", command=self.__solve)
        solve_button.pack(fill=tk.BOTH, side=tk.TOP)

        clear_button = tk.Button(self, text="Clear", command=self.__clear)
        clear_button.pack(fill=tk.BOTH, side=tk.TOP)

        load_image_button = tk.Button(self, text="Load Sudoku From Image", command=self.__load_image)
        load_image_button.pack(fill=tk.BOTH, side=tk.TOP)

        self.__draw_grid()
        self.__draw_cursor()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)
        self.canvas.bind("<Left>", self.move_left)
        self.canvas.bind("<Right>", self.move_right)
        self.canvas.bind("<Up>", self.move_up)
        self.canvas.bind("<Down>", self.move_down)
        self.canvas.bind("<BackSpace>", self.delete_number)  


    '''
    This method is used to load the sudoku puzzle from an image
    It will open a file dialog and let the user choose an image file for OCR processing
    '''
    def __load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")])
        if filepath:
            ocr_preprocessing.write_image_to_file(filepath)

            self.gird = Grid()
            ocr.ocr_image_to_GridObj(self.grid)
            print(self.grid)
        
        self.__draw_puzzle()



    '''
    Draw the grid lines for the sudoku puzzle in the canvas
    '''
    def __draw_grid(self):
        for i in range(0, 10):
            color = 'blue' if i % 3 == 0 else 'gray'

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)


    '''
    Draw the cursor for the sudoku puzzle in the canvas that indicates the current position of the user
    The cursor is a red rectangle that is drawn on top of the grid lines, the position of the cursor is determined by the row and col attributes
    '''
    def __draw_cursor(self):
        self.canvas.delete("cursor")

        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    
    '''
    Solve the sudoku puzzle using the backtracking algorithm
    it will call the solveSudoku method in the grid object, and the result will be displayed in the canvas
    '''
    def __solve(self):
        if self.grid.check_valid_sudoku():
            self.grid.solveSudoku(0)

            if self.grid.solved == False:
                self.__draw_message("Unsolvable Sudoku")
            else:
                self.__draw_puzzle()
            print(self.grid)

        else:
            self.__draw_message("Invalid Sudoku")


    '''
    Clear the sudoku puzzle by resetting the grid object and redraw the puzzle in the canvas
    '''
    def __clear(self):
        self.grid = Grid()
        self.__draw_puzzle()

    '''
    Detect the cell that the user clicked on and set the row and col attributes accordingly
    '''
    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
    
            self.row, self.col = row, col
        self.__draw_cursor()


    '''
    Draw the puzzle in the canvas using the numbers in the grid object
    '''
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                num = self.grid.grid[i][j]
                if num is not None:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    self.canvas.create_text(x, y, text=num, tags="numbers", fill="sea green", font=("Arial", 30, "bold"))

    '''
    Allows the user to input numbers into the sudoku puzzle using the keyboard
    '''
    def __key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            
            self.grid.delete_number(self.row, self.col)
            self.grid.add_number(self.row, self.col, int(event.char))
            self.__draw_puzzle()
            self.__draw_cursor()
            print(self.grid)

    '''
    Move the cursor to the left
    '''
    def move_left(self, event):
        if self.col > 0:
            self.col -= 1
            self.__draw_cursor()

    '''
    Move the cursor to the right
    '''
    def move_right(self, event):
        if self.col < 8:
            self.col += 1
            self.__draw_cursor()
    '''
    Move the cursor up
    '''
    def move_up(self, event):
        if self.row > 0:
            self.row -= 1
            self.__draw_cursor()

    '''
    Move the cursor down
    '''
    def move_down(self, event):
        if self.row < 8:
            self.row += 1
            self.__draw_cursor()

    '''
    Allow the user to delete a number from the sudoku puzzle using the backspace key
    '''
    def delete_number(self, event):
        if self.row >= 0 and self.col >= 0:
            self.grid.delete_number(self.row, self.col)
            self.__draw_puzzle()
    

    def __draw_message(self, message):
        x0 = y0 = MARGIN + SIDE * 1
        x1 = y1 = MARGIN + SIDE * 8
        self.canvas.create_oval(x0, y0, x1, y1, tags='message', fill='dark orange', outline='orange')

        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y, text=message, tags='message_text', fill='white', font=('Arial', 32))
        self.parent.after(3000, self.__dismiss_message)
        self.parent.bind('<Button-1>', self.__dismiss_message)
        self.parent.bind('<Key>', self.__dismiss_message)


    def __dismiss_message(self, event=None):
        self.canvas.delete('message', 'message_text')
        self.parent.unbind('<Button-1>', self.__dismiss_message)
        self.parent.unbind('<Key>', self.__dismiss_message)

