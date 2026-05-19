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
    single_arm_robot_types = [
        "EnlightL",
    ]
    pkg_share = FindPackageShare("flexiv_description")
    robot_sn = LaunchConfiguration("robot_sn")
    robot_type = LaunchConfiguration("robot_type")
    load_gripper = LaunchConfiguration("load_gripper")
    gripper_name = LaunchConfiguration("gripper_name")
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
                "gripper_name:=",
                gripper_name,
                " ",
                "load_mounted_ft_sensor:=",
                load_mounted_ft_sensor,
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
                name="robot_sn",
                description="Serial number of the robot to connect to. Remove any space, for example: EnlightL-123456",
            ),
            DeclareLaunchArgument(
                name="robot_type",
                default_value="EnlightL",
                description="Type of the Flexiv single-arm robot.",
                choices=single_arm_robot_types,
            ),
            DeclareLaunchArgument(
                name="load_gripper",
                default_value="False",
                description="Flag to load the Flexiv Grav gripper",
            ),
            DeclareLaunchArgument(
                name="gripper_name",
                default_value="Flexiv-GN01",
                description="Full name of the gripper to be controlled",
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
            joint_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
