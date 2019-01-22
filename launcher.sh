cd /
cd /home/pi/raspberry-pi-face-detection-master #the filepath to where the detector.py file lies
sudo modprobe bcm2835-v4l2
DISPLAY=:0 sudo python detector.py
cd /
