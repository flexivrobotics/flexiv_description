#!/bin/bash
docker build -t urdf_creation \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    ./.docker

docker run -u $(id -u) \
    -v $(pwd):/workspaces/src/flexiv_description \
    -w /workspaces/src/flexiv_description \
    urdf_creation \
    .docker/create_urdf.entrypoint.sh $*
