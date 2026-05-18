#!/bin/bash

host_package_path=$(pwd)
container_package_path=/workspaces/src/flexiv_description

echo "Running URDF generation in Docker with bind mount:"
echo "  container package path: ${container_package_path}"
echo "  host package path: ${host_package_path}"

docker build -t urdf_creation \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    ./.docker

docker run -u $(id -u) \
    -e FLEXIV_DESCRIPTION_HOST_PATH="${host_package_path}" \
    -v "${host_package_path}:${container_package_path}" \
    -w "${container_package_path}" \
    urdf_creation \
    .docker/create_urdf.entrypoint.sh "$@" --output_path "${host_package_path}"
