"""
Task 1:
    Implement a hierarchical collision checker, which checks for collision of two trajectories (similar to the concept
    explained in slide 7-82 of the course presentation). The collision checker consists of three levels:
    1. Path collision check with Axis Aligned Bounding Boxes (AABBs)
    2. Collision check based on minimum bounding circle (MBC) approximation
    3. Exact collision check
"""

import numpy as np
import trajectory_planning_helpers as tph
from matplotlib import pyplot as plt
import random
from shapely.geometry import Polygon
from shapely.ops import unary_union


def generate_trajectories(n: int, vehicle_width: float, vehicle_length: float):
    """
    Returns randomly n trajectories out of a set of generated trajectories dictionaries. Based on the vehicle_width and
    vehicle_length a shapely polygon is calculated for every time step.

    inputs:
        n (type: int): number of trajectories
        vehicle_width (type: float)
        vehicle_length (type: float)

    output:
        (type: list): list of dicts
        The dictionaries consist of:
        Key:                  | Value:                                              |Type:
         - "t"                | Time array                                          | np.ndarray
         - "xy"               | xy- coordinates of middle point for every time step | np.ndarray
         - "psi"              | Heading of vehicle for every time step              | np.ndarray
         - "vehicle_polygons" | Polygon object for every time step                  | list (of shapely polygons)
    """

    # Boundary Conditions
    # All trajectories begin at x_0 and end at x_end
    x_0 = -10.0
    x_end = 10.0

    # The y-coordinate is varied between -10 and 10
    y_0_array = np.linspace(-10, 10, 7)
    y_end_array = np.linspace(-10, 10, 7)

    # Heading of vehicle shall be same at beginning and end
    psi = -np.pi / 2

    # Number of time steps per trajectory
    t_num = 5

    trajectories = []

    # Trajectory generation with trajectory planning helper module
    for y_0 in y_0_array:
        for y_end in y_end_array:
            # x, y and psi of path
            x_coeff, y_coeff, _, _ = tph.calc_splines.calc_splines(
                path=np.vstack((np.array([x_0, y_0]), np.array([x_end, y_end]))),
                psi_s=psi,
                psi_e=psi,
            )
            xy_spline, inds_spline, p_spline, _ = tph.interp_splines.interp_splines(
                coeffs_x=x_coeff, coeffs_y=y_coeff, stepnum_fixed=[50], incl_last_point=True
            )
            psi_spline, _ = tph.calc_head_curv_an.calc_head_curv_an(
                coeffs_x=x_coeff, coeffs_y=y_coeff, ind_spls=inds_spline, t_spls=p_spline
            )

            # Total length of path and s-coordinates
            len_spline = tph.calc_spline_lengths.calc_spline_lengths(coeffs_x=x_coeff, coeffs_y=y_coeff)
            s_spline = len_spline * p_spline

            # Time array and constant velocity
            t_end = 10
            t_array = np.linspace(0, t_end, t_num)
            v = len_spline / t_end

            # Get s, x, y and psi at desired time points
            s_array = v * t_array
            x_array = np.interp(x=s_array, xp=s_spline, fp=xy_spline[:, 0])
            y_array = np.interp(x=s_array, xp=s_spline, fp=xy_spline[:, 1])
            xy_array = np.stack((x_array, y_array), axis=-1)
            psi_array = np.interp(x=s_array, xp=s_spline, fp=psi_spline)

            vehicle_polygon_list = []

            # Calculate corner points of vehicle at every time step and generate polygon object
            for i, (xy, psi) in enumerate(zip(xy_array, psi_array)):
                # Four corner points of vehicle
                vehicle_points = np.array([[vehicle_length / 2, vehicle_width / 2],
                                           [vehicle_length / 2, -vehicle_width / 2],
                                           [-vehicle_length / 2, -vehicle_width / 2],
                                           [-vehicle_length / 2, vehicle_width / 2]])

                # Rotate and translate corner points
                vehicle_points = rotate_translate_point(vehicle_points, psi - np.pi / 2, xy[0], xy[1])

                # Create polygon object and add to polygon list
                vehicle_polygon_list.append(Polygon(vehicle_points))

            # Generate trajectory dictionary
            trajectory = {"xy": xy_array, "psi": psi_array, "vehicle_polygons": vehicle_polygon_list, "t": t_array}

            # Add trajectory to list of all trajectories
            trajectories.append(trajectory)

    # Return n random trajectories
    return random.sample(trajectories, n)


