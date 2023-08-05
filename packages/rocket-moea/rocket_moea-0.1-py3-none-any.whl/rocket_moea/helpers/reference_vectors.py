# reference_vectors.py
from __future__ import print_function
import numpy as np

def fact(n):
    """
    Factorial of n
    """
    
    if n < 0:
        print("Error, n must be positive")
        return None
        
    if n == 0 or n == 1:
        return 1
        
    result = 1
    for i in range(1, n+1):
        result *= i
        
    return result


def get_limit(m_objs, H):
    """
    Return the number of solutions for Eq (1) [see list_sol()]
    """
    
    n = H + m_objs - 1
    k = H
    
    # numerator
    num = 1
    for i in range(k):
        num *= (n-i)
        
    # denominator
    den = fact(k)
    
    limit = num / den
    
    return int(limit)
   

def next_sol(sol, m_objs, H):
    """
    Create a new solution (sol) by incrementing the value of
        
        sol[m_objs-2] += 1
    
    and adjusting the last position of sol
        
        sol[m_objs-1] = H - sum(new_sol)
        
    The resulting solution (new_sol) can be invalid.
    
    Input
    sol         list, solution with m_objs integers
    m_objs      int, number of objectives
    H           int, granularity >= 2
    
    Output
    new_sol     list, a (possibly) valid solution
    """

    new_sol = [0]*m_objs
    
    for i in range(m_objs-1):
        new_sol[i] = sol[i]
        
    new_sol[m_objs-2] += 1
    new_sol[m_objs-1] = H - sum(new_sol)
    
    return new_sol
   
    
def check_sol(sol, m_objs, H, verbose=False):
    """
    Determine whether a solution (sol) is valid.
    
    Input
    sol         list, solution with m_objs integers
    m_objs      int, number of objectives
    H           int, granularity >= 2
    verbose     bool, flag to show messages
    
    Output
    ok          bool, if ok is False, sol is invalid
    error_pos   int, position of the first invalid value found in sol (if any)
    """

    ok = True
    error_pos = None
    
    for pos in range(m_objs-2, -1, -1):             # sequence [m_objs-2, ..., 0]
    
        lb = 0
        ub = H - sum(sol[:pos])                     # sum(sol[0], ..., sol[pos-1])
    
        if sol[pos] >= lb and sol[pos] <= ub:
            continue
        else:
            ok = False
            error_pos = pos
            
            if verbose:
                print(" * %s, pos %d" % (sol, pos))
                
    return ok, error_pos
    

def repair_sol(sol, m_objs, H, pos):
    """
    Given a solution (sol), a new solution is created (new_sol).
    This function copies the first pos-1 values of sol into new_sol.
    Then, the value before pos (new_sol[pos-1]) is incremented.
    Finally, the last position (new_sol[m_objs-1] == new_sol[-1])
    is adjusted to sum H.
    
    Input
    sol         list, solution with m_objs integers
    m_objs      int, number of objectives
    H           int, granularity >= 2
    pos         int, position of the first invalid value found in sol
    
    Output
    new_sol     list, a (possibly) valid solution
    """
    
    new_sol = [0]*m_objs
    
    for i in range(pos):
        new_sol[i] = sol[i]
        
    new_sol[pos-1] += 1
    
    # adjust the last position to sum H
    new_sol[m_objs-1] = H - sum(new_sol[:m_objs])   # it sums everything except the last position
    
    return new_sol


def full_repair_sol(sol, m_objs, H, verbose=False):
    """
    Given a solution (sol), this function determines if sol is a valid solution.
    If so, it is returned. Otherwise, a new attempt is made and the process
    is repeated until a valid solution is created.
    
    Input
    sol         list, solution with m_objs integers
    m_objs      int, number of objectives
    H           int, granularity >= 2
    verbose     bool, flag to show messages
    
    Output
    new_sol     list, a valid solution
    """
    
    sol_is_ok = False       # we assume that sol is invalid
    new_sol = list(sol)     # returned solution
    
    while not sol_is_ok:
        
        # determine whether new_sol is valid
        ok, pos = check_sol(new_sol, m_objs, H, verbose)
        
        if ok:
            sol_is_ok = True
            return list(new_sol)
            
        else:
            # create a new solution and repeat the process
            new_sol = repair_sol(new_sol, m_objs, H, pos)


def list_sol(m_objs, H, verbose=False):
    """
    Create a matrix (W) with the integer solutions to this equation:
    
        x_1 + x_2 + ... + x_{m_objs} = H    (1)
        
    The number of solutions is limit:
    
        limit = binom{H+m-1}{H}
              = binom{H+m-1}{m-1}
              
    Input
    m_objs      int, number of objectives
    H           int, granularity >= 2
    verbose     bool, flag to show messages
    
    Output
    W           (limit, m_objs) int np.array with solutions to Eq. (1)
    """
    
    limit = get_limit(m_objs, H)
    
    # output matrix
    W = np.zeros((limit, m_objs), dtype=int)
    
    # initial solution
    sol_a = [0]*m_objs
    sol_a[-1] = H
    
    if verbose:
        print("%2s %s" % (0, sol_a))
        
    # add to W
    W[0, :] = np.array(sol_a)
    
    # main loop
    for i in range(limit-1):
        
        # get next solution
        sol_b = next_sol(sol_a, m_objs, H)
        
        # repair it, if needed
        sol_c = full_repair_sol(sol_b, m_objs, H, verbose)
        
        # update reference
        sol_a = list(sol_c)
        
        if verbose:
            print("%2d %s" % (i+1, sol_a))
            
        # add to W
        W[i+1, :] = np.array(sol_a)
        
    return W.copy()
    

def check_vectors(W, H, verbose):
    """
    Check if the sum of each row of W equals H
    
    Input
    W           (n_rows, m_objs) np.array with n_rows solutions
    H           granularity
    verbose     bool, flag to show messages
    
    Output
    to_keep     (n_rows, ) bool np.array, if to_keep[i] == True, then
                the i-th row of W is invalid
    indices     (l, ) int np.array, if W has invalid rows, indices
                contains the indices of those invalid rows
    """
    
    by_row = 1
    suma = W.sum(axis=by_row)
    
    indices = None
    to_keep = suma != H
    
    if to_keep.any():
        print("Error, W has invalid rows")
        indices = np.arange(len(to_keep), dtype=int)[to_keep]
    else:
        if verbose:
            print("W is OK")
        return None, None
        
    return to_keep.copy(), indices.copy()
    
    
def get_reference_vectors(m_objs, H, verbose=False):
    """
    Return a matrix of reference vectors
    
    Input
    m_objs          int, number of objectives
    H               int, granularity >= 2
    verbose         bool, flag to show messages
    
    Output
    Wp              (n_rows, m_objs) float np.array, reference vectors
    """
    
    W = list_sol(m_objs, H, verbose)
    
    # check
    check_vectors(W, H, verbose)
    
    # normalize
    Wp = W/H
    
    return Wp.copy()
    
    
    
    
    
