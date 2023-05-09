"""The n queens puzzle"""
import numpy as np
import matplotlib.pyplot as plt

class NQueens:
    """Generate all valid solutions for the n queens puzzle"""

    def __init__(self, size):
        # Store the puzzle (problem) size and the number of valid solutions
        self.size = size
        self.solutions = 0
        self.first_solution = []  # A sequence of boards states that describes what steps did program take to solve task

    def solve(self):
        """Solve the n queens puzzle and print the number of solutions"""
        positions = [-1] * self.size
        self.put_queen(positions, 0)

    def put_queen(self, positions, target_row):
        """
        Try to place a queen on target_row by checking all N possible cases.
        If a valid place is found the function calls itself trying to place a queen
        on the next row until all N queens are placed on the NxN board.
        """
        # Base (stop) case - all N rows are occupied
        if target_row == self.size:
            self.show_full_board(positions)
            if self.solutions == 0:
                self.first_solution.append(self.show_full_board(positions))
            self.solutions += 1
        else:
            # For all N columns positions try to place a queen
            if self.solutions == 0:
                self.first_solution.append(self.show_full_board(positions))

            for column in range(self.size):
                # Reject all invalid positions
                if self.check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.put_queen(positions, target_row + 1)

    def check_place(self, positions, occupied_rows, column):
        """
        Check if a given position is under attack from any of
        the previously placed queens (check column and diagonal positions)
        """
        for i in range(occupied_rows):
            if positions[i] == column or \
                    positions[i] - i == column - occupied_rows or \
                    positions[i] + i == column + occupied_rows:
                return False
        return True

    def show_full_board(self, positions):
        """Show the full NxN board"""
        board = np.zeros((self.size, self.size))
        for i, col in enumerate(positions):
            if col != -1:
                board[i, col] = 1

        return board


def main():
    """Initialize and solve the n queens puzzle"""
    task = NQueens(8)
    task.solve()


if __name__ == "__main__":
    # execute only if run as a script
    main()