def rotate_translate_point(xy_points: np.ndarray, psi: float, x_tra: float, y_tra: float):
    """
    First rotates the xy_points by the angle psi. Secondly the point will be translated by x_tra and y_tra.

    inputs:
        xy_points (type: np.ndarray (of floats)): x and y coordinate of one or more points
        psi (type: float)
        x_tra (type: float)
        y_tra (type: float)

    output:
        xy_list_rot_tra (type: list (of tuples))
    """

    xy_list_rot_tra = []

    # Loop through every point
    for i, xy_point in enumerate(xy_points):
        # Rotate x- and y-coordinate
        x_rot = xy_point[0] * np.cos(psi) - xy_point[1] * np.sin(psi)
        y_rot = xy_point[0] * np.sin(psi) + xy_point[1] * np.cos(psi)

        # Translate x- and y-coordinate and add tuple to list
        xy_list_rot_tra.append((x_rot + x_tra, y_rot + y_tra))

    return xy_list_rot_tra


def get_aabb_polygon(trajectory: dict):
    """
    Function that returns the Axis Aligned Bounding Box (AABB) of a trajectory dictionary.

    inputs:
        trajectory (type: dict)

    output:
        aabb (type: shapely polygon)
    """

    # Subtask 1:
    # ToDo: Calculate the Axis Aligned Bounding Box (AABB) of a trajectory dictionary.
    #       The AABB should be a shapely polygon.
    # Hints:
    #   - Use shapely.ops.unary_union() for creating a union of all polygons
    #   - Use section "Constructive Methods" of shapely documentation for AABBs
    ########################
    #  Start of your code  #
    ########################

    vehicle_polygons = trajectory["vehicle_polygons"]
    trajectory_union = unary_union(vehicle_polygons)
    aabb = trajectory_union.envelope

    ########################
    #   End of your code   #
    ########################

    return aabb


def calculate_mbc_radius(rectangle_width: float, rectangle_length: float):
    """
    Function that returns the minimum bounding circle (MBC) radius of a rectangle.

    inputs:
        rectangle_width (type: float)
        rectangle_length (type: float)

    output:
        radius (type: float): radius of minimum bounding circle
    """
    # Subtask 2:
    # ToDo: Calculate the minimum bounding circle (MBC) radius of a rectangle.
    ########################
    #  Start of your code  #
    ########################

    diagonal_length = np.sqrt(rectangle_width ** 2 + rectangle_length ** 2)
    radius = diagonal_length / 2

    ########################
    #   End of your code   #
    ########################

    return radius


def check_circle_collision(xy1: np.ndarray, xy2: np.ndarray, r: float):
    """
    Function that checks for collision of two circles with the same radius r. The middle points of the
    circles are xy1 and xy2. Touching circles count also as collision.

    inputs:
        xy1 (type: np.ndarray (of floats)): x and y coordinate of the middle point of a circle
        xy2 (type: np.ndarray (of floats)): x and y coordinate of the middle point of a circle
        r (type: float): radius of both circles

    output:
        circle_collision (type: bool) "True" if collision detected, otherwise "False".
    """

    # Subtask 3:
    # ToDo: Check whether the given circles collide or not. Touching circles count also as collision.
    ########################
    #  Start of your code  #
    ########################

    distance = np.linalg.norm(xy2 - xy1)
    circle_collision = distance <= 2 * r

    ########################
    #   End of your code   #
    ########################

    return circle_collision


