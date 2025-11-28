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


def save_urdf_to_file(package_path, urdf_file, file_name):
    """Save URDF into a file."""
    # Save to 'urdf' folder in the package
    folder_path = os.path.join(package_path, "urdf")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    output_path = os.path.join(folder_path, f"{file_name}.urdf")
    with open(output_path, "w") as f:
        f.write(urdf_file)
    print(f"Created {output_path}")


def urdf_generation(package_path, xacro_file, file_name, mappings):
    """Generate URDF file and save it."""
    full_xacro_path = os.path.join(package_path, xacro_file)
    try:
        urdf_file = convert_xacro_to_urdf(full_xacro_path, mappings)
        urdf_file = convert_package_name_to_absolute_path(
            "flexiv_description", package_path, urdf_file
        )
        save_urdf_to_file(package_path, urdf_file, file_name)
    except Exception as e:
        print(f"Error generating URDF for {file_name}: {e}")


if __name__ == "__main__":
    package_name = "flexiv_description"

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

    RIZON_TYPES = ["Rizon4", "Rizon4s", "Rizon4M", "Rizon4R", "Rizon10", "Rizon10s"]

    parser = argparse.ArgumentParser(
        description="Create URDF files from xacro for Flexiv robots."
    )
    parser.add_argument(
        "--rizon_type",
        type=str,
        required=True,
        help=f"Rizon robot type. Options: {RIZON_TYPES}.",
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

    args = parser.parse_args()

    if args.rizon_type not in RIZON_TYPES:
        print(f"Invalid rizon_type: {args.rizon_type}. Available: {RIZON_TYPES}")
        exit(1)

    xacro_file = "urdf/rizon.urdf.xacro"

    rizon_type = args.rizon_type
    mappings = {
        "rizon_type": rizon_type,
        "arm_prefix": args.arm_prefix,
        "robot_sn": args.robot_sn,
        "load_gripper": str(args.load_gripper).lower(),
        "gripper_name": args.gripper_name,
        "load_mounted_ft_sensor": str(args.load_mounted_ft_sensor).lower(),
    }

    if args.robot_sn:
        file_name = args.robot_sn
    else:
        file_name = rizon_type

    if args.arm_prefix:
        file_name = f"{args.arm_prefix}_{file_name}"
    if args.load_gripper:
        file_name += f"_{args.gripper_name}"

    print(f"Generating URDF for {rizon_type}...")
    urdf_generation(os.getcwd(), xacro_file, file_name, mappings)
