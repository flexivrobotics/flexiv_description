# flexiv_description

URDF description for Flexiv robots.

## URDF Creation

The URDF files for Flexiv robots can be generated from xacro files using the provided script. This script runs inside a Docker container to ensure a consistent environment.

### Supported robot types

The same `robot_type` values are used by both URDF creation and visualization.
[config/robot_types.yaml](config/robot_types.yaml) is the single source of truth
and is read by both `scripts/create_urdf.py` and `launch/view_flexiv.launch.py`.

**Single arm on a mount** — one `robot_sn`, pose from `config/single_robot_mounting.yaml`:

- `Enlight-L`
- `Rizon4`
- `Rizon4s`
- `Rizon4M`
- `Rizon4R`
- `Rizon10`
- `Rizon10s`
- `Rizon10R`

`Rizon4R` is mirrored `Rizon4` kinematics and is the default right arm of a pair.
`Rizon10R` is mirrored `Rizon10` kinematics and is the default right arm of an `AICO2-10-V1` pair.

**One robot with two arms** — one `robot_sn`, one `FlexivHardwareInterface`:

| `robot_type` | Arms | Torso |
| --- | --- | --- |
| `Enlight-LL` | Two Enlight-L on `world` | — |
| `MICO-Core` | Two Enlight-L | fixed |
| `MICO-Plus` | Two Enlight-L | 2-DoF (yaw + pitch) pan-tilt |
| `MICO-Ultra` | Two Enlight-L | 2-DoF (waist yaw + pitch) on a mobile base (empty base root, no mesh) |

Arm joints and links are prefixed `left_${robot_sn}_` and `right_${robot_sn}_`, the
MICO-Plus/Ultra torso uses `${robot_sn}_torso_` (`${robot_sn}_torso_joint1`/`joint2`),
and all MICO arms reuse the `config/Enlight-L` parameters.

**Single arm on an external axis** — one `robot_sn`; the axis joints join the arm's
own hardware interface. Select the arm with `arm_type` (`Rizon4`, `Rizon4s` or
`Rizon4R`; empty picks `Rizon4`):

| `robot_type` | Actuated axis joints |
| --- | --- |
| `AICO1-4-V1` | `joint2` (`joint1` is fixed) |
| `AICO1-4-V2` | `joint1`, `joint2`, `joint_head` |

**Two paired robots** — `robot_sn_left` **and** `robot_sn_right` are both required,
driven by one `FlexivDualHardwareInterface`. Select the arms with `arm_type_left`
and `arm_type_right`; empty picks the arm the model actually carries:

| `robot_type` | External axis | Default arms |
| --- | --- | --- |
| `Rizon-Dual` | none, both arms bolt to `world` using `config/dual_arm_mounting.yaml` | `Rizon4` + `Rizon4R` |
| `AICO2-4-V1` | 2-DoF | `Rizon4` + `Rizon4R` |
| `AICO2-4-V2` | 2-DoF | `Rizon4` + `Rizon4R` |
| `AICO2-10-V1` | 2-DoF | `Rizon10` + `Rizon10R` |

Arm prefixes are `left_${robot_sn_left}_` and `right_${robot_sn_right}_`. Since the
two arms are separate robots, each has its own GPIO block.

> [!NOTE]
> Digital IO is 16 control-box ports plus 2 per wrist connector, so Enlight-L and
> MICO expose 20 ports while Rizon exposes 18.

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
                      [--load_mounted_ft_sensor] [--output_path OUTPUT_PATH]
                      [--external_axis_prefix EXTERNAL_AXIS_PREFIX]
                      [--arm_type ARM_TYPE]
                      [--robot_sn_left ROBOT_SN_LEFT]
                      [--robot_sn_right ROBOT_SN_RIGHT]
                      [--arm_type_left ARM_TYPE_LEFT]
                      [--arm_type_right ARM_TYPE_RIGHT]
                      [--load_gripper_left] [--load_gripper_right]
                      [--gripper_name_left GRIPPER_NAME_LEFT]
                      [--gripper_name_right GRIPPER_NAME_RIGHT]
                      [--load_mounted_ft_sensor_left]
                      [--load_mounted_ft_sensor_right]

Create URDF files from xacro for Flexiv robots.

optional arguments:
  -h, --help            show this help message and exit
  --robot_type ROBOT_TYPE
                        Robot type. See config/robot_types.yaml.
                        (default: 'Enlight-L')
  --arm_prefix ARM_PREFIX
                        Arm prefix. (default: '')
  --robot_sn ROBOT_SN   Robot serial number. (default: '')
  --load_gripper        Load gripper. (default: False)
  --gripper_name GRIPPER_NAME
                        Gripper name. (default: 'Flexiv-GN01')
  --load_mounted_ft_sensor
                        Load mounted FT sensor. (default: False)
  --output_path OUTPUT_PATH
                        Absolute path to replace package://flexiv_description
                        with. (default: '')

