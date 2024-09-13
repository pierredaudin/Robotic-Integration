import rospy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import PoseStamped, Point, Vector3
from tf.transformations import quaternion_from_matrix
import numpy as np

def create_look_at_constraint(frame_id, link_name, target_point):
    constraint = moveit_msgs.msg.Constraints()
    orientation_constraint = moveit_msgs.msg.OrientationConstraint()
    
    orientation_constraint.link_name = link_name
    orientation_constraint.header.frame_id = frame_id
    
    # Calculer la matrice de rotation pour que l'axe Z pointe vers la cible
    z_axis = np.array(target_point) - np.array([0, 0, 0])  # Vecteur de l'origine vers la cible
    z_axis = z_axis / np.linalg.norm(z_axis)  # Normaliser
    x_axis = np.array([1, 0, 0])  # Choisir un axe X arbitraire
    y_axis = np.cross(z_axis, x_axis)  # Calculer l'axe Y perpendiculaire
    x_axis = np.cross(y_axis, z_axis)  # Recalculer l'axe X pour s'assurer de l'orthogonalité
    
    # Créer la matrice de rotation
    rotation_matrix = np.column_stack((x_axis, y_axis, z_axis, [0, 0, 0]))
    rotation_matrix = np.vstack((rotation_matrix, [0, 0, 0, 1]))
    
    # Convertir en quaternion
    q = quaternion_from_matrix(rotation_matrix)
    orientation_constraint.orientation.x, orientation_constraint.orientation.y, orientation_constraint.orientation.z, orientation_constraint.orientation.w = q
    
    # Définir les tolérances (permettre une rotation autour de l'axe Z)
    orientation_constraint.absolute_x_axis_tolerance = 3.14  # Permettre une rotation complète
    orientation_constraint.absolute_y_axis_tolerance = 3.14  # Permettre une rotation complète
    orientation_constraint.absolute_z_axis_tolerance = 0.1   # Limiter la rotation autour de Z
    orientation_constraint.weight = 1.0
    
    constraint.orientation_constraints.append(orientation_constraint)
    return constraint

# Initialisation de ROS et MoveIt
rospy.init_node('point_orientation_node')
robot = moveit_commander.RobotCommander()
group = moveit_commander.MoveGroupCommander("arm")  # Remplacez "arm" par le nom de votre groupe

# Point cible
target_point = Point(1, 1, 1)

# Créer la contrainte
constraint = create_look_at_constraint("base_link", "end_effector_link", [target_point.x, target_point.y, target_point.z])

# Appliquer la contrainte
group.set_path_constraints(constraint)

# Définir plusieurs poses cibles autour du point (1, 1, 1)
radius = 0.5  # Rayon du cercle autour du point cible
for angle in range(0, 360, 45):  # 8 points autour du cercle
    x = target_point.x + radius * np.cos(np.radians(angle))
    y = target_point.y + radius * np.sin(np.radians(angle))
    z = target_point.z
    
    target_pose = PoseStamped()
    target_pose.header.frame_id = "base_link"
    target_pose.pose.position = Point(x, y, z)
    
    # L'orientation sera ajustée par la contrainte
    target_pose.pose.orientation.w = 1.0

    # Planifier et exécuter le mouvement
    group.set_pose_target(target_pose)
    plan = group.plan()
    if plan[0]:  # Vérifier si la planification a réussi
        group.execute(plan, wait=True)
    else:
        rospy.logwarn(f"Impossible de planifier le mouvement vers la position ({x}, {y}, {z})")

    rospy.sleep(1)  # Pause entre chaque mouvement

# Nettoyer
group.clear_pose_targets()
group.clear_path_constraints()