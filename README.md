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

```bash
usage: create_urdf.sh [-h] --rizon_type RIZON_TYPE [--arm_prefix ARM_PREFIX] [--robot_sn ROBOT_SN] [--load_gripper] [--gripper_name GRIPPER_NAME][--load_mounted_ft_sensor]

Create URDF files from xacro for Flexiv robots.

required arguments:
  --rizon_type RIZON_TYPE       Rizon robot type. Options: ['Rizon4', 'Rizon4s', 'Rizon4M', 'Rizon4R', 'Rizon10', 'Rizon10s'].

optional arguments:
  --arm_prefix ARM_PREFIX       Arm prefix. (default: '')
  --robot_sn ROBOT_SN           Robot serial number. (default: '')
  --load_gripper                Load gripper. (default: False)
  --gripper_name GRIPPER_NAME   Gripper name. (default: 'Flexiv-GN01')
  --load_mounted_ft_sensor      Load mounted FT sensor. (default: False)
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

## Visualize in RViz

The robot models can be visualized in RViz using the provided script. This script runs inside a Docker container and requires a GUI environment.

```bash
usage: visualize_rizon.sh robot_sn:=ROBOT_SN [rizon_type:=Rizon4] [load_gripper:=false] [gripper_name:=Flexiv-GN01] [load_mounted_ft_sensor:=false] [gui:=false]

Visualize Flexiv robots in RViz.

required arguments:
  robot_sn:=ROBOT_SN       Serial number of the robot to connect to. Remove any space, for example: Rizon4s-123456.

optional arguments:
  rizon_type               Type of the Flexiv Rizon robot. Options: ['Rizon4', 'Rizon4M', 'Rizon4R', 'Rizon4s', 'Rizon10', 'Rizon10s']. (default: 'Rizon4')
  load_gripper             Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name             Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor   Flag to load the mounted force torque sensor. Only available for Rizon4, Rizon4R and Rizon10. (default: 'False')
  gui                      Flag to enable joint_state_publisher_gui. (default: 'False')
```

### Example

```bash
./scripts/visualize_rizon.sh rizon_type:=Rizon4 robot_sn:=Rizon4-123456 gui:=True
```
