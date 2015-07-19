# Steps for use eye tracker with UDOO (tested in Quad Core version)

### Select OS
from http://www.udoo.org/downloads/
select UDOObuntu_quad_v1.1.img (or the dualcore image)
fit the image into a microSD card (at least 8 Gb class 10)
following the guide in the download page.

### Configure OS
when the system has booted, change use the tools "Udoo configuration" on the desktop
to change keyboard layout, timezone, password, expand the filesystem

### Start the installation script 
wget -O https://github.com/davidecaminati/EyeTracker_Raspberry2/blob/master/install_eyetracking.sh
sudo sh ./install_eyetracking.sh