<p align="center">
  <img src="/img/logo.png" alt="" width="200"/>
</p>

# Scan Tools HC10

Créer un environnement `catkin`
```
mkdir -p catkin_ws/src
cd catkin_ws
. /opt/ros/noetic/setup.bash
```

Cloner notre repository
```
cd src 
git clone --branch master git@github.com:pierredaudin/Robotic-Integration.git
mv Robotic-Integration/yaskawa_moveit_V2/ .
mv Robotic-Integration/motoman_V2/ .
rm -r Robotic-Integration/
cd ..
```

Build le repo et lancer RViz
```
catkin config --extend /opt/ros/${ROS_DISTRO} --cmake-args -DCMAKE_BUILD_TYPE=Release
catkin build
source ~/catkin_ws/devel/setup.bash
echo 'source ~/catkin_ws/devel/setup.bash' >> ~/.bashrc
roslaunch yaskawa_moveit_V2 demo_gazebo.launch
```

Lancer le programme Python dans un autre terminal
```
# source ~/bashrc
cd src/yaskawa_moveit_V2/
chmod +x scan.py
rosrun yaskawa_moveit_V2 scan.py
```
