# sudoku-solver-ocr

## Overview
This Sudoku Solver is a Python-based application built using the Tkinter GUI library. The program allows users to interactively solve Sudoku puzzles, either by manually inputting numbers or by loading puzzles from images through an Optical Character Recognition (OCR) feature. The solver employs a backtracking algorithm to find the solution for the Sudoku puzzle.

## Features
Interactive GUI: The user-friendly graphical interface allows users to input numbers manually, navigate through cells, and visualize the solving process.

OCR Integration: Load Sudoku puzzles from images using the OCR feature. The program processes the image using cv2, then extracts the puzzle. (Due to the nature of OCR, it's not perfect. User will need to manually adjust some of the numbers the program extracts)

Backtracking Algorithm: The solver utilizes a backtracking algorithm to find the solution to the Sudoku puzzle, ensuring efficiency and accuracy.

Navigation and Editing: Users can easily navigate through cells using arrow keys, edit numbers, and clear the entire puzzle when needed.

## Getting Started
1. Install the dependencies:
```
pip install -r requirements.txt
```
2. Run the program:
```
python main.py
```

## Usage
* Manual Input:
    * Click on cells to select them. 
    * Use keyboard input to enter numbers.
    * Navigate through cells using arrow keys.
    * Clear a cell with the Backspace key.

* OCR Feature:
    * Click on "Load Sudoku From Image" to open a file dialog.
    * Select an image file containing a Sudoku puzzle.
    * The program will process the image, recognize the puzzle, and display the solution.

* Solve Puzzle:
    * Click on the "Solve" button to solve the puzzle using the backtracking algorithm.
    * The solved puzzle will be displayed on the GUI.

* Clear Puzzle:
    * Click on the "Clear" button to reset the Sudoku puzzle.