def polygon_collision_check(trajectory1: dict, trajectory2: dict):
    """
    Function that checks for collision of two trajectory dictionaries exactly.

    inputs:
        trajectory1 (type: dict)
        trajectory2 (type: dict)

    output:
        polygon_collision (type: bool): "True" if collision detected, otherwise "False".
    """

    # Subtask 4:
    # ToDo: Check exactly whether the given trajectories collide. The vehicle shall not be approximated.
    # Hint: Use section "Binary Predicates" of shapely documentation
    ########################
    #  Start of your code  #
    ########################

    polygons1 = trajectory1["vehicle_polygons"]
    polygons2 = trajectory2["vehicle_polygons"]
    trajectory_intersection = any(poly1.intersects(poly2) for poly1 in polygons1 for poly2 in polygons2)
    polygon_collision = trajectory_intersection

    ########################
    #   End of your code   #
    ########################

    return polygon_collision


def mbc_collision_check(trajectory1: dict, trajectory2: dict, mbc_radius: float,
                        given_circle_collision_check=check_circle_collision):
    """
    Function that checks for collision of two trajectory dictionaries by approximating the vehicle with a
    Minimum Bounding Circle.

    inputs:
        trajectory1 (type: dict)
        trajectory2 (type: dict)
        mbc_radius (type: float): radius of the minimum bounding circle
        given_circle_collision_check (type: function): given function which checks whether two circles collide

    output:
        mbc_collision (type: bool): "True" if collision detected, otherwise "False".
    """

    # Subtask 5:
    # ToDo: Check whether the given trajectories collide. The vehicle shall be approximated by the
    #       Minimum Bounding Circle with the radius mbc_radius. Use the function given_circle_collision_check().
    # Hint: Using the function 'given_circle_collision_check' ensures that you will still be able to pass this subtask
    #       on CodeFreak although your implementation of the function 'check_circle_collision' in subtask 3 is not
    #       working properly. However, the local implementation depends only on the functions you implement.
    ########################
    #  Start of your code  #
    ########################
    mbc_collision = False
    polygons1 = trajectory1["vehicle_polygons"]
    polygons2 = trajectory2["vehicle_polygons"]
    approx_radius = mbc_radius

    for i in range(len(polygons1)):
        xy1 = trajectory1["xy"][i]

        for j in range(len(polygons2)):
            xy2 = trajectory2["xy"][j]

            if given_circle_collision_check(xy1, xy2, approx_radius):
                mbc_collision = True

    ########################
    #   End of your code   #
    ########################

    return mbc_collision


def aabb_collision_check(aabb1: Polygon, aabb2: Polygon):
    """
    Function that checks for collision of two Axis Aligned Bounding Boxes, which are represented as
    shapely polygons.

    inputs:
        aabb1 (type: shapely polygon)
        aabb2 (type: shapely polygon)

    output:
        aabb_collision (type: bool): "True" if collision detected, otherwise "False".
    """

    # Subtask 6:
    # ToDo: Check whether the given Axis Aligned Bounding Boxes collide.
    # Hint: Use section "Binary Predicates" of shapely documentation
    ########################
    #  Start of your code  #
    ########################

    aabb_collision = aabb1.intersects(aabb2)

    ########################
    #   End of your code   #
    ########################

    return aabb_collision


