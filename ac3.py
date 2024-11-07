#imports
from collections import deque
from csp import SudokuCSP, read_puzzle
"""
main ac3 algorithm to enforce arc consistency and find solution
"""
def ac3(csp):
    
    #initialize empty dequeue to hold arcs
    queue = deque()
    
    #loop over rows
    for row in range(9):
        
        #loop over columns
        for col in range(9):
            
            #iterate over each cell's neighbor
            #neighbor is cell in same row, col, or 3x3 subgrid
            for neighbor in csp.neighbors[row][col]:
                
                #append arc to queue
                queue.append(((row, col), neighbor))
    
    #while there are arcs in queue
    while queue:
        
        #print queue length at each iteration
        print(f"Queue length: {len(queue)}")
        
        #remove first arc and assign to xi and xj
        (xi, xj) = queue.popleft()
        
        #call revise func to check if domain of xi needs to be updated to be consistent with xj
        if revise(csp, xi, xj):
            
            #check if domain of xi is empty after revision
            if not csp.neighbors[xi[0]][xi[1]]:
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
        print_solution(csp)
    
    #puzzle failure message
    else:
        print("Puzzle is not fully solved.")
    
    return solved
    
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
        
def main():
    
    input_puzzle = read_puzzle("input.txt")

    # #example puzzle
    # inputPuzzle = [
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
    csp = SudokuCSP(input_puzzle)
    ac3(csp)
    
if __name__ == "__main__":
    main()