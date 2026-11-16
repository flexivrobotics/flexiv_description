import math
import os
import re

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

# Grav Enhanced A mode input (a_mode_angle_joint) starts just past P mode's 100 mm
A_MODE_START_ANGLE = math.radians(120.0)


def load_robot_types():
    """Load the robot types grouped by hardware topology.

    config/robot_types.yaml is the single source of truth, shared with
    scripts/create_urdf.py.
    """
    path = os.path.join(
        get_package_share_directory("flexiv_description"), "config", "robot_types.yaml"
    )
    with open(path) as f:
        return yaml.safe_load(f)


def load_gripper_types():
    """Load the gripper types.

    config/gripper_types.yaml is the single source of truth, shared with
    urdf/common/flexiv_robot.xacro and scripts/create_urdf.py.
    """
    path = os.path.join(
        get_package_share_directory("flexiv_description"),
        "config",
        "gripper_types.yaml",
    )
    with open(path) as f:
        return yaml.safe_load(f)["gripper_types"]


def generate_launch_description():
    robot_type_groups = load_robot_types()
    robot_types = [t for group in robot_type_groups.values() for t in group]
    paired_types = robot_type_groups["paired"]
    gripper_types = load_gripper_types()
    pkg_share = FindPackageShare("flexiv_description")
    robot_sn = LaunchConfiguration("robot_sn")
    robot_type = LaunchConfiguration("robot_type")
    load_gripper = LaunchConfiguration("load_gripper")
    gripper_type = LaunchConfiguration("gripper_type")
    load_mounted_ft_sensor = LaunchConfiguration("load_mounted_ft_sensor")
    default_rviz_config_path = PathJoinSubstitution(
        [pkg_share, "rviz", "view_flexiv.rviz"]
    )
    robot_description_content = ParameterValue(
        Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                PathJoinSubstitution(
                    [
                        FindPackageShare("flexiv_description"),
                        "urdf",
                        "flexiv.urdf.xacro",
                    ]
                ),
                " ",
                "robot_sn:=",
                robot_sn,
                " ",
                "robot_type:=",
                robot_type,
                " ",
                "load_gripper:=",
                load_gripper,
                " ",
                "gripper_type:=",
                gripper_type,
                " ",
                "load_mounted_ft_sensor:=",
                load_mounted_ft_sensor,
                # robot_type is only known at runtime, so pass the arguments for
                # every topology. flexiv.urdf.xacro declares them all and reads
                # only the ones its selected branch needs.
                " ",
                "robot_sn_left:=",
                LaunchConfiguration("robot_sn_left"),
                " ",
                "robot_sn_right:=",
                LaunchConfiguration("robot_sn_right"),
                " ",
                "arm_type:=",
                LaunchConfiguration("arm_type"),
                " ",
                "arm_type_left:=",
                LaunchConfiguration("arm_type_left"),
                " ",
                "arm_type_right:=",
                LaunchConfiguration("arm_type_right"),
                " ",
                "external_axis_prefix:=",
                LaunchConfiguration("external_axis_prefix"),
            ]
        ),
        value_type=str,
    )

    # Robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}],
    )

    def joint_state_publishers(context):
        urdf = robot_description_content.evaluate(context)
        start_values = {
            f"zeros.{name}": A_MODE_START_ANGLE
            for name in re.findall(r'<joint name="([^"]*a_mode_angle_joint)"', urdf)
        }
        return [
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                parameters=[start_values],
                condition=UnlessCondition(LaunchConfiguration("gui")),
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                parameters=[start_values],
                condition=IfCondition(LaunchConfiguration("gui")),
            ),
        ]

    # RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="robot_sn",
                default_value="",
                description="Serial number of the robot. Remove any space, for example: Enlight-L-123456. "
                f"Leave empty for the paired types ({', '.join(paired_types)}), which use robot_sn_left and robot_sn_right instead.",
            ),
            DeclareLaunchArgument(
                name="robot_type",
                default_value="Enlight-L",
                description="Type of the Flexiv robot. See config/robot_types.yaml for the "
                "topology each type belongs to and the arguments it reads.",
                choices=robot_types,
            ),
            DeclareLaunchArgument(
                name="robot_sn_left",
                default_value="",
                description="Left robot serial number. Required by the paired types.",
            ),
            DeclareLaunchArgument(
                name="robot_sn_right",
                default_value="",
                description="Right robot serial number. Required by the paired types.",
            ),
            DeclareLaunchArgument(
                name="arm_type",
                default_value="",
                description="Arm carried by an AICO1 external axis. Empty picks the axis default.",
            ),
            DeclareLaunchArgument(
                name="arm_type_left",
                default_value="",
                description="Left arm type for the paired types. Empty picks the default.",
            ),
            DeclareLaunchArgument(
                name="arm_type_right",
                default_value="",
                description="Right arm type for the paired types. Empty picks the default.",
            ),
            DeclareLaunchArgument(
                name="external_axis_prefix",
                default_value="",
                description="Prefix for external axis links and joints (AICO types).",
            ),
            DeclareLaunchArgument(
                name="load_gripper",
                default_value="False",
                description="Flag to load the gripper selected by gripper_type",
            ),
            DeclareLaunchArgument(
                name="gripper_type",
                default_value="Grav",
                description="Type of the gripper. See config/gripper_types.yaml.",
                choices=gripper_types,
            ),
            DeclareLaunchArgument(
                name="load_mounted_ft_sensor",
                default_value="False",
                description="Flag to load the mounted force torque sensor.",
            ),
            DeclareLaunchArgument(
                name="gui",
                default_value="False",
                description="Flag to enable joint_state_publisher_gui",
            ),
            DeclareLaunchArgument(
                name="rvizconfig",
                default_value=default_rviz_config_path,
                description="Absolute path to rviz config file",
            ),
            robot_state_publisher_node,
            OpaqueFunction(function=joint_state_publishers),
            rviz_node,
        ]
    )
