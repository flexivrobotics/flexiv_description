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

    RIZON_TYPES = ["Rizon4", "Rizon4s", "Rizon4M", "Rizon4R", "Rizon10", "Rizon10s"]

    parser = argparse.ArgumentParser(
        description="Create URDF files from xacro for Flexiv robots."
    )
    parser.add_argument(
        "--dual",
        action="store_true",
        help="Generate URDF for dual arm setup.",
    )
    parser.add_argument(
        "--aico1",
        action="store_true",
        help="Generate URDF for AICO1 setup.",
    )
    parser.add_argument(
        "--aico2",
        action="store_true",
        help="Generate URDF for AICO2 setup.",
    )
    parser.add_argument(
        "--external_axis_type",
        type=str,
        default="",
        help="External axis type for AICO robots.",
        choices=[
            "AICO1-4-V1",
            "AICO1-4-V2",
            "AICO2-4-V1",
            "AICO2-4-V2",
            "AICO2-10-V1",
        ],
    )
    parser.add_argument(
        "--external_axis_prefix",
        type=str,
        default="",
        help="External axis prefix.",
    )
    parser.add_argument(
        "--rizon_type",
        type=str,
        help=f"Rizon robot type (Single arm). Options: {RIZON_TYPES}.",
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

    # Dual arm arguments
    parser.add_argument(
        "--rizon_type_left",
        type=str,
        default="Rizon4",
        help=f"Left Rizon robot type. Options: {RIZON_TYPES}.",
    )
    parser.add_argument(
        "--rizon_type_right",
        type=str,
        default="Rizon4R",
        help=f"Right Rizon robot type. Options: {RIZON_TYPES}.",
    )
    parser.add_argument(
        "--robot_sn_left", type=str, default="", help="Left robot serial number."
    )
    parser.add_argument(
        "--robot_sn_right", type=str, default="", help="Right robot serial number."
    )
    parser.add_argument(
        "--load_gripper_left", action="store_true", help="Load gripper for left robot."
    )
    parser.add_argument(
        "--load_gripper_right",
        action="store_true",
        help="Load gripper for right robot.",
    )
    parser.add_argument(
        "--gripper_name_left",
        type=str,
        default="Flexiv-GN01",
        help="Gripper name for left robot.",
    )
    parser.add_argument(
        "--gripper_name_right",
        type=str,
        default="Flexiv-GN01",
        help="Gripper name for right robot.",
    )
    parser.add_argument(
        "--load_mounted_ft_sensor_left",
        action="store_true",
        help="Load mounted FT sensor for left robot.",
    )
    parser.add_argument(
        "--load_mounted_ft_sensor_right",
        action="store_true",
        help="Load mounted FT sensor for right robot.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="",
        help="Absolute path to replace package://flexiv_description with.",
    )

    args = parser.parse_args()

    if args.aico1:
        if not args.rizon_type:
            print("Error: --rizon_type is required for AICO1 generation.")
            exit(1)
        if args.rizon_type not in ["Rizon4", "Rizon4s"]:
            print(
                f"Invalid rizon_type: {args.rizon_type}. AICO1 only supports Rizon4 and Rizon4s."
            )
            exit(1)

        xacro_file = "urdf/aico1.urdf.xacro"
        mappings = {
            "external_axis_type": args.external_axis_type.replace("-", "_").lower(),
            "external_axis_prefix": args.external_axis_prefix,
            "robot_sn": args.robot_sn,
            "rizon_type": args.rizon_type,
            "load_gripper": str(args.load_gripper).lower(),
            "gripper_name": args.gripper_name,
            "load_mounted_ft_sensor": str(args.load_mounted_ft_sensor).lower(),
        }

        file_name = "aico1"
        if args.robot_sn:
            file_name = f"aico1_{args.robot_sn}"

        urdf_generation(
            os.getcwd(),
            xacro_file,
            file_name,
            mappings,
            f"{args.external_axis_type} with robot type '{args.rizon_type}'",
            args.output_path,
            host_package_path,
        )

    elif args.aico2:
        if not args.rizon_type:
            print("Error: --rizon_type is required for AICO2 generation.")
            exit(1)
        if args.rizon_type not in ["Rizon4", "Rizon10"]:
            print(
                f"Invalid rizon_type: {args.rizon_type}. AICO2 only supports Rizon4 and Rizon10 pairs."
            )
            exit(1)

        if (
            args.rizon_type == "Rizon4"
            and args.external_axis_type != "AICO2-4-V1"
            and args.external_axis_type != "AICO2-4-V2"
        ):
            print(
                f"Invalid external_axis_type: {args.external_axis_type}. AICO2 with Rizon4 only supports AICO2-4-V1 and AICO2-4-V2."
            )
            exit(1)
        if args.rizon_type == "Rizon10" and args.external_axis_type != "AICO2-10-V1":
            print(
                f"Invalid external_axis_type: {args.external_axis_type}. AICO2 with Rizon10 only supports AICO2-10-V1."
            )
            exit(1)

        xacro_file = "urdf/aico2.urdf.xacro"
        mappings = {
            "external_axis_type": args.external_axis_type.replace("-", "_").lower(),
            "external_axis_prefix": args.external_axis_prefix,
            "rizon_type": args.rizon_type,
            "robot_sn_left": args.robot_sn_left,
            "robot_sn_right": args.robot_sn_right,
            "load_gripper_left": str(args.load_gripper_left).lower(),
            "load_gripper_right": str(args.load_gripper_right).lower(),
            "gripper_name_left": args.gripper_name_left,
            "gripper_name_right": args.gripper_name_right,
            "load_mounted_ft_sensor_left": str(
                args.load_mounted_ft_sensor_left
            ).lower(),
            "load_mounted_ft_sensor_right": str(
                args.load_mounted_ft_sensor_right
            ).lower(),
        }

        file_name = "aico2"
        if args.robot_sn_left and args.robot_sn_right:
            file_name = f"aico2_{args.robot_sn_left}_{args.robot_sn_right}"

        urdf_generation(
            os.getcwd(),
            xacro_file,
            file_name,
            mappings,
            f"{args.external_axis_type} with robot type '{args.rizon_type}'",
            args.output_path,
            host_package_path,
        )

    elif args.dual:
        if args.rizon_type_left not in RIZON_TYPES:
            print(
                f"Invalid rizon_type_left: {args.rizon_type_left}. Available: {RIZON_TYPES}"
            )
            exit(1)
        if args.rizon_type_right not in RIZON_TYPES:
            print(
                f"Invalid rizon_type_right: {args.rizon_type_right}. Available: {RIZON_TYPES}"
            )
            exit(1)

        xacro_file = "urdf/rizon_dual.urdf.xacro"
        mappings = {
            "rizon_type_left": args.rizon_type_left,
            "rizon_type_right": args.rizon_type_right,
            "robot_sn_left": args.robot_sn_left,
            "robot_sn_right": args.robot_sn_right,
            "load_gripper_left": str(args.load_gripper_left).lower(),
            "load_gripper_right": str(args.load_gripper_right).lower(),
            "gripper_name_left": args.gripper_name_left,
            "gripper_name_right": args.gripper_name_right,
            "load_mounted_ft_sensor_left": str(
                args.load_mounted_ft_sensor_left
            ).lower(),
            "load_mounted_ft_sensor_right": str(
                args.load_mounted_ft_sensor_right
            ).lower(),
        }

        file_name = "rizon_dual"
        if args.robot_sn_left and args.robot_sn_right:
            file_name = f"dual_{args.robot_sn_left}_{args.robot_sn_right}"

        urdf_generation(
            os.getcwd(),
            xacro_file,
            file_name,
            mappings,
            (
                "dual-arm setup with "
                f"'{args.rizon_type_left}' and '{args.rizon_type_right}'"
            ),
            args.output_path,
            host_package_path,
        )

    else:
        if not args.rizon_type:
            print("Error: --rizon_type is required for single arm generation.")
            exit(1)

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

        urdf_generation(
            os.getcwd(),
            xacro_file,
            file_name,
            mappings,
            f"robot type '{rizon_type}'",
            args.output_path,
            host_package_path,
        )
