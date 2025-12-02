FROM osrf/ros:jazzy-desktop
ARG DEBIAN_FRONTEND=noninteractive
ARG USER_UID=1000
ARG USER_GID=1000
ARG USERNAME=user

WORKDIR /workspaces

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p -m 0700 /run/user/"${USER_UID}" \
    && chown $USERNAME:$USERNAME /run/user/"${USER_UID}" \
    && chown $USERNAME:$USERNAME /workspaces

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-rviz2 \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

USER $USERNAME
