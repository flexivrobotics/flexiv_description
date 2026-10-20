FROM osrf/ros:lyrical-desktop
ARG DEBIAN_FRONTEND=noninteractive
ARG USER_UID=1000
ARG USER_GID=1000
ARG USERNAME=user

WORKDIR /workspaces

RUN if getent passwd $USER_UID; then userdel -r $(getent passwd $USER_UID | cut -d: -f1) || true; fi \
    && if getent group $USER_GID; then groupdel $(getent group $USER_GID | cut -d: -f1) || true; fi \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p -m 0700 /run/user/"${USER_UID}" \
    && chown $USERNAME:$USERNAME /run/user/"${USER_UID}" \
    && chown $USERNAME:$USERNAME /workspaces

RUN sed -i 's/^Types: deb deb-src$/Types: deb/' /etc/apt/sources.list.d/ros2.sources

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-lyrical-xacro \
    ros-lyrical-joint-state-publisher \
    ros-lyrical-joint-state-publisher-gui \
    ros-lyrical-robot-state-publisher \
    ros-lyrical-rviz2 \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

USER $USERNAME
