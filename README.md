# flexiv_description

URDF description for Flexiv robots

## URDF Creation

The URDF files for Flexiv robots can be generated from xacro files using the provided script. This script runs inside a Docker container to ensure a consistent environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

### Usage

Run the `create_urdf.sh` script from the package root directory:

```bash
./scripts/create_urdf.sh --rizon_type <RIZON_TYPE> [OPTIONS]
```

### Parameters

```
usage: create_urdf.py [-h] [--dual] [--aico1] [--aico2]
                      [--rizon_type RIZON_TYPE]
                      [--arm_prefix ARM_PREFIX] [--robot_sn ROBOT_SN]
                      [--external_axis_type EXTERNAL_AXIS_TYPE] [--external_axis_prefix EXTERNAL_AXIS_PREFIX]
                      [--load_gripper] [--gripper_name GRIPPER_NAME]
                      [--load_mounted_ft_sensor]
                      [--rizon_type_left RIZON_TYPE_LEFT]
                      [--rizon_type_right RIZON_TYPE_RIGHT]
                      [--robot_sn_left ROBOT_SN_LEFT]
                      [--robot_sn_right ROBOT_SN_RIGHT] [--load_gripper_left]
                      [--load_gripper_right]
                      [--gripper_name_left GRIPPER_NAME_LEFT]
                      [--gripper_name_right GRIPPER_NAME_RIGHT]
                      [--load_mounted_ft_sensor_left]
                      [--load_mounted_ft_sensor_right]

Create URDF files from xacro for Flexiv robots.

optional arguments:
  -h, --help            show this help message and exit
  --dual                Generate URDF for dual arm setup.
  --aico1               Generate URDF for AICO1 setup.
  --aico2               Generate URDF for AICO2 setup.
  --rizon_type RIZON_TYPE
                        Rizon robot type (Single arm). Options: ['Rizon4', 'Rizon4s', 'Rizon4M', 'Rizon4R', 'Rizon10', 'Rizon10s'].
  --arm_prefix ARM_PREFIX
                        Arm prefix. (default: '')
  --robot_sn ROBOT_SN   Robot serial number. (default: '')
  --load_gripper        Load gripper. (default: False)
  --gripper_name GRIPPER_NAME
                        Gripper name. (default: 'Flexiv-GN01')
  --load_mounted_ft_sensor
                        Load mounted FT sensor. (default: False)

AICO arguments:
  --external_axis_type EXTERNAL_AXIS_TYPE
                        External axis type. Options: ['AICO1-4-V1', 'AICO1-4-V2', 'AICO2-4-V2', 'AICO2-10-V1'].
  --external_axis_prefix EXTERNAL_AXIS_PREFIX
                        External axis prefix. (default: '')

Dual arm or AICO2 arguments:
  --rizon_type_left RIZON_TYPE_LEFT
                        Left Rizon robot type.
  --rizon_type_right RIZON_TYPE_RIGHT
                        Right Rizon robot type.
  --robot_sn_left ROBOT_SN_LEFT
                        Left robot serial number.
  --robot_sn_right ROBOT_SN_RIGHT
                        Right robot serial number.
  --load_gripper_left   Load gripper for left robot.
  --load_gripper_right  Load gripper for right robot.
  --gripper_name_left GRIPPER_NAME_LEFT
                        Gripper name for left robot.
  --gripper_name_right GRIPPER_NAME_RIGHT
                        Gripper name for right robot.
  --load_mounted_ft_sensor_left
                        Load mounted FT sensor for left robot.
  --load_mounted_ft_sensor_right
                        Load mounted FT sensor for right robot.
```

### Examples

Generate URDF for Rizon4:

```bash
./scripts/create_urdf.sh --rizon_type Rizon4
```

Generate URDF for Rizon4 with a specific serial number:

```bash
./scripts/create_urdf.sh --rizon_type Rizon4 --robot_sn Rizon4-123456
```

Generate URDF for Dual Arm setup:

```bash
./scripts/create_urdf.sh --dual --rizon_type_left Rizon4 --rizon_type_right Rizon4R --robot_sn_left Rizon4-123456 --robot_sn_right Rizon4R-654321
```

Generate URDF for AICO1-4-V1:

```bash
./scripts/create_urdf.sh --aico1 --external_axis_type AICO1-4-V1 --rizon_type Rizon4 --robot_sn Rizon4-123456
```

Generate URDF for AICO2-4-V1:

