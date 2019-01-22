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
@reboot sh /home/pi/raspberry-pi-face-detection-master/launcher.sh >/home/pi/logs/cronlog 2>&1
```
**NOTE**: */home/pi/raspberry-pi-face-detection-master/launcher.sh* should be the exact file path to the *launcher.sh* file.

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

###### 10. Installing S3Tools
Create another directory with any name you want ```mkdir DIRECTORY_NAME``` and ```cd``` into it.

Follow the next set of commands in order to install S3Tools, else you can follow the tutorial directly by clicking [here](https://rbgeek.wordpress.com/2014/07/16/how-to-install-the-latest-version-of-s3cmd-tool-on-linux/).

* Install the required packages before installing S3Tools.
```
sudo yum install unzip python-pip
```
```
wget https://github.com/s3tools/s3cmd/archive/master.zip
```

* Unzip the downloaded source zip and ```cd``` into it.
```
unzip master.zip
```
```
cd s3cmd-master/
```

* Run the following command:
```
sudo python setup.py install
```

* Next, install the *dateutil* module, which is powerful extensions to the datetime module.
```
sudo pip install python-dateutil
```

* Check the installed version of s3cmd tool:
```
s3cmd --version
```

* After the installation, run the following command to configure your s3cmd tools using your **AMAZON ACCESS KEY** and **SECRET KEY**.
```
s3cmd --configure
```

* A prompt will appear where it asks you for both, your Access Key and Secret Key. Add both and a few more prompts will appear, but you can just use the default input by hitting *ENTER* for every prompt, until it asks you:

> Test access with supplied credentials? [Y/n]
```
y
```

* You should then get a prompt saying:

> Success. Your access key and secret key worked fine :-)

* If you get this prompt, it will then ask you to save settings:
```
y
```

* S3Tools is then successfully installed and you can continue, or else redo this process if you've encountered anything that I did not mention.

**NOTE**: You can repeat this process any time you want.

###### 11. Add the final few steps
If you made it this far then you can be sure that S3Tools is working smoothly.

Next, we need to go back to *crontab* to add the automation to AWS uploading:
```
sudo crontab -e
```
Then add the following to the bottom line:
```
*/5 * * * * /scripts/datasend.sh > /dev/null 2>&1
```
This should upload everything , with an interval of 5 minutes, that is in the *dataset* directory, created in step 6, to the S3 bucket you specified in step 9.

You can test this by ```cd``` into the *dataset* directory and running the following command to create a test image and wait for it to upload to your bucket:
```
raspistill -o test.jpg
```
**NOTE**: This command will also allow you to see if your camera is connected properly.

If the *test.jpg* file is uploaded sucessfully, then you can congratulate yourself to have a fully functioning facial detection system that uploads the data to the AWS cloud.
