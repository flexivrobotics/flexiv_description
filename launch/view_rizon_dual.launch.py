from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
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


def generate_launch_description():
    pkg_share = FindPackageShare("flexiv_description")

    robot_sn_left = LaunchConfiguration("robot_sn_left")
    rizon_type_left = LaunchConfiguration("rizon_type_left")
    load_gripper_left = LaunchConfiguration("load_gripper_left")
    gripper_name_left = LaunchConfiguration("gripper_name_left")
    load_mounted_ft_sensor_left = LaunchConfiguration("load_mounted_ft_sensor_left")

    robot_sn_right = LaunchConfiguration("robot_sn_right")
    rizon_type_right = LaunchConfiguration("rizon_type_right")
    load_gripper_right = LaunchConfiguration("load_gripper_right")
    gripper_name_right = LaunchConfiguration("gripper_name_right")
    load_mounted_ft_sensor_right = LaunchConfiguration("load_mounted_ft_sensor_right")

    default_rviz_config_path = PathJoinSubstitution(
        [pkg_share, "rviz", "view_rizon_dual.rviz"]
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
                        "rizon_dual.urdf.xacro",
                    ]
                ),
                " ",
                "robot_sn_left:=",
                robot_sn_left,
                " ",
                "robot_sn_right:=",
                robot_sn_right,
                " ",
                "rizon_type_left:=",
                rizon_type_left,
                " ",
                "rizon_type_right:=",
                rizon_type_right,
                " ",
                "load_gripper_left:=",
                load_gripper_left,
                " ",
                "load_gripper_right:=",
                load_gripper_right,
                " ",
                "gripper_name_left:=",
                gripper_name_left,
                " ",
                "gripper_name_right:=",
                gripper_name_right,
                " ",
                "load_mounted_ft_sensor_left:=",
                load_mounted_ft_sensor_left,
                " ",
                "load_mounted_ft_sensor_right:=",
                load_mounted_ft_sensor_right,
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

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        condition=UnlessCondition(LaunchConfiguration("gui")),
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        condition=IfCondition(LaunchConfiguration("gui")),
    )

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
                name="robot_sn_left",
                description="Serial number of the left robot.",
            ),
            DeclareLaunchArgument(
                name="robot_sn_right",
                description="Serial number of the right robot.",
            ),
            DeclareLaunchArgument(
                name="rizon_type_left",
                default_value="Rizon4",
                description="Type of the left Flexiv Rizon robot.",
                choices=[
                    "Rizon4",
                    "Rizon4M",
                    "Rizon4R",
                    "Rizon4s",
                    "Rizon10",
                    "Rizon10s",
                ],
            ),
            DeclareLaunchArgument(
                name="rizon_type_right",
                default_value="Rizon4",
                description="Type of the right Flexiv Rizon robot.",
                choices=[
                    "Rizon4",
                    "Rizon4M",
                    "Rizon4R",
                    "Rizon4s",
                    "Rizon10",
                    "Rizon10s",
                ],
            ),
            DeclareLaunchArgument(
                name="load_gripper_left",
                default_value="False",
                description="Flag to load the Flexiv Grav gripper for left robot",
            ),
            DeclareLaunchArgument(
                name="load_gripper_right",
                default_value="False",
                description="Flag to load the Flexiv Grav gripper for right robot",
            ),
            DeclareLaunchArgument(
                name="gripper_name_left",
                default_value="Flexiv-GN01",
                description="Full name of the gripper to be controlled for left robot",
            ),
            DeclareLaunchArgument(
                name="gripper_name_right",
                default_value="Flexiv-GN01",
                description="Full name of the gripper to be controlled for right robot",
            ),
            DeclareLaunchArgument(
                name="load_mounted_ft_sensor_left",
                default_value="False",
                description="Flag to load the mounted force torque sensor for left robot. Only available for Rizon4, Rizon4R and Rizon10",
            ),
            DeclareLaunchArgument(
                name="load_mounted_ft_sensor_right",
                default_value="False",
                description="Flag to load the mounted force torque sensor for right robot. Only available for Rizon4, Rizon4R and Rizon10",
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
            joint_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
