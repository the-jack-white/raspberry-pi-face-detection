import cv2
import os
#from time import gmtime, strftime
import time
import datetime

#add the Haar Cascades for testing data
face_cascade = cv2.CascadeClassifier ('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier ('haarcascade_eye.xml')

#Use video camera, 0 ----> first assigned camera
cap = cv2.VideoCapture(0)
cap.set(3, 640) # set video width
cap.set(4, 480) # set video height
count = 0

#vdate = strftime("%a_%d_%b_%Y_")
#htime = strftime("%H-")
#mtime = strftime("%M-")
#stime = strftime("%S_")

d = datetime.date.today()
#ddate = str(d.day) + "_" + str(d.year) + "_" + str(d.hour) + "_" + str(d.minute) + "_" + str(d.second)

while (True):
    #read what is displayed on the camera
    ret, img = cap.read()

    #convert to grey scale, for better processing
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #create the detection boarders around features
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        #cv2.imwrite("dataset/s001/" + "S001_" + "C01_" + date + htime + mtime + stime + str(count) + ".jpg", img)
        cv2.imwrite("dataset/s001/" + "S001_C01_" + str(d) + "_" + time.strftime("%H_%M_%S") + ".jpg", img)
            
        for (ex, ey, ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew,ey+eh), (0,255,0), 2)

        count += 1

#Add a display window
    #cv2.imshow('img',img)  #Uncomment for window
  
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    #elif count >= 5:
    #    break
    elif count >= 1: # After the first image is taken, the whole process will be delayed with 2 seconds (so will capture on the 1st and 4th, etc, second)
        time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()

#Version 6 Notes:   The naming convention gave a bit of trouble where it didn't want to write the images in the "dataset"
#                   folder, although the whole script was passed through successfully. 
