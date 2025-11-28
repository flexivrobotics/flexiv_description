#!/bin/bash
args=$*
shift $#
source /ros_entrypoint.sh
cd /workspaces
colcon build --packages-select flexiv_description > /dev/null
source install/setup.bash

ros2 launch flexiv_description view_rizon.launch.py ${args}
