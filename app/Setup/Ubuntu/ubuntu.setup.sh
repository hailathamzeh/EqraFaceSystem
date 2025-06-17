#!/bin/bash
#fobeid 00962799599100 com.fobeid@gmail.com

# cd ~ && sudo apt-get update && sudo apt-get install wget && wget -O - https://hafiz.s3.amazonaws.com/demo/hikvision/ubuntu.setup.sh | bash


cd
cd ~
sudo apt-get update
sudo apt-get install wget
wget -q https://hafiz.s3.amazonaws.com/demo/hikvision/EqraTech-IPCam.zip -O ~/EqraTech-IPCam.zip
sudo apt-get install unzip
sudo unzip -o EqraTech-IPCam.zip -d EqraTech-IPCam

sudo apt-get update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
#sudo apt-get install python3.7
sudo apt-get install python3.8
sudo apt-get install -y python3-pip
sudo apt-get install -y build-essential
sudo apt-get install -y git
sudo apt-get install -y python3
sudo apt-get install -y python3-dev

sudo apt-get install pyqt5-tools
sudo apt-get install libxcb-xinerama0


pip install cmake==3.22.6
pip install IPython==8.4.0
pip install imutils==0.5.4
pip install numpy==1.21.6
pip install pyqt5==5.15.4
pip install pyqt5-tools==5.15.4.3.2
pip install PyQt-builder==1.13.0
pip install mysql-connector-python==8.0.30
pip install pillow==7.1.2 
pip install wheel==0.34.2

#restart computer
pip install opencv-python==4.2.0.32
pip install deepface==0.0.75
pip install dlib==19.24.0
pip install face_recognition==1.3.0


## TODO Run
sudo chown -R $USER ~/EqraTech-IPCam
sudo chown -R $USER ~/EqraTech-IPCam/*
cd ~/EqraTech-IPCam
python3 UserInterface.py





 pip install pyserial
 ls /dev/ttyACM0
 sudo chmod a+rw /dev/ttyACM0
 
 # ESP8266 # ESP-12E NodeMCU
 ls /dev/ttyUSB0
 sudo chmod a+rw /dev/ttyUSB0
 
lesson 1 ::  https://www.youtube.com/watch?v=vbQCL4Zf5co
lesson 2 ::  https://www.youtube.com/watch?v=kobG0EgDwI0
lesson 3 ::  https://www.youtube.com/watch?v=qZsJoGATdn8
lesson 4 ::  https://www.youtube.com/watch?v=AS2cItK1d2s
 

 
import serial
arduinoData = serial.Serial('/dev/ttyACM0', 9600)
arduinoData.write('T'.encode())

