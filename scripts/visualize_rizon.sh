#!/bin/bash
docker build -t urdf_creation \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    ./.docker

echo

LAUNCH_FILE="view_rizon.launch.py"
ARGS=""

for arg in "$@"
do
    if [ "$arg" == "--dual" ]; then
        LAUNCH_FILE="view_rizon_dual.launch.py"
    elif [ "$arg" == "--aico1" ]; then
        LAUNCH_FILE="view_aico1.launch.py"
    elif [ "$arg" == "--aico2" ]; then
        LAUNCH_FILE="view_aico2.launch.py"
    else
        ARGS="$ARGS $arg"
    fi
done

docker run -it -u $(id -u) \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=${DISPLAY} \
    -v $(pwd):/workspaces/src/flexiv_description \
    -w /workspaces/src/flexiv_description \
    -e LAUNCH_FILE=$LAUNCH_FILE \
    urdf_creation \
    .docker/visualize_rizon.entrypoint.sh $ARGS
