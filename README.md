# Raspberry Pi Face Detection Camera
This project shows you how to setup a functioning facial detection camera using a Raspberry Pi and a PiCam V2 and then automatically upload the data to an AWS S3 bucket.


## First configuring the Raspberry Pi
###### 1. Load Raspbian onto the Pi device.
Download Raspbian off the [official site](https://www.raspberrypi.org/downloads/) and use [Etcher](https://www.balena.io/etcher/) to flash Raspbian to the MicroSD card.

###### 2. Uninstall all unnecessary programs.
Run the in the Terminal to remove all unnecessary programs:
```
sudo apt-get remove --purge wolfram-engine* scratch* libreoffice*
```
Once done:
```
sudo apt-get autoremove --purge
```
to remove all dependencies that have been uninstalled. After that, update all excisting programs:
```
sudo apt-get update && sudo apt-get upgrade -y
```

## Installing OpenCV
###### 3. Now the OpenCV installation can begin.
Click [here](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) and follow the steps exactly to make sure OpenCV is installed properly.

After following the online tutorial, OpenCV should be installed and in perfect working condition.

To test:
```
python
>>>import cv2
```
