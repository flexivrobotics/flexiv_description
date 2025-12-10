#!/bin/bash
args=$*
shift $#
source /ros_entrypoint.sh
cd /workspaces
colcon build --packages-select flexiv_description > /dev/null
source install/setup.bash

LAUNCH_FILE=${LAUNCH_FILE:-view_rizon.launch.py}
ros2 launch flexiv_description $LAUNCH_FILE ${args}
