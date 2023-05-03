"""
Goal of Task 2:
    Interpolate missing GNSS values with IMU accelerations to use a Kalman Filter with a frequency of 50 Hz.

Hint: The Kalman Filter is already implemented in KalmanFilter.py.
"""


import numpy as np


def adaptHmatrix(current_measurement, last_measurement):
    """
    inputs:
        current_measurement (type: np.ndarray, shape (4,)): [a_x, a_y, pos_x, pos_y]
        last_measurement (type: np.ndarray, shape (4,)): [a_x, a_y, pos_x, pos_y]

    output:
        H (type: np.matrix): H matrix
    """

    # Task:
    # ToDo: check if new GNSS value arrived (extract GNSS value from measurement vector) and adapt H matrix accordingly
    # Hints:
    #   - use GNSS measurements if they changed, otherwise set them zero
    #   - the H matrix using both, IMU and GNSS can be found in KalmanFilter.py
    #   - use np.matrix()
    ########################
    #  Start of your code  #
    ########################

    if current_measurement[2] == last_measurement[2]:
        a_x = 1.0
        pos_x = 0.0
    else:
        a_x = 1.0
        pos_x = 1.0

    if current_measurement[3] == last_measurement[3]:
        a_y = 1.0
        pos_y = 0.0
    else:
        a_y = 1.0
        pos_y = 1.0

    H = np.matrix([[0.0, 0.0, 0.0, 0.0, a_x, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, a_y],
                   [pos_x, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, pos_y, 0.0, 0.0, 0.0, 0.0]])

    ########################
    #   End of your code   #
    ########################

    return H
