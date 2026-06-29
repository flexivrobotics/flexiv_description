# flexiv_description

URDF description for Flexiv robots.

> [!IMPORTANT]
> This branch works with Flexiv software package **v4** and Flexiv ROS 2 Jazzy **v2** versions.
>
> Flexiv software v4 series is only for Enlight/MICO product family use. For Flexiv Rizon and AICO products, please refer to the `jazzy-v1` branch.

## URDF Creation

The URDF files for Flexiv robots can be generated from xacro files using the provided script. This script runs inside a Docker container to ensure a consistent environment.

### Supported robot types

The same `robot_type` values are used by both URDF creation and visualization:

| `robot_type` | Arms | Torso | Notes |
| --- | --- | --- | --- |
| `Enlight-L` | single | — | Single 7-DoF arm |
| `Enlight-LL` | dual | — | Two Enlight-L arms mounted on `world` |
| `MICO-Core` | dual | fixed | Two Enlight-L arms on a fixed torso |
| `MICO-Plus` | dual | 2-DoF (yaw + pitch) | Pan-tilt torso |
| `MICO-Ultra` | dual | 2-DoF (waist yaw + pitch) | Torso on a mobile base (modeled as an empty base root, no mesh) |

Dual-arm robots (Enlight-LL, MICO-\*) share one serial number; their arm joints/links are prefixed `left_${robot_sn}_` and `right_${robot_sn}_`, and the MICO-Plus/Ultra torso uses the prefix `${robot_sn}_torso_` (`${robot_sn}_torso_joint1`/`joint2`). All MICO arms reuse the `config/Enlight-L` parameters.

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
                        Robot type. Options: ['Enlight-L', 'Enlight-LL',
                        'MICO-Core', 'MICO-Plus', 'MICO-Ultra']. (default: 'Enlight-L')
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

Generate URDF for Enlight-L:

```bash
./scripts/create_urdf.sh --robot_type Enlight-L
```

Generate URDF for Enlight-L with a specific serial number:

```bash
./scripts/create_urdf.sh --robot_type Enlight-L --robot_sn Enlight-L-123456
```

Generate URDF for Enlight-L with gripper:

```bash
./scripts/create_urdf.sh --robot_type Enlight-L --robot_sn Enlight-L-123456 --load_gripper
```

Generate URDF for a dual-arm robot (Enlight-LL or any MICO variant):

```bash
./scripts/create_urdf.sh --robot_type Enlight-LL --robot_sn Enlight-LL-123456
./scripts/create_urdf.sh --robot_type MICO-Core  --robot_sn MICO-Core-123456
./scripts/create_urdf.sh --robot_type MICO-Plus  --robot_sn MICO-Plus-123456
./scripts/create_urdf.sh --robot_type MICO-Ultra --robot_sn MICO-Ultra-123456
```

## Visualize in RViz

The robot models can be visualized in RViz using the provided script. This script runs inside a Docker container and requires a GUI environment.

```
usage: visualize_flexiv.sh [OPTIONS]

Visualize Flexiv robots in RViz.

Arguments:
  robot_sn:=ROBOT_SN            Serial number of the robot to connect to.
  robot_type:=TYPE              Type of the Flexiv robot (single- or dual-arm). (default: 'Enlight-L')
  load_gripper:=BOOL            Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name:=NAME            Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor:=BOOL  Flag to load the mounted force torque sensor. (default: 'False')
  gui:=BOOL                     Flag to enable joint_state_publisher_gui. (default: 'False')
```

Visualize Enlight-L:

```bash
./scripts/visualize_flexiv.sh robot_type:=Enlight-L robot_sn:=Enlight-L-123456 gui:=True
```

Visualize a dual-arm robot (Enlight-LL or any MICO variant):

```bash
./scripts/visualize_flexiv.sh robot_type:=Enlight-LL robot_sn:=Enlight-LL-123456 gui:=True
./scripts/visualize_flexiv.sh robot_type:=MICO-Core  robot_sn:=MICO-Core-123456  gui:=True
./scripts/visualize_flexiv.sh robot_type:=MICO-Plus  robot_sn:=MICO-Plus-123456  gui:=True
./scripts/visualize_flexiv.sh robot_type:=MICO-Ultra robot_sn:=MICO-Ultra-123456 gui:=True
```

> [!NOTE]
> The launch files can also be run directly using `ros2 launch` if the package is built and sourced in your ROS 2 workspace.
