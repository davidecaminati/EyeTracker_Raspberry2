#EyeTracker_Raspberry2
EyeTracker for Raspberry2

We want create a simple device for detect simple eye movement (RIGHT,LEFT,CENTER) and use this detection
to create a gesture for control device like IR Remote control, windows/doors, television, every electrical device.

We have choose Raspberry 2 and Python (for the moment 2.7) to make it simple to reproduce and simple to manage.
We also use a Logitech camera and an Arduino for our purpose.

To use this software you have 2 ways:
First way

Download the image of the entire OS and fit it into a MicroSD card (we suggest 16 Gb Evo Samsung ~10,00 €)
Follow the instruction on youtube [TODO provide link]

Start your Raspberry, open a console and run "ifconfig" to check the IP address.
ie. 192.168.0.6   

Now connect a USB camera and check if the system recognize it, use this command
ls /dev | grep video0
if  "video0" is the output, the camera are correctly recognized

now if you want use another computer to connect to the Raspberry, you need a terminal client (ie. on Windows use PUTTY)
remember: if you launch a script with graphical output (like this OpenCV) you need to redirect the output of the terminal using this command
export DISPLAY=:0.0
this permit to render the graphical in the raspberry attached monitor.



#####We need to fix an issue in the Virtual Environment
#####update your ~/.profile  file to include the following lines in the end of the file:
nano ~/.profile  

export WORKON_HOME=$HOME/.virtualenvs  
source /usr/local/bin/virtualenvwrapper.sh  

#####Now reload the profile
source ~/.profile

#####And activate Virtual Environment
workon cv


#####Now clone the repository (be sure you are in the user folder /home/pi)
git clone https://github.com/davidecaminati/EyeTracker_Raspberry2

#####move into directory
cd EyeTracker_Raspberry2

#####start the program
python external_eyetraking_webcam.py -o True -e 0






Second way

Start from scratch downloading the Raspbian image from this link (https://www.raspberrypi.org/downloads/) 
then follow the instruction to fit the Image into your MicroSD card, after this, follow the guide of installation for
OpenCV (https://github.com/davidecaminati/EyeTracker_Raspberry2/blob/master/external_eyetraking_webcam.py)





