# fronts.py
from __future__ import print_function
import numpy as np
from numpy.linalg import norm
import os, sys
from rocket_moea.helpers import get_reference_vectors

def simplex_lattice(m_objs):
    """
    Create a uniform set of reference vectors.
    [Deb14] An Evolutionary Many-Objective Optimization Algorithm Using 
            Reference-Point-Based Nondominated Sorting Approach, 
            Part I: Solving Problems With Box Constrains
    
    Input
    m_objs      int, number of objectives
    
    Output
    w           (n_points, m_objs) float np.array, reference vectors
    """
    
    # spacing H1, H2
    spacing = {
        2: (99, 0),
        3: (12, 0),
        5: (6, 0),
        8: (3, 0),
        10: (3, 0),
    }
    
    dims = m_objs
    h1, h2 = spacing[m_objs]
    
    # create first layer
    w = get_reference_vectors(dims, h1)
    
    # create second layer (optional)
    if h2:
        sf = 0.5            # this scaling factor is employed in [Deb14], Fig 4.
        v = get_reference_vectors(dims, h2) * sf  
        
        merged = np.vstack((w, v))
        w = merged.copy()
        
    return w.copy()
    
def create_linear_front(m_objs, scale=None):
    """
    Create the linear Pareto front of DTLZ1 according to
    [Li15] An Evolutionary Many-Objective Optimization Algorithm Based on Dominance and Decomposition
    
    Input
    m_objs      int, number of objectives
    scale       (m_objs, ) scale[i] is the scaling factor for the i-th objective (ie, fronts[:, i]).
                If scale is None, the objectives are not scaled.
                
    Output
    front       (n_points, m_objs) float np.array, sample front
    """
    
    # uniform set of vectors
    vectors = simplex_lattice(m_objs)
    
    # number of vectors
    n_points = vectors.shape[0]
    
    by_row = 1
    div = vectors.sum(axis=by_row).reshape((n_points, 1))
    
    # linear pareto front
    front = 0.5 * (vectors / div)           # Eq. (14) [Li15]
    
    # scale each dimension (optional)
    if scale is not None:
        for m in range(m_objs):
            front[:, m] = front[:, m] * scale[m]
            
    return front.copy()
    
def create_spherical_front(m_objs, scale=None):
    """
    Create the spherical Pareto front of DTLZ2-4 according to
    [Li15] An Evolutionary Many-Objective Optimization Algorithm Based on Dominance and Decomposition
    
    Input
    m_objs      int, number of objectives
    scale       (m_objs, ) scale[i] is the scaling factor for the i-th objective (ie, fronts[:, i]).
                If scale is None, the objectives are not scaled.
                
    Output
    front       (n_points, m_objs) float np.array, sample front
    """
    
    # uniform set of vectors
    vectors = simplex_lattice(m_objs)
    
    # number of vectors
    n_points = vectors.shape[0]
    
    by_row = 1
    div = norm(vectors, axis=by_row).reshape((n_points, 1))
    
    # spherical pareto front
    front = vectors / div                   # Eq. (17) [Li15]
    
    # scale each dimension (optional)
    if scale is not None:
        for m in range(m_objs):
            front[:, m] = front[:, m] * scale[m]
            
    return front.copy()
    
def create_inverted_linear_front(m_objs, scale=None):
    """
    Create the inverted linear Pareto front of inv-DTLZ1 according to
    [Tian17] PlatEMO: A MATLAB Platform for Evolutionary Multi-Objective Optimization
    
    Input
    m_objs      int, number of objectives
    scale       (m_objs, ) scale[i] is the scaling factor for the i-th objective (ie, fronts[:, i]).
                If scale is None, the objectives are not scaled.
                
    Output
    front       (n_points, m_objs) float np.array, sample front
    """
    
    # uniform set of vectors
    vectors = simplex_lattice(m_objs)
    
    # inverted front as defined in IDTLZ1.m
    front = (1 - vectors) / 2
    
    # scale each dimension (optional)
    if scale is not None:
        for m in range(m_objs):
            front[:, m] = front[:, m] * scale[m]
            
    return front.copy()
    
def get_front(mop_name, m_objs):
    """
    Return the Pareto front of a given problem.
    
    Input
    mop_name            str, name of problem
    m_objs              int, number of objectives
    
    Output
    front               (pop_size, m_objs) np.array, Pareto front
    """
    
    if mop_name == "dtlz1":
        return create_linear_front(m_objs)
    
    elif mop_name == "inv-dtlz1":
        return create_inverted_linear_front(m_objs)
        
    elif mop_name in ("dtlz2", "dtlz3"):
        return create_spherical_front(m_objs)
        
    else:
        print("Problem not found (mop_name: %s)" % mop_name)
    
