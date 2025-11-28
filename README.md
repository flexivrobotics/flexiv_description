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

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `--rizon_type` | **Required**. Rizon robot type. Options: `Rizon4`, `Rizon4s`, `Rizon4M`, `Rizon4R`, `Rizon10`, `Rizon10s`. | - |
| `--arm_prefix` | Prefix for the arm links and joints. | "" |
| `--robot_sn` | Robot serial number. If provided, it will be used in the output filename. | "" |
| `--load_gripper` | Flag to load the gripper. | False |
| `--gripper_name` | Name of the gripper to load. | `Flexiv-GN01` |
| `--load_mounted_ft_sensor` | Flag to load the mounted FT sensor. | False |

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
./scripts/visualize_rizon.sh rizon_type:=Rizon4 robot_sn:=Rizon4-123456
```
