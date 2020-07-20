# Sudoku-Solver
To solve a Sudoku puzzle, one needs to use a combination of logic and trial-and-error. More math is involved behind the scenes: combinatorics used in counting valid Sudoku grids, group theory used to describe ideas of when two grids are equivalent, and computational complexity with regards to solving Sudokus.

# Rule
The standard version of Sudoku consists of a 9×9 square grid containing 81 cells. The grid is subdivided into nine 3×3 blocks. Some of the 81 cells are filled in with numbers from the set {1,2,3,4,5,6,7,8,9}. These filled-in cells are called givens. The goal is to fill in the whole grid using the nine digits so that each row, each column, and each block contains each number exactly once. We call this constraint on the rows, columns, and blocks the One Rule.

The above-described puzzle is called a Sudoku of rank 3. A Sudoku of rank n is an n2×n2 square grid, subdivided into n2 blocks, each of size n×n. The numbers used to fill the grid in are 1, 2, 3, ..., n2, and the One Rule still applies.

# solving stratergy
The most basic strategy to solve a Sudoku puzzle is to first write down, in each empty cell, all possible entries that will not contradict the One Rule with respect to the given cells. If a cell ends up having only one possible entry, it is a "forced" entry that you should fill in.

# Implementation
The sudokuGUI.py contains the main GUI code that uses pygame.

# Algorithm
Starting with an incomplete board:

1. Find some empty space
2. Attempt to place the digits 1-9 in that space
3. Check if that digit is valid in the current spot based on the current board
     a. If the digit is valid, recursively attempt to fill the board using steps 1-3.
     b. If it is not valid, reset the square you just filled and go back to the previous step.
4. Once the board is full by the definition of this algorithm we have found a solution.
5. We will finish about half of the algorithm in part 1. In part 2 (look below) we will implement the entire algorithm.