def hierarchical_collision_check(traj1: dict, aabb1: Polygon, traj2: dict, aabb2: Polygon, mbc_radius: float,
                                 given_aabb_collision_check=aabb_collision_check,
                                 given_mbc_collision_check=mbc_collision_check,
                                 given_polygon_collision_check=polygon_collision_check):
    """
    Hierarchical collision checker which checks for collision of two trajectories.

    inputs:
        traj1 (type: dict): trajectory
        aabb1 (type: shapely polygon): Axis Aligned Bounding Box
        traj2 (type: dict): trajectory
        aabb2 (type: shapely polygon): Axis Aligned Bounding Box
        mbc_radius (type: float): minimum bounding circle radius of vehicle
        given_aabb_collision_check (type: function): given function which checks for collision of two AABBs
        given_mbc_collision_check (type: function): given function which checks for collision of two MBCs
        given_polygon_collision_check (type: function): given function which checks for collision of two trajectory
                                                        dictionaries exactly

    output:
        (type: tuple (of bool))
    """

    collision = None
    aabb_collision = None
    mbc_collision = None
    polygon_collision = None

    # Subtask 7:
    # ToDo: Implement a hierarchical collision checker, which checks for collision of two trajectory dictionaries.
    # Hints:
    # - The hierarchical check should be implemented with the following levels:
    #     1. Path collision check with AABBs (not OBB!) -> Use given_aabb_collision_check()
    #     2. Collision check based on MBC approximation -> Use given_mbc_collision_check()
    #     3. Exact collision check -> Use given_polygon_collision_check()
    # - Using the given functions ensures that you will still be able to pass this subtask on CodeFreak although your
    #   implementation of other subtasks is not working properly. However, the local implementation depends only on the
    #   functions you implement.
    # - For every collision check level a bool shall be returned, which are initialized to None. If one of the levels
    #   does not identify a collision, the following levels should not be executed. Example: The AABB collision check
    #   returns False -> The second and third level should not be executed (the booleans 'mbc_collision' and
    #   'polygon_collision' will remain None).
    # - The boolean 'collision' shall be the final decision of the collision checker. It has to be False or True and
    #   therefore should not be None.
    ########################
    #  Start of your code  #
    ########################

    aabb_collision = given_aabb_collision_check(aabb1, aabb2)

    if not aabb_collision:
        collision = False
        return collision, aabb_collision, mbc_collision, polygon_collision

    mbc_collision = given_mbc_collision_check(traj1, traj2, mbc_radius)

    if not mbc_collision:
        collision = False
        return collision, aabb_collision, mbc_collision, polygon_collision

    polygon_collision = given_polygon_collision_check(traj1, traj2)

    collision = polygon_collision

    ########################
    #   End of your code   #
    ########################

    return collision, aabb_collision, mbc_collision, polygon_collision


if __name__ == "__main__":

    # Width and length of vehicles
    width = 1.5
    length = 4.0

    # Get minimum bounding circle radius of vehicle
    mbc_radius = calculate_mbc_radius(rectangle_width=width, rectangle_length=length)

    # Generate two random trajectories
    trajectory1, trajectory2 = generate_trajectories(n=2, vehicle_width=width, vehicle_length=length)

    # Generate Axis Aligned Bounding Boxes out of the trajectories
    aabb1 = get_aabb_polygon(trajectory=trajectory1)
    aabb2 = get_aabb_polygon(trajectory=trajectory2)

    # Hierarchical collision check of trajectories
    collision, aabb_collision, mbc_collision, polygon_collision = hierarchical_collision_check(traj1=trajectory1,
                                                                                               aabb1=aabb1,
                                                                                               traj2=trajectory2,
                                                                                               aabb2=aabb2,
                                                                                               mbc_radius=mbc_radius)

    # Print collision results
    print(f'AABB Collision Check:     {aabb_collision}')
    print(f'MBC Collision Check:      {mbc_collision}')
    print(f'Exact Collision Check:    {polygon_collision}')
    print(f'Collision Detected:       {collision}')

    # Plot trajectories, vehicle polygons, Minimum Bounding Circles and Axis Aligned Bounding Boxes
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    for trajectory in [trajectory1, trajectory2]:
        ax.plot(trajectory['xy'][:, 0], trajectory['xy'][:, 1], 'bo-')

        for vehicle_polygon in trajectory['vehicle_polygons']:
            x, y = vehicle_polygon.exterior.xy
            ax.plot(x, y, '-r')

        # Plot MBC radii, if the radius exists
        if mbc_radius:
            for xy in trajectory['xy']:
                circle = plt.Circle(xy, mbc_radius, color='g', fill=False, linestyle='--')
                ax.add_patch(circle)

    # Plot AABBs, if the polygon objects exist
    if aabb1 and aabb2:
        x, y = aabb1.exterior.xy
        ax.plot(x, y, '--y')
        x, y = aabb2.exterior.xy
        ax.plot(x, y, '--y')

    plt.show()
