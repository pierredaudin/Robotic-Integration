# CMake generated Testfile for 
# Source directory: /home/etudiant/catkin_ws/src/motoman/motoman_driver
# Build directory: /home/etudiant/catkin_ws/build/motoman_driver
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_motoman_driver_roslint_package "/home/etudiant/catkin_ws/build/motoman_driver/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/etudiant/catkin_ws/build/motoman_driver/test_results/motoman_driver/roslint-motoman_driver.xml" "--working-dir" "/home/etudiant/catkin_ws/build/motoman_driver" "--return-code" "/opt/ros/noetic/share/roslint/cmake/../../../lib/roslint/test_wrapper /home/etudiant/catkin_ws/build/motoman_driver/test_results/motoman_driver/roslint-motoman_driver.xml make roslint_motoman_driver")
set_tests_properties(_ctest_motoman_driver_roslint_package PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/roslint/cmake/roslint-extras.cmake;67;catkin_run_tests_target;/home/etudiant/catkin_ws/src/motoman/motoman_driver/CMakeLists.txt;287;roslint_add_test;/home/etudiant/catkin_ws/src/motoman/motoman_driver/CMakeLists.txt;0;")
add_test(_ctest_motoman_driver_roslaunch-check_tests_roslaunch_test_io_relay.xml "/home/etudiant/catkin_ws/build/motoman_driver/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/etudiant/catkin_ws/build/motoman_driver/test_results/motoman_driver/roslaunch-check_tests_roslaunch_test_io_relay.xml.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/etudiant/catkin_ws/build/motoman_driver/test_results/motoman_driver" "/opt/ros/noetic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/etudiant/catkin_ws/build/motoman_driver/test_results/motoman_driver/roslaunch-check_tests_roslaunch_test_io_relay.xml.xml\" \"/home/etudiant/catkin_ws/src/motoman/motoman_driver/tests/roslaunch_test_io_relay.xml\" ")
set_tests_properties(_ctest_motoman_driver_roslaunch-check_tests_roslaunch_test_io_relay.xml PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/roslaunch/cmake/roslaunch-extras.cmake;66;catkin_run_tests_target;/home/etudiant/catkin_ws/src/motoman/motoman_driver/CMakeLists.txt;290;roslaunch_add_file_check;/home/etudiant/catkin_ws/src/motoman/motoman_driver/CMakeLists.txt;0;")
subdirs("gtest")
