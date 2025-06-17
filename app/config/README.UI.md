# README #


### HikVision-IP-Camera-UI-Python

* download python 3.7

sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
	
	
* For Windows download MySQL Installer 8.0.30 (mysql-installer-community-8.0.30.0.msi)
https://dev.mysql.com/downloads/installer/


#$ sudo apt install python3.8-venv
#$ python3 -m venv ./venv
#$ source venv/bin/activate
#(venv) $ pip install pyqt5==5.15.4 pyqt5-tools==5.15.4.3.2


* python libraries: 


pip install pyqt5==5.15.4
pip install pyqt5-tools==5.15.4.3.2
pip install PyQt-builder==1.13.0
pip install mysql-connector-python==8.0.30
pip install imutils==0.5.4


## deepface 0.0.75 has requirement opencv-python>=4.5.5.64,
pip install opencv-python==4.2.0.32 ## use this for ui
pip install opencv-python==4.6.0.66 ## dont used this


$ python3 UserInterface.py # For Ubuntu
$ python UserInterface.py # For windows