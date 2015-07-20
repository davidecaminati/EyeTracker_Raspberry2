#!/bin/sh
echo "UDOO installation started"
apt-get update  # To get the latest package lists
apt-get upgrade
apt-get install build-essential cmake pkg-config --assume-yes
apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev --assume-yes
apt-get install libgtk2 --assume-yes
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev --assume-yes
apt-get install libatlas-base-dev gfortran --assume-yes
apt-get install git --assume-yes
wget https://www.dropbox.com/s/8p1tkfaxpdoibsm/opencv-2.4.10.zip
unzip opencv-2.4.10.zip
cd opencv-2.4.10/build
make install
ldconfig
cd ~
git clone https://github.com/davidecaminati/EyeTracker_Raspberry2
cd EyeTracker_Raspberry2
echo "launch a test"
export DISPLAY=:0.0
python external_eyetraking_webcam.py -o True -e 0 -v output640.avi
echo "installation ended"
#etc.