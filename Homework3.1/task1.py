"""
Goal of Task 1:
    Implement an automated map-generator.

Hint: Use the already implemented EKF SLAM in EKF_SLAM.py to test your code.
"""
import random
import numpy as np


def GenerateLandmarks(x_min, x_max, y_min, y_max, n):
    """
    inputs:
        x_min (type: int): lower limit of x-coordinate
        x_max (type: int): upper limit of x-coordinate
        y_min (type: int): lower limit of y-coordinate
        y_max (type: int): upper limit of y-coordinate
        n (type: int): number of landmarks to be generated

    output:
        landmarks (type: np.ndarray, shape (n,2)): [x, y] - points for all n landmarks
    """

    # Task:
    # ToDo: Generate n randomly positioned landmarks within the given range.
    ########################
    #  Start of your code  #
    ########################
    landmarks = np.ndarray(shape=(n, 2), dtype=int)

    for i in range(n):
        landmarks[i][0] = random.randrange(x_min, x_max)
        landmarks[i][1] = random.randrange(y_min, y_max)
    ########################
    #   End of your code   #
    ########################

    return landmarks
