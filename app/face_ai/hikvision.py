# by fobeid com.fobeid@gmail.com
import cv2
import sys
import logging as log
import datetime as dt
import imutils # pip install imutils
from datetime import datetime
from time import sleep
from recognition import detect_id
from threading import Thread
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print("ROOT_DIR",ROOT_DIR)

#http://192.168.1.22/doc/page/login.asp?_1662457803794&page=config
#http://192.168.1.22/ISAPI/Streaming/channels/1/picture

cascPath = ROOT_DIR + "/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='hikvision.log',level=log.INFO)

# todo by PC camera
#cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture()

# get Original resolution (default as per settings)
cap.open("rtsp://admin:abcd1234@192.168.1.22:554/Streaming/channels/1")

cap.set(cv2.CAP_PROP_SETTINGS, 1)
#cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

# width 640.0 height 360.0
#cap.open("rtsp://admin:abcd1234@192.168.1.22:554/Streaming/channels/2")

_WIDTH = 640
_HEIGHT = 360

# _WIDTH = 1280
# _HEIGHT = 720

#_WIDTH = 2688
#_HEIGHT = 1520

#_WIDTH = 3840
#_HEIGHT = 2160

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap.set(cv2.CAP_PROP_FPS, 50)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("width",width)
print("height",height)

anterior = 0
timestamp = 0

anteriors = [0]
times = [0]

def detect(img):
    fTime = dt.datetime.now().timestamp()
    print("detecting...")
    nImagePath = (ROOT_DIR+"/do/"+str(dt.datetime.now()).replace(':','-')+".jpeg")
    # TODO Save jpeg
    cv2.imwrite(nImagePath, img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    try:
        detect_id(nImagePath, 0.8, 4 , ROOT_DIR+"/id_folder" )
    except:
        print("An exception occurred")  
    finally:
        os.remove(nImagePath) 
    sTime = dt.datetime.now().timestamp()
    diff = sTime - fTime
    print(diff)


while True:

    # when Unable to load camera
    if not cap.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Change Resolution Cam
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, _WIDTH)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _HEIGHT)
    #cap.set(cv2.CAP_PROP_FPS, 100)

    # Capture frame-by-frame
    ret, frame = cap.read()

    # tmp image
    img_1280w_720h = frame
    #img_1280w_720h = imutils.resize(frame, width=1280, height=720)

    # Change Frame Size if more than 1280w 720h
    frame = imutils.resize(frame, width=_WIDTH, height=_HEIGHT)
    
    # Display the resulting frame
    #cv2.imshow('HikVision', frame) 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)  
        
    if anterior != len(faces):
        anterior = len(faces)
        #log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        cTime = int(round(datetime.timestamp(datetime.now())))
        if cTime - timestamp > 3:
        	timestamp = cTime
        	nTask = Thread(target=detect, args=(img_1280w_720h,))
        	nTask.start()
        	#nTask.join()
   
    cv2.imshow('HikVision', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #if cv2.waitKey(1) & 0xFF == ord('s'):
    #    nTask = Thread(target=detect, args=(img_1280w_720h,))
    #    nTask.start()   

    #print(str(dt.datetime.now()))

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
