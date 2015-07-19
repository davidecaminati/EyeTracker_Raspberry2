#!/bin/sh
echo "UDOO installation started"
apt-get update  # To get the latest package lists
apt-get upgrade
apt-get install build-essential cmake pkg-config --assume-yes
apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev --assume-yes
apt-get install libgtk2 --assume-yes
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev --assume-yes
apt-get install libatlas-base-dev gfortran --assume-yes
echo "installation ended"
#etc.