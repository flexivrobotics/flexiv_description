# flexiv_description

URDF description for Flexiv robots.

## URDF Creation

The URDF files for Flexiv robots can be generated from xacro files using the provided script. This script runs inside a Docker container to ensure a consistent environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

### Usage

Run the `create_urdf.sh` script from the package root directory:

```bash
./scripts/create_urdf.sh --robot_type <ROBOT_TYPE> [OPTIONS]
```

### Parameters

```
usage: create_urdf.py [-h] [--robot_type ROBOT_TYPE]
                      [--arm_prefix ARM_PREFIX] [--robot_sn ROBOT_SN]
                      [--load_gripper] [--gripper_name GRIPPER_NAME]
                      [--load_mounted_ft_sensor]

Create URDF files from xacro for Flexiv robots.

optional arguments:
  -h, --help            show this help message and exit
  --robot_type ROBOT_TYPE
                        Single-arm robot type. Options: ['EnlightL']. (default: 'EnlightL')
  --arm_prefix ARM_PREFIX
                        Arm prefix. (default: '')
  --robot_sn ROBOT_SN   Robot serial number. (default: '')
  --load_gripper        Load gripper. (default: False)
  --gripper_name GRIPPER_NAME
                        Gripper name. (default: 'Flexiv-GN01')
  --load_mounted_ft_sensor
                        Load mounted FT sensor. (default: False)
```

### Examples

Generate URDF for EnlightL:

```bash
./scripts/create_urdf.sh --robot_type EnlightL
```

Generate URDF for EnlightL with a specific serial number:

```bash
./scripts/create_urdf.sh --robot_type EnlightL --robot_sn EnlightL-123456
```

Generate URDF for EnlightL with gripper:

```bash
./scripts/create_urdf.sh --robot_type EnlightL --robot_sn EnlightL-123456 --load_gripper
```

## Visualize in RViz

The robot models can be visualized in RViz using the provided script. This script runs inside a Docker container and requires a GUI environment.

```
usage: visualize_flexiv.sh [OPTIONS]

Visualize Flexiv robots in RViz.

Arguments:
  robot_sn:=ROBOT_SN            Serial number of the robot to connect to.
  robot_type:=TYPE              Type of the Flexiv single-arm robot. (default: 'EnlightL')
  load_gripper:=BOOL            Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name:=NAME            Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor:=BOOL  Flag to load the mounted force torque sensor. (default: 'False')
  gui:=BOOL                     Flag to enable joint_state_publisher_gui. (default: 'False')
```

Visualize EnlightL:

```bash
./scripts/visualize_flexiv.sh robot_type:=EnlightL robot_sn:=EnlightL-123456 gui:=True
```

> [!NOTE]
> The launch files can also be run directly using `ros2 launch` if the package is built and sourced in your ROS 2 workspace.
