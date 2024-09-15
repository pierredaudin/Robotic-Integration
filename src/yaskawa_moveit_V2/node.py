#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
from math import pi, cos, sin, atan2, sqrt
import numpy as np
import tf

def quaternion_from_rotation_matrix(R):
    """ Convert a 3x3 rotation matrix to a quaternion (q_w, q_x, q_y, q_z) """
    trace = np.trace(R)
    
    if trace > 0:
        S = np.sqrt(trace + 1.0) * 2  # S=4*q_w
        q_w = 0.25 * S
        q_x = (R[2, 1] - R[1, 2]) / S
        q_y = (R[0, 2] - R[2, 0]) / S
        q_z = (R[1, 0] - R[0, 1]) / S
    elif (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
        S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2  # S=4*q_x
        q_w = (R[2, 1] - R[1, 2]) / S
        q_x = 0.25 * S
        q_y = (R[0, 1] + R[1, 0]) / S
        q_z = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2  # S=4*q_y
        q_w = (R[0, 2] - R[2, 0]) / S
        q_x = (R[0, 1] + R[1, 0]) / S
        q_y = 0.25 * S
        q_z = (R[1, 2] + R[2, 1]) / S
    else:
        S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2  # S=4*q_z
        q_w = (R[1, 0] - R[0, 1]) / S
        q_x = (R[0, 2] + R[2, 0]) / S
        q_y = (R[1, 2] + R[2, 1]) / S
        q_z = 0.25 * S

    return np.array([q_w, q_x, q_y, q_z])

def calculate_rotation_matrix(arm_position, object_position):
    """ Compute a rotation matrix that aligns the camera to point towards the object """
    direction = np.array(object_position) - np.array(arm_position)
    direction = direction / np.linalg.norm(direction)  # Normalize the direction vector

    # Assume that the Z-axis of the camera should point towards the object
    # Construct a rotation matrix where the Z-axis aligns with the direction vector
    up = np.array([0, 0, 1])  # Up vector (can be adjusted if needed)
    z_axis = direction
    x_axis = np.cross(up, z_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)  # Normalize the X-axis
    y_axis = np.cross(z_axis, x_axis)

    # Rotation matrix aligning the Z-axis with the direction to the object
    R = np.array([x_axis, y_axis, z_axis]).T  # Build the matrix

    return R

def move_to_initial_configuration(move_group):
    initial_joint_values = move_group.get_current_joint_values()
    initial_joint_values[0] = 0.0
    initial_joint_values[1] = 0
    initial_joint_values[2] = 0.0
    initial_joint_values[3] = 0
    initial_joint_values[4] = 0
    initial_joint_values[5] = 0
    move_group.set_joint_value_target(initial_joint_values)
    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    return plan

def move_group_scan_with_kinect(center_x, center_y, center_z, radius, height, num_points=36):

    # Paramètres de balayage
    object_center_x = center_x  # Coordonnée X du centre de l'objet
    object_center_y = center_y # Coordonnée Y du centre de l'objet
    object_center_z = center_z  # Hauteur (Z) de l'objet
    object_radius = radius  # Rayon du cercle de balayage
    object_height = height  # Hauteur à laquelle le bras doit rester pendant le balayage
    object_num_points = num_points  # Nombre de points autour du cercle

    print("Moving to initial configuration...")
    success_initial = move_to_initial_configuration(move_group)

    if success_initial:
        print("Successfully moved to initial configuration.")
    else:
        print("Failed to move to initial configuration.")
        return


    # Créer une liste de waypoints pour la trajectoire
    waypoints = []

    object_center = [object_center_x, object_center_y, object_center_z]

    # Générer les points autour du cercle
    for i in range(object_num_points):
        angle = 2 * pi * i / object_num_points  # Convertir l'angle en radians
        x = object_center_x + object_radius * cos(angle)
        y = object_center_y + object_radius * sin(angle)
        z = object_height

        # Calculer la matrice de rotation pour aligner la Kinect vers l'objet
        arm_position = [x, y, z]
        rotation_matrix = calculate_rotation_matrix(arm_position, object_center)

        # Convertir la matrice de rotation en quaternion
        quaternion = quaternion_from_rotation_matrix(rotation_matrix)

        # Définir la pose du bras à ce point
        pose = geometry_msgs.msg.Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        pose.orientation.x = quaternion[1]  # q_x
        pose.orientation.y = quaternion[2]  # q_y
        pose.orientation.z = quaternion[3]  # q_z
        pose.orientation.w = quaternion[0]  # q_w

        waypoints.append(pose)

    # Générer et exécuter la trajectoire
    (plan, fraction) = move_group.compute_cartesian_path(waypoints, 0.01, 0.0)  # Précision de 1 cm
    move_group.execute(plan, wait=True)
    # success_initial = move_to_initial_configuration(move_group)

if __name__ == '__main__':
    try:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_scan_with_kinect', anonymous=True)

        # Initialisation du move_group pour le bras manipulateur
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "robot"  # Remplace par le nom du groupe du bras HC10 si nécessaire
        move_group = moveit_commander.MoveGroupCommander(group_name)
        move_to_initial_configuration(move_group)
        move_group_scan_with_kinect(0, 0.4, 0.4, 0.2, 0.6)
        move_group_scan_with_kinect(0, 0.4, 0.3, 0.4, 0.4)
        moveit_commander.roscpp_shutdown()

    except rospy.ROSInterruptException:
        pass