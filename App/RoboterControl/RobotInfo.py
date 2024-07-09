import numpy as np

# Axis movement maximum range in degrees
axis_limits = {
    'A': (-179.0, 179.0),  # rotation of the base
    'B': (-80.0, 140.0),
    'C': (-80.0, 140.0),
    'D': (-179.0, 179.0),  # rotation inside of the rod CToE
    'E': (-95.0, 95.0),
    'F': (-179.0, 179.0)   # rotation of the rod EToEnd on the end
}

# Sizes in mm
rod_lengths = {
    'BaseToB': 252,
    'BToC': 237,
    'CToE': 297,
    'EToEnd': 126
}

def check_range_of_motion(*axes):
    """Check if given axis movements are within the defined range."""
    adjusted_angles = [adjust_angle(axis, axis_limits[ax]) for axis, ax in zip(axes, 'ABCDEF')]
    return adjusted_angles, all(axis_limits[ax][0] <= angle <= axis_limits[ax][1] for angle, ax in zip(adjusted_angles, 'ABCDEF'))

def adjust_angle(angle, limits):
    """Adjust angle to be within limits."""
    low, high = limits
    return min(max(angle, low), high)

def rotate_vector_3d(vector_start, vector_end, point, angle_x, angle_y, angle_z):
    """Transform the vector."""
    theta_x = np.radians(angle_x)
    theta_y = np.radians(angle_y)
    phi_z = np.radians(angle_z)
    
    # Translate vector to the origin
    translated_start = np.array(vector_start) - np.array(point)
    translated_end = np.array(vector_end) - np.array(point)
    
    # Rotation matrix around the x-axis
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x)],
        [0, np.sin(theta_x), np.cos(theta_x)]
    ])
    
    # Rotation matrix around the y-axis
    rotation_matrix_y = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])
    
    # Rotation matrix around the z-axis
    rotation_matrix_z = np.array([
        [np.cos(phi_z), -np.sin(phi_z), 0],
        [np.sin(phi_z), np.cos(phi_z), 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix
    combined_rotation_matrix = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))
    
    # Rotate the vector
    rotated_end = np.dot(combined_rotation_matrix, translated_end)
    
    # Translate the vector back to its original position
    final_start = translated_start + np.array(point)
    final_end = rotated_end + np.array(point)
    formatted_final_end = tuple(map(float, final_end))

    return final_start, formatted_final_end

def find_point_on_vector(start, end, distance):
    """Find a point at a specific distance along a vector."""
    direction = np.array(end) - np.array(start)
    direction_unit = direction / np.linalg.norm(direction)
    return np.array(start) + distance * direction_unit
    

def create_rotation_matrix_from_vector(vector):
    """Create a rotation matrix that aligns the z-axis with the given vector."""
    # Normalize the vector
    vector = vector / np.linalg.norm(vector)
    z_axis = np.array([0, 0, 1])
    
    # Compute the cross product and the sine of the angle
    cross_prod = np.cross(z_axis, vector)
    sin_angle = np.linalg.norm(cross_prod)
    cos_angle = np.dot(z_axis, vector)
    
    # Create the skew-symmetric cross-product matrix
    skew_sym_matrix = np.array([
        [0, -cross_prod[2], cross_prod[1]],
        [cross_prod[2], 0, -cross_prod[0]],
        [-cross_prod[1], cross_prod[0], 0]
    ])
    
    # Compute the rotation matrix using the Rodrigues' rotation formula
    rotation_matrix = (
        np.eye(3) +
        skew_sym_matrix +
        np.dot(skew_sym_matrix, skew_sym_matrix) * ((1 - cos_angle) / (sin_angle ** 2))
    )
    
    return rotation_matrix

def getPosition(a, b, c, d, e, f, robot):
    vector_start = (0.0, 0.0, rod_lengths['BaseToB'])
    vector_end = (0.0, 0.0, sum(rod_lengths.values()))  # Initial end point

    if robot == 'IGUSREBEL6':
        # First transformation (Rotation with axis B)
        new_start, new_end = rotate_vector_3d(vector_start, vector_end, vector_start, 0, b, 0)
        point_at_distance = find_point_on_vector(new_start, new_end, rod_lengths['BToC'])
        formatted_point_at_distance = tuple(map(float, point_at_distance))

        # Second transformation (Rotation with axis C)
        new_start2, new_end2 = rotate_vector_3d(formatted_point_at_distance, new_end, formatted_point_at_distance, 0, c, 0)
        point_at_distance2 = find_point_on_vector(new_start2, new_end2, rod_lengths['CToE'])
        formatted_point_at_distance2 = tuple(map(float, point_at_distance2))

        # Third transformation (Rotation with axis E)
        new_start3, new_end3 = rotate_vector_3d(formatted_point_at_distance2, new_end2, formatted_point_at_distance2, 0, e, 0)

        # Forth transformation (Rotation with axis D)
        new_start4, new_end4 = rotate_vector_3d(formatted_point_at_distance2, new_end3, formatted_point_at_distance2, d, 0, 0)
        point_at_distanc4 = find_point_on_vector(new_start4, new_end4, rod_lengths['EToEnd'])
        formatted_point_at_distance4 = tuple(map(float, point_at_distanc4))

        # Fith transformation (Rotation with axis A)
        new_start5, new_end5 = rotate_vector_3d(vector_start, formatted_point_at_distance4, vector_start, 0, 0, a)
        
    return new_end5


a, b, c, d, e, f = 30, 45, 60, 90, 10, 15
adjusted_angles, outOfMotion = check_range_of_motion(a, b, c, d, e, f)
print(getPosition(*adjusted_angles, 'IGUSREBEL6'))

'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
def plotOut():

    formatted_new_end3 = tuple(map(float, new_end3))
    np.set_printoptions(precision=2, suppress=True)


    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Transformed vectors
    ax.plot([new_start[0], point_at_distance[0]], [new_start[1], point_at_distance[1]], [new_start[2], point_at_distance[2]], label='Transformed Vector 1', color='red')
    ax.plot([point_at_distance[0], point_at_distance2[0]], [point_at_distance[1], point_at_distance2[1]], [point_at_distance[2], point_at_distance2[2]], label='Transformed Vector 2', color='blue')
    #ax.plot([point_at_distance2[0], point_at_distance4[0]], [point_at_distance2[1], point_at_distance4[1]], [point_at_distance2[2], point_at_distance4[2]], label='Transformed Vector 3', color='green')
    
    # Points at distances
    ax.scatter(*vector_start, color='orange')
    ax.scatter(*formatted_point_at_distance, color='green')
    ax.scatter(*formatted_point_at_distance2, color='green')
    ax.scatter(*formatted_point_at_distance4, color='green')
    ax.scatter(*formatted_new_end3, color='orange')
    ax.plot([formatted_new_end3[0], formatted_point_at_distance4[0]], [formatted_new_end3[1], formatted_point_at_distance4[1]], [formatted_new_end3[2], formatted_point_at_distance4[2]], label='Transformed Vector 1', color='pink')

    # Calculate circle parameters
    z_coord = formatted_point_at_distance4[2]
    radius = np.sqrt(formatted_point_at_distance4[0]**2 + formatted_point_at_distance4[1]**2)

    # Generate circle points
    theta = np.linspace(0, 2 * np.pi, 100)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    z_circle = np.full_like(theta, z_coord)

    # Plot the circle
    ax.plot(x_circle, y_circle, z_circle, label='Circle', color='purple')

    # Plot the vector (0, 0, 0) to (0, 0, 252) in thick orange line
    ax.plot([0, 0], [0, 0], [0, 252], label='Fixed Vector', color='orange', linewidth=3)

    # Labels and legend
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    x_limit = 600
    y_limit = 600
    z_limit = 950
    ax.set_xlim([-x_limit, x_limit])
    ax.set_ylim([-y_limit, y_limit])
    ax.set_zlim([0, z_limit])


    plt.show()

'''
