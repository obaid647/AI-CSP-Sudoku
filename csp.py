class SudokuCSP:
    def __init__(self, puzzle):
        #sets the domains
        #each cell takes values 1 from 9 if empty
        self.domains = []
        for i in range(9):
             row = []
             for j in range(9):

                if puzzle [i][j] == 0:
                    row.append(set(range(1,10)))
                else:
                    row.append({puzzle[i][j]})
             self.domains.append(row)
        #neighbors represents values in the same row, col, or 3x3 grid
        self.neighbors = self.get_all_neighbors()

    def get_all_neighbors(self):
            neighbors = []
            for _ in range(9):
                row_neighbors = []
                for _ in range (9):
                    row_neighbors.append(set())
                neighbors.append(row_neighbors)
            for row in range (9):
                for col in range (9):
                    neighbors[row][col] = self._get_neighbors(row,col)
            return neighbors
        
    def _get_neighbors(self, row, col):
            neighbors = set()
            #Add cells in the same row
            for j in range(9):
                if j!= col:
                    neighbors.add((row, j))

            #add cells in the same column
            for i in range(9):
                if i!= row:
                    neighbors.add((i, col))
            #add cells in the same 3x3 sub-grid
            grid_row, grid_col = 3* (row//3), 3*(col//3)
            for i in range(grid_row, grid_row + 3):
                for j in range (grid_col, grid_col + 3):
                    if(i, j) != (row, col):
                        neighbors.add((i,j))
            return neighbors
        
    def get_all_arcs(self):
        arcs = set()
        for row in range(9):
            for col in range(9):
                for neighbor in self.neighbors[row][col]:
                    arcs.add(((row, col), neighbor))
        return sorted(list(arcs))

def read_puzzle(fileName):
    input_puzzle = []
    with open(fileName, "r") as f:
        for line in f:
            row = [int(num) for num in line.strip().split()]
            input_puzzle.append(row)
    return input_puzzle

def main():
    input_puzzle = read_puzzle("input.txt")
    sudoku_csp = SudokuCSP(input_puzzle)
    row, col = 8,8
    print("Domains initialized:", sudoku_csp.domains)
    print(f'Neighbors for cell ({row},{col}):', sudoku_csp.neighbors[row][col])


if __name__ == "__main__":
    main()

# Example usage:
# Assuming input_puzzle is a 9x9 grid (list of lists) with 0 representing empty cells
# input_puzzle = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

# sudoku_csp = SudokuCSP(input_puzzle)
# row, col = 8,8
# print("Domains initialized:", sudoku_csp.domains)
# print(f'Neighbors for cell ({row},{col}):', sudoku_csp.neighbors[row][col])

