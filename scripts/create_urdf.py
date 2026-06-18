#!/usr/bin/env python3
import argparse
import os
import xacro


def convert_xacro_to_urdf(xacro_file, mappings):
    """Convert xacro file into a URDF file."""
    doc = xacro.process_file(xacro_file, mappings=mappings)
    urdf_file = doc.toprettyxml(indent="  ")
    return urdf_file


def convert_package_name_to_absolute_path(package_name, package_path, urdf_file):
    """Replace a ROS package names with the absolute paths."""
    urdf_file = urdf_file.replace("package://{}".format(package_name), package_path)
    return urdf_file


def build_urdf_output_paths(package_path, file_name, host_package_path=None):
    """Build the container and host-visible URDF output paths."""
    container_output_path = os.path.join(package_path, "urdf", f"{file_name}.urdf")
    host_output_path = None
    if host_package_path:
        host_output_path = os.path.join(host_package_path, "urdf", f"{file_name}.urdf")
    return container_output_path, host_output_path


def print_output_location(message, container_output_path, host_output_path=None):
    """Print where the generated URDF can be found."""
    if host_output_path and os.path.normpath(host_output_path) != os.path.normpath(
        container_output_path
    ):
        print(f"{message} (container): {container_output_path}")
        print(f"{message} (host): {host_output_path}")
        return

    print(f"{message}: {container_output_path}")


def save_urdf_to_file(package_path, urdf_file, file_name, host_package_path=None):
    """Save URDF into a file."""
    # Save to 'urdf' folder in the package
    folder_path = os.path.join(package_path, "urdf")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    container_output_path, host_output_path = build_urdf_output_paths(
        package_path, file_name, host_package_path
    )
    with open(container_output_path, "w") as f:
        f.write(urdf_file)
    print_output_location("Created URDF file", container_output_path, host_output_path)


def urdf_generation(
    package_path,
    xacro_file,
    file_name,
    mappings,
    description,
    output_path=None,
    host_package_path=None,
):
    """Generate URDF file and save it."""
    full_xacro_path = os.path.join(package_path, xacro_file)
    try:
        print(
            f"Generating URDF '{file_name}.urdf' from '{xacro_file}' for {description}."
        )

        urdf_file = convert_xacro_to_urdf(full_xacro_path, mappings)

        target_path = output_path if output_path else package_path

        urdf_file = convert_package_name_to_absolute_path(
            "flexiv_description", target_path, urdf_file
        )
        save_urdf_to_file(package_path, urdf_file, file_name, host_package_path)
    except Exception as e:
        print(f"Error generating URDF for {file_name}: {e}")


if __name__ == "__main__":
    package_name = "flexiv_description"
    host_package_path = os.environ.get("FLEXIV_DESCRIPTION_HOST_PATH")

    # Ensure we are in the package root
    cwd = os.getcwd()
    if (
        os.path.basename(cwd) == "scripts"
        and os.path.basename(os.path.dirname(cwd)) == package_name
    ):
        os.chdir("..")
        cwd = os.getcwd()

    if os.path.basename(cwd) != package_name:
        # Try to find the package root if we are in the workspace
        if os.path.exists(os.path.join(cwd, "src", package_name)):
            os.chdir(os.path.join(cwd, "src", package_name))
            cwd = os.getcwd()
            print(f"Changed directory to {cwd}")
        elif os.path.basename(cwd) != package_name:
            print(
                f"Warning: You are running this script from {cwd}. It is recommended to run it from the {package_name} root folder."
            )

    # Single-arm (Enlight-L) and dual-arm (Enlight-LL + MICO family) robot types.
    ROBOT_TYPES = ["Enlight-L", "Enlight-LL", "MICO-Core", "MICO-Plus", "MICO-Ultra"]

    parser = argparse.ArgumentParser(
        description="Create URDF files from xacro for Flexiv robots."
    )
    parser.add_argument(
        "--robot_type",
        type=str,
        default="Enlight-L",
        help=f"Robot type. Options: {ROBOT_TYPES}.",
    )
    parser.add_argument("--arm_prefix", type=str, default="", help="Arm prefix.")
    parser.add_argument("--robot_sn", type=str, default="", help="Robot serial number.")
    parser.add_argument("--load_gripper", action="store_true", help="Load gripper.")
    parser.add_argument(
        "--gripper_name", type=str, default="Flexiv-GN01", help="Gripper name."
    )
    parser.add_argument(
        "--load_mounted_ft_sensor", action="store_true", help="Load mounted FT sensor."
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="",
        help="Absolute path to replace package://flexiv_description with.",
    )

    args = parser.parse_args()

    robot_type = args.robot_type

    if robot_type not in ROBOT_TYPES:
        print(f"Invalid robot_type: {robot_type}. Available: {ROBOT_TYPES}")
        exit(1)

    xacro_file = "urdf/flexiv.urdf.xacro"

    mappings = {
        "robot_type": robot_type,
        "arm_prefix": args.arm_prefix,
        "robot_sn": args.robot_sn,
        "load_gripper": str(args.load_gripper).lower(),
        "gripper_name": args.gripper_name,
        "load_mounted_ft_sensor": str(args.load_mounted_ft_sensor).lower(),
    }

    if args.robot_sn:
        file_name = args.robot_sn
    else:
        file_name = robot_type

    if args.arm_prefix:
        file_name = f"{args.arm_prefix}_{file_name}"
    if args.load_gripper:
        file_name += f"_{args.gripper_name}"

    urdf_generation(
        os.getcwd(),
        xacro_file,
        file_name,
        mappings,
        f"robot type '{robot_type}'",
        args.output_path,
        host_package_path,
    )