```bash
./scripts/create_urdf.sh --aico2 --external_axis_type AICO2-4-V1 --rizon_type Rizon4 --robot_sn_left Rizon4-123456 --robot_sn_right Rizon4R-654321
```

## Visualize in RViz

The robot models can be visualized in RViz using the provided script. This script runs inside a Docker container and requires a GUI environment.

```
usage: visualize_rizon.sh [--dual | --aico1 | --aico2] [OPTIONS]

Visualize Flexiv robots in RViz.

Single Arm Arguments:
  robot_sn:=ROBOT_SN            Serial number of the robot to connect to.
  rizon_type:=TYPE              Type of the Flexiv Rizon robot. (default: 'Rizon4')
  load_gripper:=BOOL            Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name:=NAME            Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor:=BOOL  Flag to load the mounted force torque sensor. (default: 'False')

Dual Arm Arguments (use with --dual):
  robot_sn_left:=SN                   Serial number of the left robot.
  robot_sn_right:=SN                  Serial number of the right robot.
  rizon_type_left:=TYPE               Type of the left robot. (default: 'Rizon4')
  rizon_type_right:=TYPE              Type of the right robot. (default: 'Rizon4')
  load_gripper_left:=BOOL             Load gripper for left robot. (default: 'False')
  load_gripper_right:=BOOL            Load gripper for right robot. (default: 'False')
  gripper_name_left:=NAME             Gripper name for left robot. (default: 'Flexiv-GN01')
  gripper_name_right:=NAME            Gripper name for right robot. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor_left:=BOOL   Load FT sensor for left robot. (default: 'False')
  load_mounted_ft_sensor_right:=BOOL  Load FT sensor for right robot. (default: 'False')

AICO1 Arguments (use with --aico1):
  external_axis_type:=TYPE      Type of the AICO platform (default: 'AICO1-4-V1').
  external_axis_prefix:=PREFIX  Prefix for the platform links and joints. (default: '')
  robot_sn:=ROBOT_SN            Serial number of the robot.
  rizon_type:=TYPE              Type of the Flexiv Rizon robot. (default: 'Rizon4')
  load_gripper:=BOOL            Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name:=NAME            Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor:=BOOL  Flag to load the mounted force torque sensor. (default: 'False')

AICO2 Arguments (use with --aico2):
  external_axis_type:=TYPE            Type of the AICO platform (default: 'AICO2-4-V1').
  external_axis_prefix:=PREFIX        Prefix for the platform links and joints. (default: '')
  rizon_type:=TYPE                    Type of the Flexiv Rizon robot. (default: 'Rizon4')
  robot_sn_left:=SN                   Serial number of the left robot.
  robot_sn_right:=SN                  Serial number of the right robot.
  load_gripper_left:=BOOL             Load gripper for left robot. (default: 'False')
  load_gripper_right:=BOOL            Load gripper for right robot. (default: 'False')
  gripper_name_left:=NAME             Gripper name for left robot. (default: 'Flexiv-GN01')
  gripper_name_right:=NAME            Gripper name for right robot. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor_left:=BOOL   Load FT sensor for left robot. (default: 'False')
  load_mounted_ft_sensor_right:=BOOL  Load FT sensor for right robot. (default: 'False')

Common Arguments:
  gui:=BOOL                Flag to enable joint_state_publisher_gui. (default: 'False')
```

Visualize single robot:

```bash
./scripts/visualize_rizon.sh rizon_type:=Rizon4 robot_sn:=Rizon4-123456 gui:=True
```

Visualize dual robots:

```bash
./scripts/visualize_rizon.sh --dual robot_sn_left:=Rizon4-123456 robot_sn_right:=Rizon4R-654321 gui:=True
```

Visualize AICO1-4-V1:

```bash
./scripts/visualize_rizon.sh --aico1 external_axis_type:=AICO1-4-V1 rizon_type:=Rizon4 robot_sn:=Rizon4-123456 gui:=True
```

Visualize AICO2-4-V1:

```bash
./scripts/visualize_rizon.sh --aico2 external_axis_type:=AICO2-4-V1 rizon_type:=Rizon4 robot_sn_left:=Rizon4-123456 robot_sn_right:=Rizon4R-654321 gui:=True
```

The translation of the two robots in the world frame can be configured in the `config/dual_arm_translations.yaml` file.

> [!NOTE]
> The launch files can also be run directly using `ros2 launch` if the package is built and sourced in your ROS2 workspace.
