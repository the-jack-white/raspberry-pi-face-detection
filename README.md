# Raspberry Pi Face Detection Camera
This project shows you how to setup a functioning facial detection camera using a Raspberry Pi and a PiCam V2 and then automatically upload the data to an AWS S3 bucket.


## First configuring the Raspberry Pi
###### 1. Load Raspbian onto the Pi device.
Download Raspbian off the [official site](https://www.raspberrypi.org/downloads/) and use [Etcher](https://www.balena.io/etcher/) to flash Raspbian to the MicroSD card.

###### 2. Uninstall all unnecessary programs.
Run the following in the Terminal to remove all unnecessary programs:
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
If an error is displayed then something went wrong and then the process needs to be redone.

## Setting up the facial detection code
###### 4. Creating directory
Download this repository in /home/pi/ directory and unzip.

###### 5. Give full permission
Give *launcher.sh* full permissions by typing:
```
chmod 777 launcher.sh
```

###### 6. Create the directory for the saved images.
Create the *dataset* directory in /home/pi/ directory by typing: ```mkdir dataset```

**NOTE**: Do not use a different name for the directory, or else AWS will not be able to connect to this directory.

###### 7. Run script to make sure everything is working
Make sure *detector.py* works by running:
```
python detector.py
```

**NOTE**: Don't run ```sh launcher.sh``` as it won't show a display, because it is used for the automation process.<br>
**NOTE**: If *detector.py* gives an error, run ```sudo modprobe bcm2835-v4l2``` and run ```python detector.py``` again.

## Script automation
###### 8. Ensure script runs automatically upon booting up the Pi.
In order to automate the *detector.py* script, we'll have to edit the *crontab*. In order to do so, run the following in the Terminal:
```
sudo crontab -e
```
**NOTE**: If the Terminal asks what editor to use, it doesn't really matter. I personally keep it to the NANO editor which is the default editor.

The *crontab* gives a brief description on how the syntax works, so feel free to go through that.

Add the following to the bottom line of the *crontab*:
```
@reboot sh /home/pi/faceDetection/launcher.sh >/home/pi/logs/cronlog 2>&1
```

After the *crontab* has been updated, the *logs* directory needs to be created in order to log any errors that could show up in the automation, if this is the case.

```cd``` to the /home/pi/ directory and create the *logs* directory by typing ```mkdir logs```.

Once the Pi is rebooted, the script should now be automatically running in the background and take pictures of any faces that are detected. Upon first boot, consult the *cronlog* that has been created in the *logs* directory (created in previous step). If the *cronlog* is empty, then you can be sure that everything is working, or else the error will be displayed within the *cronlog*.

## Connecting to AWS S3.
**NOTE**: You should already have an AWS account with valid credentials in order to continue with this step.

###### 9. Prepare to install S3Tools and connect to AWS.
```cd``` to root directory and give writing permissions by typing:
```
sudo su
```

Create a directory, *scripts*, by typing ```mkdir scripts```, ```cd``` into *scripts* and create a file called *datasend.sh* by typing ```touch datasend.sh```. Once *datasend.sh* has been created, use the NANO editor to open the *datasend.sh* file, by typing ```nano datasend.sh```, and add the following lines of code to *datasend.sh*:
```
s3=/usr/local/bin/s3cmd
logfile=/var/log/pisync.log
data_dir=/home/pi/dataset
s3_location=S3_BUCKETNAME   #Add own S3 bucket name
$s3 sync $data_dir s3://$s3_location
if [ $? -eq 0 ]; then
     	rm -rf $data_dir/*
        echo "Success Sync to Cloud `date`" >> $logfile
        else
        echo "Failed to execute sync command `date`" >> $logfile
fi
```
**NOTE**: Replace *S3_BUCKETNAME* in code shown above with the name of your own S3 bucket.<br>
**NB**:  

* The bucket name should be EXACTLY the same as the bucket name in AWS S3.
* There should be no spaces in the bucket name, as it can cause errors.
* Try not to use an exsiting bucket, rather create a brand new bucket, as it can also create errors.
