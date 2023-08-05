# test_fronts.py
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from rocket_moea.fronts import get_front

if __name__ == "__main__":

    m_objs = 3
    
    for mop_name in ("dtlz1", "dtlz2", "dtlz3", "inv-dtlz1"):
    
        # get front
        front = get_front(mop_name, m_objs)
        
        # plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        
        # setup plot
        ax.set_xlabel("$f_1$")
        ax.set_ylabel("$f_2$")
        ax.set_zlabel("$f_3$")
        ax.set_title(mop_name)
        ax.view_init(30, 45)
        
        ax.plot(front[:, 0], front[:, 1], front[:, 2], marker="o", color="#74CE74", ls="none")
        plt.show()
