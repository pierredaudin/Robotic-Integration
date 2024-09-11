# Robotic Integration

Créer un environnement `catkin`
```
mkdir -p catkin_ws/src
cd catkin_ws
. /opt/ros/noetic/setup.bash
```

Cloner le dépôt contenant le modèle du robot HC10
```
cd src
git clone https://github.com/ros-industrial/motoman.git
cd ..
catkin build
. devel/setup.bash
```

Cloner notre repository
```
git clone --branch master git@github.com:pierredaudin/Robotic-Integration.git
cd ~/Robotic-Integration/catkin_ws/
source ~/Robotic-Integration/catkin_ws/devel/setup.bash
```

Build le repo
```
catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release
catkin build
source ~/Robotic-Integration/catkin_ws/devel/setup.bash
echo 'source ~/Robotic-Integration/catkin_ws/devel/setup.bash' >> ~/.bashrc
```

## Environnement de simulation

### MoveIt Quickstart in RViz
- Test de la mobilité des joint pour vérifier la bonne configuration du xacro via le setup assistant Moveit
- Planification d'une trajectoire quelconque pour vérifier que la configuration est stable
- Ajout d'un objet obstuant la trajectoire
- Re-plannification de la trajectoire
- Execution de la trajectoire
- Conclusion : La planification + execution de la trajectoire évite l'objet importé

### Gazebo
- Ajout des controlleurs via le setup assistant MoveIt
- Copier-Coller le XML généré dans un fichier xacro indépendant "hc10_control"
- Lancer la commande
```
rosrun ...
```

### Move Group Python Interface
- Ouvrir un termial et lancer la demo sur RViz 
```
roslaunch hc10_moveit_config demo.launch
```
- Récuperer le [code python](https://github.com/moveit/moveit_tutorials/blob/master/doc/move_group_python_interface/scripts/move_group_python_interface_tutorial.py) et modifier les "panda" par des "hc10"
- Ouvrir un second terminal et lancer le code python
```
rosrun hc10_moveit_config move_group_python_interface_tutorial.py
```

## Génération de trajectoire
- Adapter le code pour planifier une position donnée (rappel on doit se baser sur le capteur - prévoir une sorte de PID pour se positionner à une certaine distance de l'objet capté)

## Capteurs
- ...

*Check [MoveIt tutorial documentation for ROS Noetic](https://moveit.github.io/moveit_tutorials/)*

