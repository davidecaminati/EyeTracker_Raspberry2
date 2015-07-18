#EyeTracker_Raspberry2
EyeTracker for Raspberry2

Install OpenCV on raspberry 2
=======
follow this guide to install OpenCV (thanks to Adrian Rosebrock)
-----------
http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/
-----------
Step by step guide
-----------

sudo apt-get update
sudo apt-get upgrade
sudo rpi-update

sudo apt-get install build-essential cmake pkg-config

sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev

sudo apt-get install libgtk2.0-dev

sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

sudo apt-get install libatlas-base-dev gfortran

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install virtualenv virtualenvwrapper

###Then, update your ~/.profile  file to include the following lines:
nano ~/.profile  
export WORKON_HOME=$HOME/.virtualenvs  
source /usr/local/bin/virtualenvwrapper.sh  

source ~/.profile

mkvirtualenv cv

sudo apt-get install python2.7-dev

pip install numpy

wget -O opencv-2.4.10.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download  
unzip opencv-2.4.10.zip  
cd opencv-2.4.10

mkdir build  
cd build  
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON ..

make
or if you want to use multicore capability during compiling thy with this other
make -j3


sudo make install  
sudo ldconfig

cd ~/.virtualenvs/cv/lib/python2.7/site-packages/  
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so  
ln -s /usr/local/lib/python2.7/site-packages/cv.py cv.py  


### Test it!
workon cv  
python  
import cv2  
cv2.__version__  
'2.4.10'

### install git
sudo apt-get install git

### clone the repository inside home directory
cd ~
git clone https://github.com/davidecaminati/Handcart-lift-rotary

### link some file 
ln Handcart-lift-rotary/Python/facedetect_mio.py opencv-2.4.10/samples/python2/
ln Handcart-lift-rotary/Python/digits.py opencv-2.4.10/samples/python2/
ln Handcart-lift-rotary/Python/digits_video_v2.py opencv-2.4.10/samples/python2/
ln Handcart-lift-rotary/Python/facedetect_mio_detect_cyrcle.py opencv-2.4.10/samples/python2/
ln Handcart-lift-rotary/Python/How\ to\ use.txt opencv-2.4.10/samples/python2/    
ln Handcart-lift-rotary/Python/my_collage.py opencv-2.4.10/samples/python2/

### make it executable
~/opencv-2.4.10/samples/python2
chmod +x digits_video_v2.py
chmod +x facedetect_mio_detect_cyrcle.py
chmod +x facedetect_mio.py
chmod +x my_collage.py

### install firmata library for comunication with Arduino
sudo apt-get install arduino
pip install pyfirmata

### For audio management
sudo apt-get install python-pygame
