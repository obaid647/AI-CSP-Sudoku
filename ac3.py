#imports
from collections import deque
from csp import SudokuCSP, read_puzzle

"""
main ac3 algorithm to enforce arc consistency and find solution
"""
def ac3(csp):
    
    #initialize empty dequeue to hold arcs
    queue = deque(csp.get_all_arcs())
    
    #while there are arcs in queue
    while queue:
        
        #print queue length at each iteration
        print(f"Queue length: {len(queue)}")
        
        #retrieve first arc and assign to xi and xj
        (xi, xj) = queue.popleft()
        
        #call revise func to check if domain of xi needs to be updated to be consistent with xj
        if revise(csp, xi, xj):
            
            #check if domain of xi is empty after revision
            if not csp.domains[xi[0]][xi[1]]:
                #if empty no valid values remain
                return False
            
            #loop through each neighbor xk of xi
            for xk in csp.neighbors[xi[0]][xi[1]]:
                
                #check if xk is not the cell xj that was revised
                if xk != xj:
                    
                    #add arc back to queue to check consistency of xi neighbors
                    queue.append((xk, xi))
    
    #check if every cell in grid has exactly 1 value in domain                
    solved = all(len(csp.domains[row][col]) == 1 for row in range(9) for col in range(9))
    
    #if solved print in readable format
    if solved:
        print("Puzzle solved by AC-3")
        print_solution(csp)
        return True
    
    #puzzle failure message
    else:
        print("Puzzle is not fully solved by AC-3.")
        return False
    
"""
checks if domain of xi should be adjusted based on xj
"""
def revise(csp, xi, xj):
    
    #initialize revised to false to track changes to xi domain
    revised = False
    
    #get domains of cells xi and xj
    xi_domain = csp.domains[xi[0]][xi[1]]
    xj_domain = csp.domains[xj[0]][xj[1]]
    
    #loop through xi domain
    #copy used to avoid modifying domain while iterating
    for value in xi_domain.copy():
        
        #check if xj has only 1 possible value and if it exist in xi domain
        if len(xj_domain) == 1 and value in xj_domain:
            
            #remove value from xi domain
            xi_domain.remove(value)
            
            #xi domain has been changed
            revised = True
    
    return revised

"""
prints sudoku puzzle in readable format
"""
def print_solution(csp):
    
    #iterate rows in domains
    for row in csp.domains:
        
        #print each cell value if domain has only 1 value otherwise 0
        print([list(cell)[0] if len(cell) == 1 else 0 for cell in row])
        
"""
order values by least constraining value heuristic
"""
def order_domain_values(sudoku_csp, row, col):
    #return values in ascending order of constraint of cell (row,col)
    #sorting key is lambda func that calls counting func to find constraint value
    return sorted(sudoku_csp.domains[row][col], key=lambda val: count_constraints(sudoku_csp, row, col, val))

"""
count num of constraints when assigning value to cell (row, col) would have on neighbors
"""
def count_constraints(sudoku_csp, row, col, value):
    
    #initialize count
    count = 0
    
    #iterate each neighbor of cell
    for neighbor in sudoku_csp.neighbors[row][col]:
        
        #unpack neighbor coordinates
        n_row, n_col = neighbor
        
        #check if neighbor domain has more than 1 possible value and if value is in domain
        if len(sudoku_csp.domains[n_row][n_col]) > 1 and value in sudoku_csp.domains[n_row][n_col]:
            #increment count
            count += 1
            
    return count

"""
removes value from domains of neighboring cells after value is assigned.
if neighbor left with empty domain there is conflict
"""
def forward_check(csp, row, col, value):
    
    #store removed values from neighbor domains
    removed = []
    
    #iterate each neighbor of cell
    for neighbor in csp.neighbors[row][col]:
        
        #unpack neighbor coordinates
        nrow, ncol = neighbor
        
        #check if value is present in neighbor domain
        if value in csp.domains[nrow][ncol]:
            
            #remove value from neighbor domain
            csp.domains[nrow][ncol].remove(value)
            
            #record removed value
            removed.append((nrow, ncol, value))
            
            #check if neighbor domain empty
            if not csp.domains[nrow][ncol]:
                return False, removed
    
    #no conflict found        
    return True, removed

"""
restores previously removed values to domain in neighboring cells
"""
def restore_domains(csp, removed):
    
    #iterate each tuple in removed
    for row, col, value in removed:
        
        #add value back to domain of cell
        csp.domains[row][col].add(value)

"""
backtracking algorithm to solve sudoku puzzle if AC-3 is incomplete
"""
def backtrack(csp):
    
    #call func to find next empty cell in puzzle
    emptyCell = find_empty_cell(csp)

    #all cells have single value in domain and puzzle is solved
    if not emptyCell:
        return True
    
    #unpack cell coordinates
    row, col = emptyCell
    
    #loop over possible values in domain of cell to see if value led to solution
    for value in order_domain_values(csp, row, col):
        
        #check if value at coordinates is valid
        if is_valid(csp, row, col, value):
            
            #assign value to cell to single value set
            csp.domains[row][col] = {value}

            #forward check to remove value from neighbor domains
            success, removed = forward_check(csp, row, col, value)
            
            #forward check successful
            if success:
                
                #call backtrack recursively
                if backtrack(csp):
                    #puzzle solved
                    return True
            
            #undo assignment if recursive call unsuccessful
            csp.domains[row][col] = set(order_domain_values(csp, row, col))
            
            #restore values of forward check
            restore_domains(csp, removed)
    
    #no values led to solution
    return False
    
"""
find next empty cell with fewest possible values in puzzle
"""
def find_empty_cell(sudoku_csp):
    
    #initialize min length and best cell
    min_len = float('inf')
    best_cell = None
    
    #iterate rows
    for row in range(9):
        
        #iterate columns
        for col in range(9):
            
            #retrieve domain size of cell
            domain_size = len(sudoku_csp.domains[row][col])
            
            #if cell has more than 1 value and fewer than 
            if 1 < domain_size and domain_size < min_len:
                
                #update minimum and best cell
                min_len = domain_size
                best_cell = (row, col)
    
    return best_cell
        
"""
check if assigning a value to a cell is consistent with neighbors
"""
def is_valid(csp, row, col, value):
    
    #loop over all neighbor of cell
    for neighbor in csp.neighbors[row][col]:
        
        #unpack neighbor coordinates
        nrow, ncol = neighbor
        
        #check if neighbor cell has single value in domain and equal to value
        if len(csp.domains[nrow][ncol]) == 1 and value in csp.domains[nrow][ncol]:
            #value conflicts with neighbor
            return False
    
    #no conflicts found
    return True
        
def main():
    
    input_puzzle = read_puzzle("input.txt")
    csp = SudokuCSP(input_puzzle)
    
    #attempt to solve puzzle with ac3
    if not ac3(csp):
        print("Solving puzzle with backtracking.")
        
        #attempt to solve puzzle using backtracking
        if backtrack(csp):
            print("Puzzle solved with backtracking.")
            print_solution(csp)
        
        #puzzle unable to be solved
        else:
            print("No solution found.")
    
if __name__ == "__main__":
    main()
