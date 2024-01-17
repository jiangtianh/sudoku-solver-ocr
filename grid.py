

class Grid:
    '''
    Grid class for sudoku solver
    Responsible for storing the sudoku grid and solving it
    Include methods for adding and deleting numbers from the grid based on the columns and rows, 
    Checking if a number is valid to place in a certain position,
    Solving the sudoku grid using backtracking algorithm,
    '''

    '''
    Constructor for the Grid class
    If no grid is provided, it will create an empty grid (grid is a 9 x 9 matrix)
    Else, it will run through the grid passed in, and add the numbers to the horizontal, vertical and square sets lists
    The horizontal, vertical and square lists are used to check if a number is valid to place in a certain position
    input:  grid -> 9 x 9 matrix containing the sudoku grid. If no grid is provided, it will be None
            The grid contains numbers from 1 - 9, and None for empty positions

    '''
    def __init__(self, grid=None):
        self.horizontal = [set() for _ in range(9)]
        self.vertical = [set() for _ in range(9)]
        self.square = [set() for _ in range(9)]

        if grid is not None:
            self.grid = grid
            for x in range(9):
                for y in range(9):
                    num = self.grid[x][y]
                    if num is not None:
                        self.horizontal[x].add(num)
                        self.vertical[y].add(num)
                        self.square[self.getSquareIdx(x, y)].add(num)


        else:
            self.grid = [[None] * 9 for _ in range(9)]

    '''
    Add a number to the specified position
    First check if the number is valid to place in that position, if it is, add the number to the grid and the horizontal, vertical and square sets lists accordingly
    Else, print an error message
    input:  x -> row index as integer
            y -> column index as integer
            num -> number to be placed as integer (1 - 9)
    '''
    def add_number(self, x, y, num):
        if self.check(x, y, num):
            self.grid[x][y] = num
            self.horizontal[x].add(num)
            self.vertical[y].add(num)
            self.square[self.getSquareIdx(x, y)].add(num)
        else:
            print("Invalid number to place here")
            
    '''
    Delete the number at the specified position
    First check if the position is empty, if it is, do nothing
    Else, delete the number from the grid, and the horizontal, vertical and square sets lists accordingly
    input:  x -> row index as integer
            y -> column index as integer
    '''
    def delete_number(self, x, y):
        if self.grid[x][y] is None:
            return
        num = self.grid[x][y]
        self.grid[x][y] = None
        self.horizontal[x].remove(num)
        self.vertical[y].remove(num)
        self.square[self.getSquareIdx(x, y)].remove(num)
        
    '''
    Get the square index of a certain position
    The square index is used to determine which square a certain position is in
    Square index is labeled as :
    0 1 2
    3 4 5
    6 7 8
    input:  x -> row index as integer
            y -> column index as integer
    '''
    def getSquareIdx(self, x, y):
        return (x // 3) * 3 + y // 3   
    
    '''
    Check if a number is valid to place in a certain position
    input:  x -> row index as integer
            y -> column index as integer
            num -> number to be placed as integer (1 - 9)
    '''
    def check(self, x, y, num):
        return num not in self.horizontal[x] and num not in self.vertical[y] and num not in self.square[self.getSquareIdx(x, y)]

    def __str__(self):
        s = ""
        for i in range(9):
            for j in range(9):
                s += str(self.grid[i][j]) + " "
            s += "\n"
        return s
    
    '''
    solveSudoku method using backtracking algorithm to solve the sudoku grid
    The algorithm will recursively try to place a number in a certain position, and if it is valid, it will move on to the next position
    If it is not valid, it will try the next number
    If it cannot place any number in a certain position, it will backtrack to the previous position and try the next number
    input:  i -> index of the position to be placed as integer (0 - 80) Row and Col can be calculated from this index
    '''
    def solveSudoku(self, i):
        if i == 81:
            return True
        
        x = i // 9
        y = i % 9
        
        if self.grid[x][y] is None:
            for num in range(1, 10):
                if self.check(x, y, num):
                    self.grid[x][y] = num
                    self.horizontal[x].add(num)
                    self.vertical[y].add(num)
                    self.square[self.getSquareIdx(x, y)].add(num)
                    if self.solveSudoku(i + 1):
                        return True
                    self.grid[x][y] = None
                    self.horizontal[x].remove(num)
                    self.vertical[y].remove(num)
                    self.square[self.getSquareIdx(x, y)].remove(num)
            return False
        else:
            return self.solveSudoku(i + 1)
        
    '''
    Check if the sudoku grid is valid
    It will check if there are any duplicate numbers in the horizontal, vertical and square sets lists
    '''
    def check_valid_sudoku(self):
        horizontal = [set() for _ in range(9)]
        vertical = [set() for _ in range(9)]
        square = [set() for _ in range(9)]
        for x in range(9):
            for y in range(9):
                num = self.grid[x][y]
                if num is not None:
                    if num in horizontal[x] or num in vertical[y] or num in square[self.getSquareIdx(x, y)]:
                        return False
                    else:
                        horizontal[x].add(num)
                        vertical[y].add(num)
                        square[self.getSquareIdx(x, y)].add(num)
        return True
        