External axis (AICO) arguments:
  --external_axis_prefix EXTERNAL_AXIS_PREFIX
                        External axis prefix. (default: '')
  --arm_type ARM_TYPE   Arm carried by an AICO1 external axis. Empty picks
                        the axis default. (default: '')

Paired-robot arguments (Rizon-Dual and AICO2):
  --robot_sn_left ROBOT_SN_LEFT
                        Left robot serial number. Required. (default: '')
  --robot_sn_right ROBOT_SN_RIGHT
                        Right robot serial number. Required. (default: '')
  --arm_type_left ARM_TYPE_LEFT
                        Left arm type. Empty picks the default. (default: '')
  --arm_type_right ARM_TYPE_RIGHT
                        Right arm type. Empty picks the default. (default: '')
  --load_gripper_left   Load left gripper. (default: False)
  --load_gripper_right  Load right gripper. (default: False)
  --gripper_name_left GRIPPER_NAME_LEFT
                        Left gripper name. (default: 'Flexiv-GN01')
  --gripper_name_right GRIPPER_NAME_RIGHT
                        Right gripper name. (default: 'Flexiv-GN01')
  --load_mounted_ft_sensor_left
                        Load left mounted FT sensor. (default: False)
  --load_mounted_ft_sensor_right
                        Load right mounted FT sensor. (default: False)
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

Generate URDF for a Rizon:

```bash
./scripts/create_urdf.sh --robot_type Rizon4   --robot_sn Rizon4-062001
./scripts/create_urdf.sh --robot_type Rizon10s --robot_sn Rizon10s-062002
```

Generate URDF for a single arm on an AICO1 external axis:

```bash
./scripts/create_urdf.sh --robot_type AICO1-4-V1 --robot_sn Rizon4-062001
./scripts/create_urdf.sh --robot_type AICO1-4-V2 --robot_sn Rizon4-062001 --arm_type Rizon4s
```

Generate URDF for paired robots. Both serial numbers are required, and the output
is named `<robot_sn_left>_<robot_sn_right>.urdf`:

```bash
./scripts/create_urdf.sh --robot_type Rizon-Dual \
  --robot_sn_left Rizon4-062001 --robot_sn_right Rizon4R-062002

./scripts/create_urdf.sh --robot_type AICO2-10-V1 \
  --robot_sn_left Rizon10-062003 --robot_sn_right Rizon10R-062004
```

## Visualize in RViz

The robot models can be visualized in RViz using the provided script. This script runs inside a Docker container and requires a GUI environment.

```
usage: visualize_flexiv.sh [OPTIONS]

Visualize Flexiv robots in RViz.

Arguments:
  robot_sn:=ROBOT_SN            Serial number of the robot. Leave empty for the
                                paired types. (default: '')
  robot_type:=TYPE              Type of the Flexiv robot. (default: 'Enlight-L')
  load_gripper:=BOOL            Flag to load the Flexiv Grav gripper. (default: 'False')
  gripper_name:=NAME            Full name of the gripper to be controlled. (default: 'Flexiv-GN01')
  load_mounted_ft_sensor:=BOOL  Flag to load the mounted force torque sensor. (default: 'False')
  robot_sn_left:=SN             Left robot serial number, paired types. (default: '')
  robot_sn_right:=SN            Right robot serial number, paired types. (default: '')
  arm_type:=TYPE                Arm on an AICO1 external axis. (default: '')
  arm_type_left:=TYPE           Left arm type, paired types. (default: '')
  arm_type_right:=TYPE          Right arm type, paired types. (default: '')
  external_axis_prefix:=PREFIX  Prefix for external axis links/joints. (default: '')
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

Visualize a Rizon or an AICO1:

```bash
./scripts/visualize_flexiv.sh robot_type:=Rizon4     robot_sn:=Rizon4-062001 gui:=True
./scripts/visualize_flexiv.sh robot_type:=AICO1-4-V2 robot_sn:=Rizon4-062001 gui:=True
```

Visualize paired robots:

```bash
./scripts/visualize_flexiv.sh robot_type:=Rizon-Dual \
  robot_sn_left:=Rizon4-062001 robot_sn_right:=Rizon4R-062002 gui:=True

./scripts/visualize_flexiv.sh robot_type:=AICO2-10-V1 \
  robot_sn_left:=Rizon10-062003 robot_sn_right:=Rizon10R-062004 gui:=True
```

`rviz/view_rizon_dual.rviz` is also available as an alternative RViz layout for
paired robots; pass it with `rvizconfig:=`.

> [!NOTE]
> The launch files can also be run directly using `ros2 launch` if the package is built and sourced in your ROS 2 workspace.
