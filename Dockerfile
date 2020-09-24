FROM ubuntu:18.04

RUN apt update
RUN apt install --yes --quiet git curl gnupg

RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN echo "deb [arch=amd64] http://robotpkg.openrobots.org/wip/packages/debian/pub bionic robotpkg" > /etc/apt/sources.list.d/robotpkg.list
RUN echo "deb [arch=amd64] http://robotpkg.openrobots.org/packages/debian/pub bionic robotpkg" >> /etc/apt/sources.list.d/robotpkg.list
RUN curl http://robotpkg.openrobots.org/packages/debian/robotpkg.key | apt-key add -
RUN apt update
RUN apt upgrade --yes

#RUN apt install --yes --quiet robotpkg-romeo-description
RUN DEBIAN_FRONTEND="noninteractive" apt install --yes --quiet robotpkg-py36-hpp-manipulation-corba robotpkg-py36-qt5-hpp-gepetto-viewer
RUN apt install --yes --quiet robotpkg-py36-qt5-hpp-gui robotpkg-py36-qt5-hpp-plot

RUN apt install --yes --quiet ipython3 python3-numpy

ENV QT_X11_NO_MITSHM=1

RUN echo "export ROBOTPKG_BASE=/opt/openrobots" >> ~/.bashrc
RUN echo "export PATH=\$ROBOTPKG_BASE/bin:\$PATH" >> ~/.bashrc
RUN echo "export PYTHONPATH=\$ROBOTPKG_BASE/lib/python3.6/site-packages:\$PYTHONPATH" >> ~/.bashrc
RUN echo "export LD_LIBRARY_PATH=\$ROBOTPKG_BASE/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc
RUN echo "export CMAKE_PREFIX_PATH=\$ROBOTPKG_BASE:\$CMAKE_PREFIX_PATH" >> ~/.bashrc
RUN echo "export ROS_PACKAGE_PATH=\$ROBOTPKG_BASE/share:/opt/ros/melodic/share" >> ~/.bashrc

RUN mkdir /workspace && cd /workspace && git clone --recursive --branch upssitech-2020 https://github.com/jmirabel/hpp-practicals
