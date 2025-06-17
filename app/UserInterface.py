# by fobeid com.fobeid@gmail.com 00962799599100
import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms"

import serial

import sys
import _IO
#import _IO_Mysql
import _IO_sqlite
from _User import User
from _AttendanceRecord import AttendanceRecord
from _Cam import Cam
import secrets
import shutil
from csv import DictReader

from face_ai.recognition import (generate_id, detect_id, del_id) # *
#from face_ai.recognition import detect_id

#http://192.168.1.22/doc/page/login.asp?_1662457803794&page=config
#http://192.168.1.22/ISAPI/Streaming/channels/1/picture

import cv2
import numpy as np
import logging as log
import datetime as dt
import imutils # pip install imutils
from datetime import datetime
from time import sleep
from threading import Thread
import json
from json.decoder import JSONDecodeError
import CapturePicture

arduinoData = None
try:
    arduinoData = serial.Serial('/dev/ttyACM0', 9600)
except:
    print()


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print("ROOT_DIR",ROOT_DIR)

_OUTPUT_FOLDER_NAME = '_Output'

_CAM_FOLDER_NAME = _OUTPUT_FOLDER_NAME+os.sep+'_Cam'
_CAM_DIR = ROOT_DIR+os.sep+_CAM_FOLDER_NAME+os.sep

_DO_FOLDER_NAME = _OUTPUT_FOLDER_NAME+os.sep+'_Do'
_DO_DIR = ROOT_DIR+os.sep+_DO_FOLDER_NAME+os.sep

_UNKNOWN_FOLDER_NAME = _OUTPUT_FOLDER_NAME+os.sep+'_Unknown'
_UNKNOWN_DIR = ROOT_DIR+os.sep+_UNKNOWN_FOLDER_NAME+os.sep

_KNOWN_FOLDER_NAME = _OUTPUT_FOLDER_NAME+os.sep+'_Known'
_KNOWN_DIR = ROOT_DIR+os.sep+_KNOWN_FOLDER_NAME+os.sep

_FACE_AI_ID_FOLDER_DIR = ROOT_DIR+os.sep+'face_ai'+os.sep+'id_folder'

from distutils import extension
from PyQt5 import (QtGui, QtCore, QtWidgets)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
QComboBox, QDialog, QMessageBox, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
QLineEdit, QMenu, QMenuBar, QSpinBox, QTextEdit, QVBoxLayout, QInputDialog, QFileDialog, QTableWidget,
QTableWidgetItem,QRadioButton,QStyle,QScrollArea)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QThread)

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        # try:
        #     filelist = [ f for f in os.listdir(_DO_DIR) if f.endswith(".jpeg") ]
        #     for f in filelist:
        #         os.remove(os.path.join(_DO_DIR, f))
        # except:
        #     print()
        #
        # try:
        #     filelist = [ f for f in os.listdir(_CAM_DIR) if f.endswith(".jpeg") ]
        #     for f in filelist:
        #         os.remove(os.path.join(_CAM_DIR, f))
        # except:
        #     print()

        self.title = _IO._titale
        self.left = 0
        self.top = 0
        self.width = _IO._width_Screen_Available
        self.height = _IO._height_Screen_Available
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage(_IO._allRightsReserved)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()
      
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        ## TODO LiveCams
        self.LiveCams_Models = None
        self.LiveCams_QLabels = None
        self.LiveCams_Threads = None

        ## TODO AttendanceRecord
        self.aRecords_LOGs = None
        self.aRecord_LOGs = None
        self.aRecordIndex_LOGs = -1
        self.cLogCount_LOGs = -1
        self.cLogPage_LOGs = -1
        self.cLogPages_LOGs = -1

        ## TODO CamRecord
        self.aRecords_Cams = None
        self.aRecord_Cams = None
        self.aRecordIndex_Cams = -1
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.LiveCamera_tab = QWidget()
        self.AttendanceRecord_tab = QWidget()
        self.AddNewPerson_tab = QWidget()
        self.Cams_tab = QWidget()
        self.tabs.resize(_IO._width_Screen_Available,_IO._height_Screen_Available)
        
        # Add tabs
        self.tabs.addTab(self.LiveCamera_tab,_IO._liveCamera)
        self.tabs.addTab(self.AttendanceRecord_tab,_IO._attendanceRecord)
        self.tabs.addTab(self.AddNewPerson_tab,_IO._addNewPerson)
        self.tabs.addTab(self.Cams_tab,_IO._Cams)

        # create tabs
        self.CreateLiveCameraTab()
        self.CreateAttendanceRecordTab()
        self.CreateAddNewPersonTab()
        self.CreateCamsTab()
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
           
    ## TODO 1.LiveCamera TAB
    def CreateLiveCameraTab(self):


        # Scroll Area which contains the widgets, set as the centralWidget
        self.VideoFramesScroll = QScrollArea()

        # Widget that contains the collection of Vertical Box
        self.VideoFramesWidget = QWidget()

        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.VideoFramesHBoxes = QHBoxLayout()

        #TODO Add List of live Cameras
        #self.updateLiveCamsList()
        #for i in range(1,50):
        #    object = QLabel("TextLabel")
        #    self.VideoFramesHBoxes.addWidget(object)

        self.VideoFramesWidget.setLayout(self.VideoFramesHBoxes)

        #Scroll Area Properties
        self.VideoFramesScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.VideoFramesScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.VideoFramesScroll.setWidgetResizable(True)
        self.VideoFramesScroll.setWidget(self.VideoFramesWidget)


        #self.VideoFrame = QLabel(self)
        #self.VideoFrame.setAlignment(Qt.AlignCenter)
        #self.VideoFrame.resize(_IO._widthCamFrame, _IO._heightCamFrame)

        self.LogLabel = QLabel(_IO._log+":")
        self.LogTextEdit = QTextEdit(self)
        self.LogTextEdit.resize(_IO._width_Screen_Available, _IO._heightCamFrame)
        self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

        self.vbox = QGroupBox(self)
        layout = QFormLayout()
        #layout.addRow(self.VideoFrame)
        layout.addRow(self.VideoFramesScroll)
        layout.addRow(self.LogLabel)
        layout.addRow(self.LogTextEdit)
        self.vbox.setLayout(layout)

        self.LiveCamera_tab.layout = QVBoxLayout(self)
        self.LiveCamera_tab.layout.addWidget(self.vbox)
        self.LiveCamera_tab.setLayout(self.LiveCamera_tab.layout)

        self.updateLiveCamsList()

        ## create the video capture thread
        #self._VideoThread = VideoThread()
        ## connect its signal to the update_image slot
        #self._VideoThread.ListenerOnChangePixmapSignal.connect(self.OnUpdateLiveImage_VideoThread)
        #self._VideoThread.ListenerOnFaceDetect.connect(self.OnFaceDetect_VideoThread)
        #self._VideoThread.ListenerOnLog.connect(self.OnLog_VideoThread)
        ## start the thread
        #self._VideoThread.start()
        
    
    def updateLiveCamsList(self):

        self.LiveCams_Models = _IO_sqlite.getCams()
        self.LiveCams_QLabels = []
        self.LiveCams_Threads = []
        for xID,xCam in enumerate(self.LiveCams_Models):
            
            print('xID', xID)
            print('xCam', xCam.toString())

            nVideoFrame = QLabel(str(xCam.getIp()), self)
            nVideoFrame.setAlignment(Qt.AlignCenter)
            nVideoFrame.resize(int(_IO._widthCamFrame*0.75),int(_IO._heightCamFrame*0.75))
            
            # add QLabel Widget
            self.VideoFramesHBoxes.addWidget(nVideoFrame)
            
            # create the video capture thread
            _VideoThread = VideoThread(xID, xCam, nVideoFrame)
            _VideoThread.ListenerOnChangePixmapSignal.connect(self.OnUpdateLiveImage_VideoThread)
            _VideoThread.ListenerOnFaceDetect.connect(self.OnFaceDetect_VideoThread)
            _VideoThread.ListenerOnLog.connect(self.OnLog_VideoThread)
            _VideoThread.start()

            ## append new QLabel
            self.LiveCams_QLabels.append(nVideoFrame)

            ## append new Thread
            self.LiveCams_Threads.append(_VideoThread)

        


    def ConvertImageToQPixmap(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(int(_IO._widthCamFrame*0.85), int(_IO._heightCamFrame*0.85), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    ## TODO Listener VideoThread [OnUpdateLiveImage_VideoThread,OnLog_VideoThread,OnFaceDetect_VideoThread]
    @pyqtSlot(list)
    def OnUpdateLiveImage_VideoThread(self, values):
        
        xIMG = values[0]
        xID = values[1]
        xCam = values[2]
        xVideoFrameQLabel = values[3]

        #print('update_image')
        """Updates the image_label with a new opencv image"""
        qt_img = self.ConvertImageToQPixmap(xIMG)
        # TODO show live camera
        #self.VideoFrame.setPixmap(qt_img)
        #self.LiveCams_QLabels[xID].setPixmap(qt_img)
        xVideoFrameQLabel.setPixmap(qt_img)

    @pyqtSlot(list)
    def OnLog_VideoThread(self, values):

        xID = values[0]
        xCam = values[1]
        xVideoFrameQLabel = values[2]
        xLog = values[3]

        self.LogTextEdit.append(xCam.getIp()+" "+xLog) 
        self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

    @pyqtSlot(list)
    def OnFaceDetect_VideoThread(self, values):

        def syncDetectBinaryThread(self, img):

            # try:
            #     ## ui frezen
            #     if self._DetectBinaryThread is not None:
            #         print('isFinished' , self._DetectBinaryThread.isFinished())
            #         print('isRunning' , self._DetectBinaryThread.isRunning())
            #         #isFinished True
            #         #isRunning False
            #         while self._DetectBinaryThread.isRunning() and not self._DetectBinaryThread.isFinished():
            #             print('sleeeeeeeep')
            #             sleep(0.1)

            # except:
            #     print('is null _DetectBinaryThread')

            try:
                # create the video capture thread
                self._DetectBinaryThread = DetectBinaryThread(img)
                self._DetectBinaryThread.ListenerOnLog.connect(self.OnLog_DetectBinaryThread)
                self._DetectBinaryThread.ListenerOnResult.connect(self.OnResult_DetectBinaryThread)
                self._DetectBinaryThread.finished.connect(self._DetectBinaryThread.kill)
                # start the thread
                self._DetectBinaryThread.start() 
                #self._DetectBinaryThread.wait()
            except:
                print('ERR :: QThread: Destroyed while thread is still running')

        xIMG = values[0]
        xID = values[1]
        xCam = values[2]
        xVideoFrameQLabel = values[3]

        # # create the video capture thread
        # self._DetectBinaryThread = DetectBinaryThread(xIMG)
        # self._DetectBinaryThread.ListenerOnLog.connect(self.OnLog_DetectBinaryThread)
        # self._DetectBinaryThread.ListenerOnResult.connect(self.OnResult_DetectBinaryThread)
        # self._DetectBinaryThread.finished.connect(self._DetectBinaryThread.kill)
        # # start the thread
        # self._DetectBinaryThread.start() 
        # #self._DetectBinaryThread.wait()

        try:
            nTask = Thread(target=syncDetectBinaryThread, args=(self, xIMG,))
            nTask.start()
            nTask.join() # to solve ERR :: QThread: Destroyed while thread is still running , ui frezen
        except:
            print('ERR :: QThread: Destroyed while thread is still running')
        
    ## TODO Listener DetectBinaryThread [OnLog_DetectBinaryThread,OnResult_DetectBinaryThread]
    @pyqtSlot(str)
    def OnLog_DetectBinaryThread(self, cLog):
        self.LogTextEdit.append(cLog) 
        self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

    @pyqtSlot(str,str,str)
    def OnResult_DetectBinaryThread(self, nJSON, nImagePath, nImageID):
        print("OnResult_DetectBinaryThread")
        print("nJSON :: "+nJSON)
        print("nImageID :: "+nImageID)
        print("nImagePath :: "+nImagePath)
        
        self.LogTextEdit.append("OnResult_DetectBinaryThread")
        self.LogTextEdit.append("nJSON :: "+nJSON)
        self.LogTextEdit.append("nImageID :: "+nImageID)
        self.LogTextEdit.append("nImagePath :: "+nImagePath)
        self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

        try:
            #nJSON = nJSON.replace("'",'"')

            #print(type(nJSON))
            #cJSON = json.dumps(str(nJSON))
            #cJSON = json.dumps(nJSON)
            cJSON = json.loads(nJSON)
            #cJSON = nJSON
            #print(type(cJSON))
            #print('cJSON',cJSON)
            
            try:
                ids = cJSON['data']
                #print(type(ids))
                #data = json.dumps(ids)
                #print('ids', ids)
                for nInfo in ids:
                    cId = nInfo['id']
                    #cId = 'Unknown'
                    #print(cId)
                    print("User key is :: "+str(cId))
                    self.LogTextEdit.append("User key is :: "+str(cId))
                    self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

                    if cId == 'Unknown' or cId == 'unknown' or cId == '':
                        nPath = str(_UNKNOWN_DIR+nImageID)
                        print("nImagePath :: "+nPath)
                        self.LogTextEdit.append("nImagePath :: "+nPath)
                        #_IO_Mysql.insertLog(cId, cId, nPath)
                        _IO_sqlite.insertLog(cId, cId, nPath)
                        try:
                            #os.rename(nImagePath,nPath)
                            #shutil.move(nImagePath,nPath)
                            shutil.copyfile(nImagePath,nPath)
                            print("os.copied to :: "+nPath)
                            self.LogTextEdit.append("os.copied to :: "+nPath)
                        except:
                            print("can't copy image from : "+nImagePath+" , to : "+nPath)
                            self.LogTextEdit.append("can't move image from : "+nImagePath+" , to : "+nPath)
                    else:
                        #cUser = _IO_Mysql.getUserInfo(cId)
                        cUser = _IO_sqlite.getUserInfo(cId)
                        #print("getUserInfo :: ", cUser)
                        if cUser:
                            print("UserInfo: "+cUser.toString())
                            self.LogTextEdit.append("UserInfo: "+cUser.toString())
                            self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

                            if(cUser.getName() == 'FaisalObeid'):
                                self.LogTextEdit.append("TTTTTTTTTTTTTTTTTTTTTTT")
                                try:
                                    arduinoData.write('T'.encode())
                                except:
                                    print()
                            elif(cUser.getName() == 'dr.Hussein'):
                                self.LogTextEdit.append("TTTTTTTTTTTTTTTTTTTTTTT")
                                try:
                                    arduinoData.write('T'.encode())
                                except:
                                    print()

                            #isUserLogged =_IO_Mysql.isUserLogged_before_5_minutes(cUser.getKey())
                            isUserLogged =_IO_sqlite.isUserLogged_before_5_minutes(cUser.getKey())
                            if not isUserLogged:
                                nPath = str(_KNOWN_DIR+nImageID)
                                print("nImagePath :: "+nPath)
                                self.LogTextEdit.append("nImagePath :: "+nPath)
                                #_IO_Mysql.insertLog(cUser.getKey(), cUser.getName(), nPath)
                                _IO_sqlite.insertLog(cUser.getKey(), cUser.getName(), nPath)
                                try:
                                    #os.rename(nImagePath,nPath)
                                    #shutil.move(nImagePath,nPath)
                                    shutil.copyfile(nImagePath,nPath)
                                    print("os.copied to :: "+nPath)
                                    self.LogTextEdit.append("os.copied to :: "+nPath)
                                except:
                                    print("can't copy image from : "+nImagePath+" , to : "+nPath)
                                    self.LogTextEdit.append("can't move image from : "+nImagePath+" , to : "+nPath)
                            else:
                                print("warning: This user was logged less than 5 minutes ago")
                                self.LogTextEdit.append("warning: This user was logged less than 5 minutes ago")
                        else:
                            print("warning: This user has a Key but it is not in the database")
                            self.LogTextEdit.append("warning: This user has a Key but it is not in the database")
                
                try:
                    #os.remove(nImagePath)
                    print("os.remove :: "+nImagePath)
                    self.LogTextEdit.append("os.remove :: "+nImagePath)
                except:
                    print("can't remove image from : "+nImagePath)
                    self.LogTextEdit.append("can't remove image from : "+nImagePath)
                    
            #except JSONDecodeError as err:
            except JSONDecodeError as err:
                print("ERR:: JSON 0.1"+err.msg)
                self.LogTextEdit.append("ERR:: JSON 0.1"+err.msg)
                self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)
            except:
                print("ERR:: JSON 0.2")
                self.LogTextEdit.append("ERR:: JSON 0.2")
                self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)
        except JSONDecodeError as err:
            print("ERR:: JSON 1.1"+err.msg)
            self.LogTextEdit.append("ERR:: JSON 1.1"+err.msg)
            self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)
        except:
            print("ERR:: JSON 1.2")
            self.LogTextEdit.append("ERR:: JSON 1.2")
            self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

        self.LogTextEdit.moveCursor(QtGui.QTextCursor.End)

    ## TODO 2.AttendanceRecord TAB
    def CreateAttendanceRecordTab(self):
       
        self.AttendanceRecord_tab.layout = QGridLayout(self)
        self.AttendanceRecord_tab.layout.maximumSize().setHeight(int(_IO._height_Screen_Available*0.9))
        self.AttendanceRecord_tab.layout.maximumSize().setWidth(int(_IO._width_Screen_Available*0.9))

        #self.AttendanceRecord_tab.layout.setColumnStretch(1, 2)
        #self.AttendanceRecord_tab.layout.setRowStretch(3, 1)
        
        ## Search
        self.CreateAttendanceRecord_SearchForm()
        self.SearchGroupBox.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.SearchGroupBox.setMaximumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.AttendanceRecord_tab.layout.addWidget(self.SearchGroupBox, 0, 0)

        ## Table
        self.CreateAttendanceRecord_Table()
        self.tableWidget.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.tableWidget.setMaximumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.AttendanceRecord_tab.layout.addWidget(self.tableWidget, 1, 0, alignment=Qt.AlignHCenter)

        # ## UserInfo
        self.CreateAttendanceRecord_UserInfo()
        self.UserInfoGroupBox.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.9))
        self.UserInfoGroupBox.setMaximumWidth(int((_IO._width_Screen_Available/2)* 0.9))
        self.AttendanceRecord_tab.layout.addWidget(self.UserInfoGroupBox, 1, 1, alignment=Qt.AlignHCenter)

        ## Pages
        self.CreateAttendanceRecord_Pages()
        self.PagesGroupBox.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.PagesGroupBox.setMaximumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.AttendanceRecord_tab.layout.addWidget(self.PagesGroupBox, 2, 0, alignment=Qt.AlignHCenter)

        self.AttendanceRecord_tab.setLayout(self.AttendanceRecord_tab.layout)

        ## set Init Table info
        self.aRecords_LOGs = None
        self.aRecord_LOGs = None
        self.aRecordIndex_LOGs = -1
        self.cLogCount_LOGs = -1
        self.cLogPage_LOGs = -1
        self.cLogPages_LOGs = -1
        self.UpdateTableInfo_AttendanceRecord(None,None,0)

    ## TODO Search AttendanceRecord
    def CreateAttendanceRecord_SearchForm(self):

        self.SearchGroupBox = QGroupBox(_IO._search)
        layout = QHBoxLayout()

        # TODO search : Search_QLineEdit_2
        self.Search_QLineEdit_2 = QLineEdit(self)
        self.Search_QLineEdit_2.setPlaceholderText(_IO._search_holderText)
        layout.addWidget(self.Search_QLineEdit_2)

        # TODO dateHolder : Date_QLineEdit_2
        self.DateHolder_QLineEdit_2 = QLineEdit(self)
        self.DateHolder_QLineEdit_2.setPlaceholderText(_IO._date_holderText)
        self.DateHolder_QLineEdit_2.setReadOnly(True)
        self.DateHolder_QLineEdit_2.mousePressEvent = self.OnDateHolderClick_AttendanceRecord
        layout.addWidget(self.DateHolder_QLineEdit_2)

        # TODO dateValue : Date_QDateEdit_2
        self.DateValue_QDateEdit_2 = QtWidgets.QDateEdit(calendarPopup=True)
        layout.addWidget(self.DateValue_QDateEdit_2)
        self.DateValue_QDateEdit_2.setVisible(False)
        self.DateValue_QDateEdit_2.setDisplayFormat("yyyy-MM-dd")
        
        
        self.SearchBtn_2 = QPushButton(_IO._search, self)
        self.SearchBtn_2.clicked.connect(self.OnSearchBtn_AttendanceRecord)
        layout.addWidget(self.SearchBtn_2)

        self.CleanBtn_2 = QPushButton(_IO._clean, self)
        self.CleanBtn_2.clicked.connect(self.OnCleanBtn_AttendanceRecord)
        layout.addWidget(self.CleanBtn_2)
        
        self.SearchGroupBox.setLayout(layout)

    def ResetSearchForm_AttendanceRecord(self):
        self.Search_QLineEdit_2.setText("")
        self.DateValue_QDateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.DateValue_QDateEdit_2.setVisible(False)
        self.DateHolder_QLineEdit_2.setVisible(True)
        qdate = QtCore.QDate.fromString("2000-01-01", "yyyy-MM-dd")
        self.DateValue_QDateEdit_2.setDate(qdate)

    def OnDateHolderClick_AttendanceRecord(self, event):
        self.DateHolder_QLineEdit_2.setVisible(False)
        self.DateValue_QDateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.DateValue_QDateEdit_2.setVisible(True)

    def OnSearchBtn_AttendanceRecord(self):
        cSearchValue = self.Search_QLineEdit_2.text()
        cDateValue = self.DateValue_QDateEdit_2.date() 
        toPyDate = str(cDateValue.toPyDate())

        
        self.aRecords_LOGs = None
        self.aRecord_LOGs = None
        self.aRecordIndex_LOGs = -1
        self.cLogCount_LOGs = -1
        self.cLogPage_LOGs = -1
        self.cLogPages_LOGs = -1
        self.UpdateTableInfo_AttendanceRecord(cSearchValue,toPyDate,0)
        
    def OnCleanBtn_AttendanceRecord(self):
        self.ResetSearchForm_AttendanceRecord()

    ## TODO UserInfo AttendanceRecord
    def CreateAttendanceRecord_UserInfo(self):

        self.UserInfoGroupBox = QGroupBox(_IO._userInfo, self)
        layout = QFormLayout()

        # ImageView_QLabel_2
        self.ImageView_QLabel_2 = QLabel(self)
        self.ImageView_QLabel_2.setMaximumWidth(int(_IO._widthCamFrame*0.9))
        self.ImageView_QLabel_2.setMaximumHeight(int(_IO._heightCamFrame*0.9))
        self.ImageView_QLabel_2.resize(int(_IO._widthCamFrame*0.9),int(_IO._heightCamFrame))

        # TODO name : Name_QLineEdit_2
        self.Name_QLineEdit_2 = QLineEdit(self)

        # TODO gender : Gender_ComboBox_2
        self.Gender_ComboBox_2 = QComboBox(self)
        self.Gender_ComboBox_2.addItems(_IO.gender_list)
        self.Gender_ComboBox_2.setCurrentIndex(2)

        # TODO deatails : Deatails_QLineEdit_2
        self.Deatails_QLineEdit_2 = QLineEdit(self)

        # TODO age : Age_QSpinBox_2
        self.Age_QSpinBox_2 = QSpinBox(self)
        self.Age_QSpinBox_2.setMinimum(1)
        self.Age_QSpinBox_2.setMaximum(125)

        # TODO skinColor : SkinColor_QLineEdit_2
        self.SkinColor_QLineEdit_2 = QLineEdit(self)

        # TODO Save Btn
        SaveBtn_2 = QPushButton(_IO._addNewPerson)
        SaveBtn_2.clicked.connect(self.OnSaveBtn_AttendanceRecord)
        
        # TODO Delete Btn
        DeleteBtn_2 = QPushButton(_IO._deleteLog)
        DeleteBtn_2.clicked.connect(self.OnDeleteBtn_AttendanceRecord)

        # TODO FormAddNewPersonBtns
        UserInfo_QDialogBtns = QDialogButtonBox()
        UserInfo_QDialogBtns.addButton(SaveBtn_2, QDialogButtonBox.ActionRole)
        UserInfo_QDialogBtns.addButton(DeleteBtn_2, QDialogButtonBox.ActionRole)
        
        layout.addRow(self.ImageView_QLabel_2)
        layout.addRow(QLabel(_IO._name+":"), self.Name_QLineEdit_2)
        layout.addRow(QLabel(_IO._gender+":"), self.Gender_ComboBox_2)
        layout.addRow(QLabel(_IO._details+":"), self.Deatails_QLineEdit_2)
        layout.addRow(QLabel(_IO._age+":"), self.Age_QSpinBox_2)
        layout.addRow(QLabel(_IO._skinColor+":"), self.SkinColor_QLineEdit_2)
        layout.addRow(UserInfo_QDialogBtns)

        self.UserInfoGroupBox.setLayout(layout)

    def UpdateUserInfo_AttendanceRecord(self):

        if self.aRecord_LOGs is None or self.aRecordIndex_LOGs == -1:
            pixmap = QPixmap(None)
            self.ImageView_QLabel_2.setPixmap(pixmap)
            self.Name_QLineEdit_2.setText(str(''))
            self.Gender_ComboBox_2.setCurrentText(str(_IO.gender_list[2]))
            self.Deatails_QLineEdit_2.setText(str(''))
            self.Age_QSpinBox_2.setValue(1)
            self.SkinColor_QLineEdit_2.setText(str(''))

            self.PagesValue_QLineEdit_2.setText(str(''))
            self.PrevBtn_2.setEnabled(False)
            self.NextBtn_2.setEnabled(False)
            return

        if self.aRecordIndex_LOGs != -1 and self.aRecords_LOGs is not None and len(self.aRecords_LOGs) > 0 and self.aRecord_LOGs is not None and self.aRecordIndex_LOGs < len(self.aRecords_LOGs):
            #self.aRecord = self. get objext
            #self.aRecordIndex = self. get index

            imageSrc = self.aRecord_LOGs.getPath()
            if imageSrc and self.ImageView_QLabel_2 and os.path.exists(imageSrc):
                pixmap = QPixmap(imageSrc)
                pixmap = pixmap.scaled(int(_IO._widthCamFrame*0.85),int(_IO._heightCamFrame*0.85), QtCore.Qt.KeepAspectRatio)
                self.ImageView_QLabel_2.setPixmap(pixmap)
                

            self.Name_QLineEdit_2.setText(str(self.aRecord_LOGs.getName()))
            self.Gender_ComboBox_2.setCurrentText(((_IO.gender_list[2],self.aRecord_LOGs.getGender())[bool(self.aRecord_LOGs.getGender() is not None and self.aRecord_LOGs.getGender() in _IO.gender_list)]))
            self.Deatails_QLineEdit_2.setText(str(self.aRecord_LOGs.getDetails()))
            self.Age_QSpinBox_2.setValue(((1,self.aRecord_LOGs.getAge())[bool(self.aRecord_LOGs.getAge() is not None and isinstance(self.aRecord_LOGs.getAge(), int))]))
            self.SkinColor_QLineEdit_2.setText(str(self.aRecord_LOGs.getSkinColor()))

            self.tableWidget.selectRow(self.aRecordIndex_LOGs)

    def OnDeleteBtn_AttendanceRecord(self):

        if self.aRecord_LOGs is None or self.aRecordIndex_LOGs == -1:
            return

        print('OnDeleteBtn_AttendanceRecord')
        print('aRecord',self.aRecord_LOGs.toString())
        print('aRecordIndex',self.aRecordIndex_LOGs)

        if self.aRecordIndex_LOGs != -1 and self.aRecords_LOGs is not None and len(self.aRecords_LOGs) > 0 and self.aRecord_LOGs is not None and self.aRecordIndex_LOGs < len(self.aRecords_LOGs):
            req = QMessageBox.question(self, _IO._deleteLog, _IO._deleteLogAsk, QMessageBox.Yes, QMessageBox.No)
            if req == QMessageBox.Yes:
                #isDeleteLog = _IO_Mysql.deleteLog(self.aRecord.getId(), self.aRecord.getKey(), self.aRecord.getName())
                isDeleteLog = _IO_sqlite.deleteLog(self.aRecord_LOGs.getId(), self.aRecord_LOGs.getKey(), self.aRecord_LOGs.getName())
                if isDeleteLog:
                    self.tableWidget.removeRow(self.aRecordIndex_LOGs)
                    self.aRecords_LOGs.pop(self.aRecordIndex_LOGs)
                    #self.tableWidget.move(0,0)
                    if len(self.aRecords_LOGs) > 0:
                        self.aRecord_LOGs = self.aRecords_LOGs[0]
                        self.aRecordIndex_LOGs = 0
                        self.UpdateUserInfo_AttendanceRecord()
                    else:
                        self.aRecords_LOGs = None
                        self.aRecord_LOGs = None
                        self.aRecordIndex_LOGs = -1
                        self.UpdateUserInfo_AttendanceRecord()
                    QMessageBox.question(self, _IO._deleteLog, _IO._deleteLogSucc, QMessageBox.Ignore, QMessageBox.Ignore)
                else:
                    QMessageBox.question(self, _IO._deleteLog, _IO._deleteLogErr, QMessageBox.Ignore, QMessageBox.Ignore)
        
    def OnSaveBtn_AttendanceRecord(self):
        
        if self.aRecord_LOGs is None or self.aRecordIndex_LOGs == -1:
            return

        print('OnSaveBtn_AttendanceRecord')
        print('aRecord',self.aRecord_LOGs.toString())
        print('aRecordIndex',self.aRecordIndex_LOGs)

        if self.aRecordIndex_LOGs != -1 and self.aRecords_LOGs is not None and len(self.aRecords_LOGs) > 0 and self.aRecord_LOGs is not None and self.aRecordIndex_LOGs < len(self.aRecords_LOGs):

            imageFile = self.aRecord_LOGs.getPath()
            fileNameSplit = imageFile.split(".")
            extensionPath = fileNameSplit[-1]
            imageType = str(extensionPath).lower()
            name = self.Name_QLineEdit_2.text()
            gender = str(self.Gender_ComboBox_2.currentText())
            details = self.Deatails_QLineEdit_2.text()
            age = self.Age_QSpinBox_2.value()
            skinColor = self.SkinColor_QLineEdit_2.text()
            print("imageFile", imageFile)
            print("imageType", imageType)
            print("name", name)
            print("gender", gender)
            print("details", details)
            print("age", age)
            print("skinColor", skinColor)
            ## TODO please check your input data (Validation)

            if imageFile is None or imageFile == '' or (not os.path.exists(imageFile)):
                QMessageBox.question(self, _IO._addNewPerson, _IO._img_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return
        
            if name is None or name == '' or len(name) < 3:
                QMessageBox.question(self, _IO._addNewPerson, _IO._name_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return

            if gender is None and gender != '' and gender not in _IO.gender_list:
               QMessageBox.question(self, _IO._addNewPerson, _IO._gender_err, QMessageBox.Ignore, QMessageBox.Ignore)
               return

            if age is None and age != '':
                try:
                    age = int(age)
                except:
                    QMessageBox.question(self, _IO._addNewPerson, _IO._age_err, QMessageBox.Ignore, QMessageBox.Ignore)
                    return

            userKey = secrets.token_hex(24)
            print("userKey", userKey)

            nUser = User(userKey, '', name, details, gender, age, skinColor)

            isGenerated = generate_id(imageFile, userKey, _IO._FACE_AI_CPUs, _FACE_AI_ID_FOLDER_DIR )
            print("isGenerated", isGenerated)

            if isGenerated:
                #isInsertUser = _IO_Mysql.insertUser(nUser)
                isInsertUser = _IO_sqlite.insertUser(nUser)
                print("isInsertUser", isInsertUser)
                if isInsertUser:

                    try:
                        oldPath = imageFile
                        newPath = oldPath.replace(_UNKNOWN_DIR, _KNOWN_DIR)
                        shutil.copyfile(oldPath,newPath)
                        imageFile = newPath
                    except:
                        newPath = imageFile

                    #isUpdatedLog = _IO_Mysql.updateLog(self.aRecord.getId(), nUser.getKey(), nUser.getName(), imageFile)
                    isUpdatedLog = _IO_sqlite.updateLog(self.aRecord_LOGs.getId(), nUser.getKey(), nUser.getName(), imageFile)
                    print("isUpdatedLog", isUpdatedLog)
                    if isUpdatedLog:

                        # update tmp model
                        self.aRecord_LOGs = AttendanceRecord(self.aRecord_LOGs.getId(), nUser.getKey(), str(self.aRecord_LOGs.getCreatedAt()), nUser.getName(), str(imageFile), details, gender, skinColor, age)
                        print("n aRecord", self.aRecord_LOGs.toString())

                        # Update inside table
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,0, QTableWidgetItem(str(self.aRecord_LOGs.getKey())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,1, QTableWidgetItem(str(self.aRecord_LOGs.getName())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,2, QTableWidgetItem(str(self.aRecord_LOGs.getCreatedAt())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,3, QTableWidgetItem(str(self.aRecord_LOGs.getDetails())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,4, QTableWidgetItem(str(self.aRecord_LOGs.getGender())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,5, QTableWidgetItem(str(self.aRecord_LOGs.getSkinColor())))
                        self.tableWidget.setItem(self.aRecordIndex_LOGs,6, QTableWidgetItem(str(self.aRecord_LOGs.getAge())))

                        # Update inside Form
                        self.UpdateUserInfo_AttendanceRecord()
                        
                        QMessageBox.question(self, _IO._addNewPerson, _IO._adapt_succ, QMessageBox.Ok, QMessageBox.Ok)
                    else:
                        QMessageBox.question(self, _IO._addNewPerson, _IO._insertAdapt_DB_err, QMessageBox.Ignore, QMessageBox.Ignore)
                else:
                    del_id( userKey, _FACE_AI_ID_FOLDER_DIR)
                    QMessageBox.question(self, _IO._addNewPerson, _IO._insertAdapt_DB_err, QMessageBox.Ignore, QMessageBox.Ignore)
            else:
                QMessageBox.question(self, _IO._addNewPerson, _IO._adapt_err, QMessageBox.Ignore, QMessageBox.Ignore)

    ## TODO Table AttendanceRecord
    def CreateAttendanceRecord_Table(self):

        # Create table
        self.tableWidget = QTableWidget(self)
             
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)

        #columns = ['Key','Name','CreatedAt','Path','Details','Gender','SkinColor','Age']
        columns = ['Key','Name','CreatedAt','Details','Gender','SkinColor','Age']
        self.tableWidget.setHorizontalHeaderLabels(columns)

        #self.tableWidget.horizontalHeader().setVisible(True)
        #self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        #self.tableWidget.horizontalHeader().setDefaultSectionSize(140)
        #self.tableWidget.horizontalHeader().setHighlightSections(False)
        #self.tableWidget.horizontalHeader().setMinimumSectionSize(75)
        #self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        #self.tableWidget.horizontalHeader().setStretchLastSection(False)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

        # table selection change (on Click)
        self.tableWidget.clicked.connect(self.OnTableClicked_AttendanceRecord)
        
    def UpdateTableInfo_AttendanceRecord(self, cSearchText, cDate, cSkip):
        
        self.UpdateUserInfo_AttendanceRecord()
                
        if cSearchText is not None and cSearchText == '':
            cSearchText = None
        if cDate is not None and cDate == '2000-01-01':
            cDate = None

        print("cSearchText", cSearchText)
        print("cDate", cDate)
        
        if self.tableWidget:
            self.tableWidget.setRowCount(0)
            self.aRecords_LOGs = None
            self.aRecord_LOGs = None
            self.aRecordIndex_LOGs = -1

            #self.cLogCount = -1
            #self.cLogPage = -1
            #self.cLogPages = -1

            if self.cLogCount_LOGs == -1:
                #self.cLogCount = _IO_Mysql.getLogsCount(cSearchText, cDate)
                self.cLogCount_LOGs = _IO_sqlite.getLogsCount(cSearchText, cDate)
                try:
                    self.cLogPages_LOGs = self.cLogCount_LOGs / _IO._SQL_MAX_LIMIT_SELECT
                    cLogPages = int(self.cLogPages_LOGs)
                    #print('self.cLogPages',self.cLogPages)
                    #print('cLogPages',cLogPages)
                    if self.cLogPages_LOGs > cLogPages:
                        self.cLogPages_LOGs = int(self.cLogPages_LOGs)
                        self.cLogPages_LOGs += 1
                    self.cLogPages_LOGs = int(self.cLogPages_LOGs)
                except:
                    self.cLogPages_LOGs = 1
                #print('self.cLogPages',self.cLogPages)

            #self.aRecords = _IO_Mysql.getLogs(cSearchText, cDate, cSkip)
            self.aRecords_LOGs = _IO_sqlite.getLogs(cSearchText, cDate, cSkip)

            if self.cLogCount_LOGs > 0 and self.aRecords_LOGs and len(self.aRecords_LOGs) > 0:
                
                self.tableWidget.setRowCount(len(self.aRecords_LOGs))
                
                for idx, row in enumerate(self.aRecords_LOGs):
                    #print(idx, row.toString())

                    self.tableWidget.setItem(idx,0, QTableWidgetItem(str(row.getKey())))
                    self.tableWidget.setItem(idx,1, QTableWidgetItem(str(row.getName())))
                    self.tableWidget.setItem(idx,2, QTableWidgetItem(str(row.getCreatedAt())))
                    self.tableWidget.setItem(idx,3, QTableWidgetItem(str(row.getDetails())))
                    self.tableWidget.setItem(idx,4, QTableWidgetItem(str(row.getGender())))
                    self.tableWidget.setItem(idx,5, QTableWidgetItem(str(row.getSkinColor())))
                    self.tableWidget.setItem(idx,6, QTableWidgetItem(str(row.getAge())))

                self.aRecord_LOGs = self.aRecords_LOGs[0]
                self.aRecordIndex_LOGs = 0
                self.UpdateUserInfo_AttendanceRecord()

                if self.cLogCount_LOGs > 0:
                    try:
                        self.cLogPage_LOGs = int(cSkip/_IO._SQL_MAX_LIMIT_SELECT)
                    except:
                        self.cLogPage_LOGs = 0
                    self.cLogPage_LOGs += 1
                    print('cLogCount',self.cLogCount_LOGs)
                    print('cLogPages',self.cLogPages_LOGs)
                    print('cLogPage',self.cLogPage_LOGs)
                    
                    self.PagesValue_QLineEdit_2.setText(str(self.cLogPage_LOGs)+" / "+str(self.cLogPages_LOGs))
                    
                    if self.cLogPage_LOGs > 1:
                        self.PrevBtn_2.setEnabled(True)
                    else:
                        self.PrevBtn_2.setEnabled(False)

                    if self.cLogPages_LOGs - self.cLogPage_LOGs >= 1:
                        self.NextBtn_2.setEnabled(True)
                    else:
                        self.NextBtn_2.setEnabled(False)
                   
    def OnTableClicked_AttendanceRecord(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            cRowIndex = currentQTableWidgetItem.row()
            cColumnIndex = currentQTableWidgetItem.column()
            #print('OnTableClicked', cRowIndex, cColumnIndex, currentQTableWidgetItem.text())
            if self.aRecords_LOGs is not None and self.aRecords_LOGs and len(self.aRecords_LOGs) > 0 and cRowIndex < len(self.aRecords_LOGs):
                self.aRecord_LOGs = self.aRecords_LOGs[cRowIndex]
                self.aRecordIndex_LOGs = cRowIndex
                self.UpdateUserInfo_AttendanceRecord()

    ## TODO Pages AttendanceRecord
    def CreateAttendanceRecord_Pages(self):
        
        self.PagesGroupBox = QGroupBox(self)
        layout = QHBoxLayout()
        
        self.PrevBtn_2 = QPushButton(self)
        pixmapi_SP_ArrowBack = QStyle.StandardPixmap.SP_ArrowBack
        icon_SP_ArrowBack = self.style().standardIcon(pixmapi_SP_ArrowBack)
        self.PrevBtn_2.setIcon(icon_SP_ArrowBack)
        self.PrevBtn_2.clicked.connect(self.OnPrevBtn_AttendanceRecord)
        layout.addWidget(self.PrevBtn_2)

        # # TODO pagesValue : PagesValue_QLineEdit_2
        self.PagesValue_QLineEdit_2 = QLineEdit(self)
        self.PagesValue_QLineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.PagesValue_QLineEdit_2.returnPressed.connect(self.OnPressedPagesValue_AttendanceRecord)
        layout.addWidget(self.PagesValue_QLineEdit_2)

        self.NextBtn_2 = QPushButton(self)
        pixmapi_SP_SP_ArrowForward = QStyle.StandardPixmap.SP_ArrowForward
        icon_SP_SP_ArrowForward = self.style().standardIcon(pixmapi_SP_SP_ArrowForward)
        self.NextBtn_2.setIcon(icon_SP_SP_ArrowForward)
        self.NextBtn_2.clicked.connect(self.OnNextBtn_AttendanceRecord)
        layout.addWidget(self.NextBtn_2)
      
        
        self.PagesGroupBox.setLayout(layout)

    def OnPrevBtn_AttendanceRecord(self):

        if self.cLogCount_LOGs <= 25:
            return

        if self.cLogPage_LOGs <= 1:
            return
        
        nSkip = (self.cLogPage_LOGs - 2) * _IO._SQL_MAX_LIMIT_SELECT
        print('nSkip', nSkip)

        if nSkip < self.cLogCount_LOGs:
            cSearchValue = self.Search_QLineEdit_2.text()
            cDateValue = self.DateValue_QDateEdit_2.date() 
            toPyDate = str(cDateValue.toPyDate())

            self.aRecords_LOGs = None
            self.aRecord_LOGs = None
            self.aRecordIndex_LOGs = -1
            self.cLogCount_LOGs = -1
            self.cLogPage_LOGs = -1
            self.cLogPages_LOGs = -1
            self.UpdateTableInfo_AttendanceRecord(cSearchValue,toPyDate,nSkip)

    def OnNextBtn_AttendanceRecord(self):
        
        if self.cLogCount_LOGs <= 25:
            return

        if self.cLogPages_LOGs - self.cLogPage_LOGs < 1:
            return
        
        nSkip = self.cLogPage_LOGs * _IO._SQL_MAX_LIMIT_SELECT
        if nSkip < 0:
            nSkip = 0
        print('nSkip', nSkip)

        if nSkip > 0 and nSkip < self.cLogCount_LOGs:
            cSearchValue = self.Search_QLineEdit_2.text()
            cDateValue = self.DateValue_QDateEdit_2.date() 
            toPyDate = str(cDateValue.toPyDate())

            self.aRecords_LOGs = None
            self.aRecord_LOGs = None
            self.aRecordIndex_LOGs = -1
            self.cLogCount_LOGs = -1
            self.cLogPage_LOGs = -1
            self.cLogPages_LOGs = -1
            self.UpdateTableInfo_AttendanceRecord(cSearchValue,toPyDate,nSkip)

    def OnPressedPagesValue_AttendanceRecord(self):

        nPage = self.PagesValue_QLineEdit_2.text()
        try:
            nPageInt = int(nPage)
            print('OnPressedPagesValue', nPageInt)

            if self.cLogCount_LOGs <= 25:
                return

            if nPageInt <= 0:
                return

            if nPageInt > self.cLogPages_LOGs:
                return

            nSkip = (nPageInt - 1) * _IO._SQL_MAX_LIMIT_SELECT
            if nSkip < 0:
                nSkip = 0
            print('nSkip', nSkip)

            if nSkip < self.cLogCount_LOGs:
                cSearchValue = self.Search_QLineEdit_2.text()
                cDateValue = self.DateValue_QDateEdit_2.date() 
                toPyDate = str(cDateValue.toPyDate())

                self.aRecords_LOGs = None
                self.aRecord_LOGs = None
                self.aRecordIndex_LOGs = -1
                self.cLogCount_LOGs = -1
                self.cLogPage_LOGs = -1
                self.cLogPages_LOGs = -1
                self.UpdateTableInfo_AttendanceRecord(cSearchValue,toPyDate,nSkip)

        except:
            print('OnPressedPagesValue except :', nPage)

    ## TODO 3.AddNewPerson TAB
    def CreateAddNewPersonTab(self):

        ## TODO Form Two
        self.FormImportAddNewPerson = QGroupBox(_IO._import_csv_file)
        ImportLayout = QFormLayout()

        # TODO csvNote : CSVNote_QLabel_1
        self.CSVNote_QLabel_1 = QLabel(_IO._csv_file_header_note, self)

        # TODO csvFile : CSVFile_QLineEdit_1
        self.CSVFile_QLineEdit_1 = QLineEdit(self)
        self.CSVFile_QLineEdit_1.setClearButtonEnabled(True)
        self.CSVFile_QLineEdit_1.setReadOnly(True)
        self.CSVFile_QLineEdit_1.setPlaceholderText(_IO._csv_file_hint_msg)
        self.CSVFile_QLineEdit_1.mousePressEvent = self.OnCSVFile_SelectCSVFileNameDialog

        # TODO csvFile : CSVFile_QLineEdit_1
        self.CSVLog_QLabel_1 = QLabel(self)


        # TODO process Btn
        self.ProcessBtn_1 = QPushButton(_IO._process)
        self.ProcessBtn_1.clicked.connect(self.OnProcessBtn_AddNewPerson)
        
        # TODO FormAddNewPersonBtns
        FormImportAddNewPersonBtns = QDialogButtonBox()
        FormImportAddNewPersonBtns.addButton(self.ProcessBtn_1, QDialogButtonBox.ActionRole)


        ImportLayout.addRow(self.CSVNote_QLabel_1)
        ImportLayout.addRow(QLabel(_IO._csv_file+":"), self.CSVFile_QLineEdit_1)
        ImportLayout.addRow(QLabel(_IO._log+":"), self.CSVLog_QLabel_1)
        ImportLayout.addRow(FormImportAddNewPersonBtns)
        self.FormImportAddNewPerson.setLayout(ImportLayout)


        ## TODO Form One
        self.FormAddNewPerson = QGroupBox(_IO._addNewPerson, self)
        layout = QFormLayout()

        # ImageView_QLabel_1
        self.ImageView_QLabel_1 = QLabel(self)
        #self.ImageView_QLabel_1.setMinimumHeight(250)
        #self.ImageView_QLabel_1.setMinimumWidth(250)
        #self.ImageView_QLabel_1.setMaximumHeight(250)
        #self.ImageView_QLabel_1.setMaximumWidth(250)
        pixmap = QPixmap(ROOT_DIR+"/camera.jpeg")
        pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.ImageView_QLabel_1.setPixmap(pixmap)
        self.ImageView_QLabel_1.mousePressEvent = self.OnCapturePictureClick_AddNewPerson
        self.ImageView_QLabel_1.setAlignment(Qt.AlignHCenter)

        # TODO imageFile : ImageFile_QLineEdit_1
        self.ImageFile_QLineEdit_1 = QLineEdit(self)
        self.ImageFile_QLineEdit_1.setClearButtonEnabled(True)
        self.ImageFile_QLineEdit_1.setReadOnly(True)
        self.ImageFile_QLineEdit_1.setPlaceholderText(_IO._imageFile_hint_msg)
        self.ImageFile_QLineEdit_1.mousePressEvent = self.OnImageFile_SelectImageFileNameDialog
        self.ImageFile_QLineEdit_1.addAction(QIcon(ROOT_DIR+"/camera.jpeg"), QLineEdit.TrailingPosition)
        #self.ImageFile_QLineEdit_1.actionEvent = self.OnImageFile_SelectImageFileNameDialog
        #self.ImageFile_QLineEdit_1.installEventFilter(self)
        #goto_action = QtWidgets.QAction('&Go to Function', self.ImageFile_QLineEdit_1)
        #goto_action.triggered.connect(self.OnCapturePictureClick_AddNewPerson)

        # TODO imageType : ImageType_ComboBox_1
        self.ImageType_ComboBox_1 = QComboBox(self)
        self.ImageType_ComboBox_1.addItems(_IO.imageType_list)
        self.ImageType_ComboBox_1.setCurrentIndex(0)
        self.ImageType_ComboBox_1.setEnabled(False)

        # TODO name : Name_QLineEdit_1
        self.Name_QLineEdit_1 = QLineEdit(self)

        # TODO gender : Gender_ComboBox_1
        self.Gender_ComboBox_1 = QComboBox(self)
        self.Gender_ComboBox_1.addItems(_IO.gender_list)
        self.Gender_ComboBox_1.setCurrentIndex(2)

        # TODO deatails : Deatails_QLineEdit_1
        self.Deatails_QLineEdit_1 = QLineEdit(self)

        # TODO age : Age_QSpinBox_1
        self.Age_QSpinBox_1 = QSpinBox(self)
        self.Age_QSpinBox_1.setMinimum(1)
        self.Age_QSpinBox_1.setMaximum(125)

        # TODO skinColor : SkinColor_QLineEdit_1
        self.SkinColor_QLineEdit_1 = QLineEdit(self)

        # another design Btns
        #FormAddNewPersonBtns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.clear)
        #FormAddNewPersonBtns.accepted.connect(self.on_click)
        #FormAddNewPersonBtns.rejected.connect(self.on_click)

        # TODO Save Btn
        SaveBtn_1 = QPushButton(_IO._save)
        SaveBtn_1.clicked.connect(self.OnSaveBtn_AddNewPerson)
        #SaveBtn.setDefault(True)
        #SaveBtn.setCheckable(True)

        # TODO Clean Btn
        CleanBtn_1 = QPushButton(_IO._clean)
        CleanBtn_1.clicked.connect(self.OnCleanBtn_AddNewPerson)
        #CleanBtn.setCheckable(True)
        #CleanBtn.setAutoDefault(False)

        # TODO FormAddNewPersonBtns
        FormAddNewPersonBtns = QDialogButtonBox()
        FormAddNewPersonBtns.addButton(SaveBtn_1, QDialogButtonBox.ActionRole)
        FormAddNewPersonBtns.addButton(CleanBtn_1, QDialogButtonBox.ActionRole)

        layout.addRow(self.ImageView_QLabel_1)
        layout.addRow(QLabel(_IO._imageFile+":"), self.ImageFile_QLineEdit_1)
        layout.addRow(QLabel(_IO._imageType+":"), self.ImageType_ComboBox_1)
        layout.addRow(QLabel(_IO._name+":"), self.Name_QLineEdit_1)
        layout.addRow(QLabel(_IO._gender+":"), self.Gender_ComboBox_1)
        layout.addRow(QLabel(_IO._details+":"), self.Deatails_QLineEdit_1)
        layout.addRow(QLabel(_IO._age+":"), self.Age_QSpinBox_1)
        layout.addRow(QLabel(_IO._skinColor+":"), self.SkinColor_QLineEdit_1)
        layout.addRow(FormAddNewPersonBtns)
        layout.addRow(self.FormImportAddNewPerson)
        
        self.FormAddNewPerson.setLayout(layout)

        self.AddNewPerson_tab.layout = QVBoxLayout(self)
        self.AddNewPerson_tab.layout.addWidget(self.FormAddNewPerson)
        self.AddNewPerson_tab.setLayout(self.AddNewPerson_tab.layout)

    def OnCapturePictureClick_AddNewPerson(self, event):
        print('OnCapturePictureClick_AddNewPerson')
        imageSrc = CapturePicture.getPhoto()
        if imageSrc is None:
            print('turn on your cam')
        elif imageSrc and self.ImageView_QLabel_1 and os.path.exists(imageSrc):
            print('imageSrc', imageSrc)
            pixmap = QPixmap(imageSrc)
            pixmap = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
            self.ImageView_QLabel_1.setPixmap(pixmap)
            self.ImageFile_QLineEdit_1.setText(str(imageSrc))
            fileNameSplit = imageSrc.split(".")
            extensionPath = fileNameSplit[-1]
            extensionPath = str(extensionPath).lower()
            self.ImageType_ComboBox_1.setCurrentText(extensionPath)
            return
        else:
            print('turn on your cam')

    def OnSaveBtn_AddNewPerson(self):
        imageFile = self.ImageFile_QLineEdit_1.text()
        imageType = str(self.ImageType_ComboBox_1.currentText())
        name = self.Name_QLineEdit_1.text()
        gender = str(self.Gender_ComboBox_1.currentText())
        details = self.Deatails_QLineEdit_1.text()
        age = self.Age_QSpinBox_1.value()
        skinColor = self.SkinColor_QLineEdit_1.text()
        print("imageFile", imageFile)
        print("imageType", imageType)
        print("name", name)
        print("gender", gender)
        print("details", details)
        print("age", age)
        print("skinColor", skinColor)
        ## TODO please check your input data (Validation)

        if imageFile is None or imageFile == '' or (not os.path.exists(imageFile)):
            QMessageBox.question(self, _IO._addNewPerson, _IO._img_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return
        
        if name is None or name == '' or len(name) < 3:
            QMessageBox.question(self, _IO._addNewPerson, _IO._name_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return

        if gender is None and gender != '' and gender not in _IO.gender_list:
               QMessageBox.question(self, _IO._addNewPerson, _IO._gender_err, QMessageBox.Ignore, QMessageBox.Ignore)
               return

        if age is None and age != '':
            try:
                age = int(age)
            except:
                QMessageBox.question(self, _IO._addNewPerson, _IO._age_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return

        userKey = secrets.token_hex(24)
        print("userKey", userKey)

        nUser = User(userKey, '', name, details, gender, age, skinColor)

        isGenerated = generate_id(imageFile, userKey, _IO._FACE_AI_CPUs, _FACE_AI_ID_FOLDER_DIR )
        print("isGenerated", isGenerated)
        
        #isDetected = detect_id(imageFile, _IO._FACE_AI_ACCURACY, _IO._FACE_AI_CPUs , _FACE_AI_ID_FOLDER_DIR )
        #print("isDetected", isDetected)

        #isDeleted = del_id(name, _FACE_AI_ID_FOLDER_DIR )
        #print("isDeleted", isDeleted)

        if isGenerated:
            #isInsertUser = _IO_Mysql.insertUser(nUser)
            isInsertUser = _IO_sqlite.insertUser(nUser)
            print("isInsertUser", isInsertUser)
            if isInsertUser:
                QMessageBox.question(self, _IO._addNewPerson, _IO._adapt_succ, QMessageBox.Ok, QMessageBox.Ok)
                self.OnCleanBtn_AddNewPerson()
            else:
                del_id( userKey, _FACE_AI_ID_FOLDER_DIR)
                QMessageBox.question(self, _IO._addNewPerson, _IO._insertAdapt_DB_err, QMessageBox.Ignore, QMessageBox.Ignore)
        else:
            QMessageBox.question(self, _IO._addNewPerson, _IO._adapt_err, QMessageBox.Ignore, QMessageBox.Ignore)
        
    def OnCleanBtn_AddNewPerson(self):
        self.ImageFile_QLineEdit_1.clear()
        self.ImageType_ComboBox_1.setCurrentIndex(0)
        self.Name_QLineEdit_1.clear()
        self.Name_QLineEdit_1.setText("")
        self.Gender_ComboBox_1.setCurrentIndex(2)
        self.Deatails_QLineEdit_1.clear()
        self.Age_QSpinBox_1.setValue(1)
        self.SkinColor_QLineEdit_1.clear()
        pixmap = QPixmap(ROOT_DIR+"/camera.jpeg")
        pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.ImageView_QLabel_1.setPixmap(pixmap)

    def OnImageFile_SelectImageFileNameDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,_selectImageFile, "","Image Files (*.jpeg *.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        fileName, _ = QFileDialog.getOpenFileName(self,_IO._selectImageFile, "","Image Files (*.jpeg *.png *.jpg *.bmp *.gif)", options=options)
        if fileName:

            print('fileName', fileName)
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
            self.ImageView_QLabel_1.setPixmap(pixmap)
            self.ImageFile_QLineEdit_1.setText(fileName)
            fileNameSplit = fileName.split(".")
            extensionPath = fileNameSplit[-1]
            extensionPath = str(extensionPath).lower()
            self.ImageType_ComboBox_1.setCurrentText(extensionPath)
            print(extensionPath)

    def OnProcessBtn_AddNewPerson(self):
        csvFile = self.CSVFile_QLineEdit_1.text()
        print("csvFile", csvFile)
        
        self.CSVLog_QLabel_1.setText('')
        self.ProcessBtn_1.setEnabled(False)

        def syncImportCSVThread(self, csvFile):

            # create the video capture thread
            self._ImportCSVThread = ImportCSVThread(csvFile)
            self._ImportCSVThread.ListenerOnLog.connect(self.OnLog_ImportCSVThread)
            self._ImportCSVThread.ListenerOnFinish.connect(self.OnFinish_ImportCSVThread)
            # start the thread
            self._ImportCSVThread.start()

        try:
            nTask = Thread(target=syncImportCSVThread, args=(self, csvFile,))
            nTask.start()
            nTask.join() # to solve ERR :: QThread: Destroyed while thread is still running , ui frezen
        except:
            print('ERR :: QThread: Destroyed while thread is still running')
        
    def OnCSVFile_SelectCSVFileNameDialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,_selectImageFile, "","Image Files (*.jpeg *.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        fileName, _ = QFileDialog.getOpenFileName(self,_IO._selectImageFile, "","Image Files (*.csv *.tsv)", options=options)
        if fileName:
            print('fileName', fileName)
            self.CSVFile_QLineEdit_1.setText(fileName)

    ## TODO Listener ImportCSVThread [OnLog_ImportCSVThread,OnFinish_ImportCSVThread]
    @pyqtSlot(str)
    def OnLog_ImportCSVThread(self, cLog):
        self.CSVLog_QLabel_1.setText(str(cLog))
  
    @pyqtSlot(str)
    def OnFinish_ImportCSVThread(self, cLog):
        self.CSVLog_QLabel_1.setText(str(cLog))
        self.ProcessBtn_1.setEnabled(True)

    ## TODO 4.Cams TAB
    def CreateCamsTab(self):
       
        self.Cams_tab.layout = QGridLayout(self)
        self.Cams_tab.layout.maximumSize().setHeight(int(_IO._height_Screen_Available*0.9))
        self.Cams_tab.layout.maximumSize().setWidth(int(_IO._width_Screen_Available*0.9))

        #self.Cams_tab.layout.setColumnStretch(1, 1)
        #self.Cams_tab.layout.setRowStretch(1, 1)

        ## Table
        self.CreateCams_Table()
        self.CamTableWidget.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.Cams_tab.layout.addWidget(self.CamTableWidget, 1, 0, alignment=Qt.AlignHCenter)

        # ## CamInfo
        self.CreateCams_CamInfo()
        self.CamInfoGroupBox.setMinimumWidth(int((_IO._width_Screen_Available/2)* 0.90))
        self.Cams_tab.layout.addWidget(self.CamInfoGroupBox, 1, 1, alignment=Qt.AlignHCenter)

        self.Cams_tab.setLayout(self.Cams_tab.layout)

        ## set Init Table info
        self.aRecords_Cams = None
        self.aRecord_Cams = None
        self.aRecordIndex_Cams = -1

        self.UpdateTableInfo_CamsRecord()

    ## TODO Table Cams
    def CreateCams_Table(self):

        # Create table
        self.CamTableWidget = QTableWidget(self)
             
        self.CamTableWidget.setRowCount(0)
        self.CamTableWidget.setColumnCount(6)

        columns = [_IO._CreatedAt, _IO._IP, _IO._Port, _IO._Username, _IO._Password, _IO._Details]

        self.CamTableWidget.setHorizontalHeaderLabels(columns)

        #self.CamTableWidget.horizontalHeader().setVisible(True)
        #self.CamTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        #self.CamTableWidget.horizontalHeader().setDefaultSectionSize(140)
        #self.CamTableWidget.horizontalHeader().setHighlightSections(False)
        #self.CamTableWidget.horizontalHeader().setMinimumSectionSize(75)
        #self.CamTableWidget.horizontalHeader().setSortIndicatorShown(False)
        #self.CamTableWidget.horizontalHeader().setStretchLastSection(False)
        #self.CamTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.CamTableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.CamTableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.CamTableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.CamTableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.CamTableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.CamTableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        # table selection change (on Click)
        self.CamTableWidget.clicked.connect(self.OnTableClicked_CamsRecord)

    def UpdateTableInfo_CamsRecord(self):
        
        self.UpdateCamsInfo_CamInfo()               
        
        if self.CamTableWidget:
            self.CamTableWidget.setRowCount(0)
            self.aRecords_Cams = None
            self.aRecord_Cams = None
            self.aRecordIndex_Cams = -1

            if self.aRecordIndex_Cams == -1 or self.aRecords_Cams is None:
                self.aRecords_Cams = _IO_sqlite.getCams()
                
            if self.aRecords_Cams and len(self.aRecords_Cams) > 0:
                
                self.CamTableWidget.setRowCount(len(self.aRecords_Cams))
                
                for idx, row in enumerate(self.aRecords_Cams):
                    #print(idx, row.toString())
                    self.CamTableWidget.setItem(idx,0, QTableWidgetItem(str(row.getCreatedAt())))
                    self.CamTableWidget.setItem(idx,1, QTableWidgetItem(str(row.getIp())))
                    self.CamTableWidget.setItem(idx,2, QTableWidgetItem(str(row.getPort())))
                    self.CamTableWidget.setItem(idx,3, QTableWidgetItem(str(row.getUsername())))
                    self.CamTableWidget.setItem(idx,4, QTableWidgetItem(str(row.getPassword())))
                    self.CamTableWidget.setItem(idx,5, QTableWidgetItem(str(row.getDetails())))

                self.aRecord_Cams = self.aRecords_Cams[0]
                self.aRecordIndex_Cams = 0
                self.UpdateCamsInfo_CamInfo()

    def OnTableClicked_CamsRecord(self):
        print('--OnTableClicked_CamsRecord')
        for currentQTableWidgetItem in self.CamTableWidget.selectedItems():
            cRowIndex = currentQTableWidgetItem.row()
            cColumnIndex = currentQTableWidgetItem.column()
            #print('OnTableClicked', cRowIndex, cColumnIndex, currentQTableWidgetItem.text())
            if self.aRecords_Cams is not None and self.aRecords_Cams and len(self.aRecords_Cams) > 0 and cRowIndex < len(self.aRecords_Cams):
                self.aRecord_Cams = self.aRecords_Cams[cRowIndex]
                self.aRecordIndex_Cams = cRowIndex
                self.UpdateCamsInfo_CamInfo()

    ## TODO CamInfo Cams
    def CreateCams_CamInfo(self):

        self.CamInfoGroupBox = QGroupBox(_IO._camInfo, self)
        layout = QFormLayout()

        #columns = ['createdAt','ip','port','username','password','details']

        # TODO ip : IP_QLineEdit_4
        self.IP_QLineEdit_4 = QLineEdit(self)

        # TODO port : Port_QLineEdit_4
        self.Port_QLineEdit_4 = QLineEdit(self)

        # TODO username : Username_QLineEdit_4
        self.Username_QLineEdit_4 = QLineEdit(self)

        # TODO password : Password_QLineEdit_4
        self.Password_QLineEdit_4 = QLineEdit(self)

        # TODO deatails : Deatails_QLineEdit_4
        self.Deatails_QLineEdit_4 = QLineEdit(self)

        # TODO Add Btn
        AddBtn_4 = QPushButton(_IO._add)
        AddBtn_4.clicked.connect(self.OnAddBtn_CamInfo)

        # TODO Update Btn
        UpdateBtn_4 = QPushButton(_IO._update)
        UpdateBtn_4.clicked.connect(self.OnUpdateBtn_CamInfo)
        
        # TODO Delete Btn
        DeleteBtn_4 = QPushButton(_IO._delete)
        DeleteBtn_4.clicked.connect(self.OnDeleteBtn_CamInfo)

        # TODO FormAddNewPersonBtns
        CamInfo_QDialogBtns = QDialogButtonBox()
        CamInfo_QDialogBtns.addButton(AddBtn_4, QDialogButtonBox.ActionRole)
        CamInfo_QDialogBtns.addButton(UpdateBtn_4, QDialogButtonBox.ActionRole)
        CamInfo_QDialogBtns.addButton(DeleteBtn_4, QDialogButtonBox.ActionRole)
        
        layout.addRow(QLabel(_IO._IP+":"), self.IP_QLineEdit_4)
        layout.addRow(QLabel(_IO._Port+":"), self.Port_QLineEdit_4)
        layout.addRow(QLabel(_IO._Username+":"), self.Username_QLineEdit_4)
        layout.addRow(QLabel(_IO._Password+":"), self.Password_QLineEdit_4)
        layout.addRow(QLabel(_IO._Details+":"), self.Deatails_QLineEdit_4)
        layout.addRow(CamInfo_QDialogBtns)

        self.CamInfoGroupBox.setLayout(layout)

    def UpdateCamsInfo_CamInfo(self):
        print('UpdateCamsInfo_CamInfo')


        if self.aRecords_Cams is None or self.aRecordIndex_Cams == -1:
            self.IP_QLineEdit_4.setText(str(''))
            self.Port_QLineEdit_4.setText(str(''))
            self.Username_QLineEdit_4.setText(str(''))
            self.Password_QLineEdit_4.setText(str(''))
            self.Deatails_QLineEdit_4.setText(str(''))
            return

        if self.aRecordIndex_Cams != -1 and self.aRecords_Cams is not None and len(self.aRecords_Cams) > 0 and self.aRecord_Cams is not None and self.aRecordIndex_Cams < len(self.aRecords_Cams):
            #self.aRecord_Cams = self. get objext
            #self.aRecordIndex_Cams = self. get index

            self.IP_QLineEdit_4.setText(str(self.aRecord_Cams.getIp()))
            self.Port_QLineEdit_4.setText(str(self.aRecord_Cams.getPort()))
            self.Username_QLineEdit_4.setText(str(self.aRecord_Cams.getUsername()))
            self.Password_QLineEdit_4.setText(str(self.aRecord_Cams.getPassword()))
            self.Deatails_QLineEdit_4.setText(str(self.aRecord_Cams.getDetails()))
            
            self.CamTableWidget.selectRow(self.aRecordIndex_Cams)

    def OnDeleteBtn_CamInfo(self):
        print('OnDeleteBtn_CamInfo')

        if self.aRecords_Cams is None or self.aRecordIndex_Cams == -1:
            return

        print('aRecord',self.aRecord_Cams.toString())
        print('aRecordIndex',self.aRecordIndex_Cams)

        if self.aRecordIndex_Cams != -1 and self.aRecords_Cams is not None and len(self.aRecords_Cams) > 0 and self.aRecord_Cams is not None and self.aRecordIndex_Cams < len(self.aRecords_Cams):
            req = QMessageBox.question(self, _IO._deleteCam, _IO._deleteCamAsk, QMessageBox.Yes, QMessageBox.No)
            if req == QMessageBox.Yes:
                isDeleteCam = _IO_sqlite.deleteCam(self.aRecord_Cams)
                print("isDeleteCam", isDeleteCam)
                if isDeleteCam:
                    
                    # try:
                    #     ## TODO remove frame    
                    #     #self.LiveCams_Models = _IO_sqlite.getCams()
                    #     #self.LiveCams_QLabels = []
                    #     #self.LiveCams_Threads = []
                    #     cDeleteIndex = -1
                    #     if self.LiveCams_Models is not None and len(self.LiveCams_Models) > 0:
                    #         for xID,xCam in enumerate(self.LiveCams_Models):
                    #             if self.aRecord_Cams.getId() == xCam.getId():
                    #                 self.LiveCams_Threads[xID].quit()
                    #                 self.LiveCams_Threads[xID].terminate()
                    #                 self.LiveCams_QLabels[xID].setVisible(False)
                    #                 self.VideoFramesHBoxes.removeWidget(self.LiveCams_QLabels[xID])
                    #                 cDeleteIndex = xID
                    #                 break
                    #         if cDeleteIndex != -1 and cDeleteIndex < len(self.LiveCams_Models):
                    #             self.LiveCams_Threads.pop(cDeleteIndex)
                    #             self.LiveCams_QLabels.pop(cDeleteIndex)
                    #             self.LiveCams_Models.pop(cDeleteIndex)
                    # except:
                    #     print("can't delete camera frame")

                    self.CamTableWidget.removeRow(self.aRecordIndex_Cams)
                    self.aRecords_Cams.pop(self.aRecordIndex_Cams)
                    #self.CamTableWidget.move(0,0)
                    if len(self.aRecords_Cams) > 0:
                        self.aRecord_Cams = self.aRecords_Cams[0]
                        self.aRecordIndex_Cams = 0
                        self.UpdateCamsInfo_CamInfo()
                    else:
                        self.aRecords_Cams = None
                        self.aRecord_Cams = None
                        self.aRecordIndex_Cams = -1
                        self.UpdateCamsInfo_CamInfo()


                    QMessageBox.question(self, _IO._deleteCam, _IO._deleteCamSucc, QMessageBox.Ignore, QMessageBox.Ignore)
                else:
                    QMessageBox.question(self, _IO._deleteCam, _IO._deleteCamErr, QMessageBox.Ignore, QMessageBox.Ignore)

    def OnAddBtn_CamInfo(self):
        print('OnAddBtn_CamInfo')

        nIP = self.IP_QLineEdit_4.text()
        nPort = self.Port_QLineEdit_4.text()
        nUsername = self.Username_QLineEdit_4.text()
        nPassword = self.Password_QLineEdit_4.text()
        nDeatails = self.Deatails_QLineEdit_4.text()

        print("nIP", nIP)
        print("nPort", nPort)
        print("nUsername", nUsername)
        print("nPassword", nPassword)
        print("nDeatails", nDeatails)
        ## TODO please check your input data (Validation)
    
        if nIP is None or nIP == '' or len(nIP) < 3:
            QMessageBox.question(self, _IO._addCam, _IO._ip_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return

        if nUsername is None or nUsername == '' or len(nUsername) < 3:
            QMessageBox.question(self, _IO._addCam, _IO._username_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return

        if nPassword is None or nPassword == '' or len(nPassword) < 3:
            QMessageBox.question(self, _IO._addCam, _IO._password_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return    

        if nPort is None and nPort != '':
            QMessageBox.question(self, _IO._addCam, _IO._port_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return

        try:
            nPort = int(nPort)
        except:
            QMessageBox.question(self, _IO._addCam, _IO._port_err, QMessageBox.Ignore, QMessageBox.Ignore)
            return


        #nCam = Cam(1, None, '192.168.1.22', '554', 'admin', 'abcd1234', 'entrance')
        nCam = Cam(0, None, nIP, nPort, nUsername, nPassword, nDeatails)

        isInsertCam = _IO_sqlite.insertCam(nCam)
        print("isInsertCam", isInsertCam)
        if isInsertCam:

            self.aRecords_Cams = None
            self.aRecord_Cams = None
            self.aRecordIndex_Cams = -1
            
            self.UpdateTableInfo_CamsRecord()
        
            QMessageBox.question(self, _IO._addCam, _IO._add_Came_DB_succ, QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, _IO._addCam, _IO._add_Came_DB_err, QMessageBox.Ignore, QMessageBox.Ignore)

    def OnUpdateBtn_CamInfo(self):
        print('OnUpdateBtn_CamInfo')

        if self.aRecords_Cams is None or self.aRecordIndex_Cams == -1:
            return

        print('aRecord',self.aRecord_Cams.toString())
        print('aRecordIndex',self.aRecordIndex_Cams)

        if self.aRecordIndex_Cams != -1 and self.aRecords_Cams is not None and len(self.aRecords_Cams) > 0 and self.aRecord_Cams is not None and self.aRecordIndex_Cams < len(self.aRecords_Cams):
            
            nIP = self.IP_QLineEdit_4.text()
            nPort = self.Port_QLineEdit_4.text()
            nUsername = self.Username_QLineEdit_4.text()
            nPassword = self.Password_QLineEdit_4.text()
            nDeatails = self.Deatails_QLineEdit_4.text()

            print("nIP", nIP)
            print("nPort", nPort)
            print("nUsername", nUsername)
            print("nPassword", nPassword)
            print("nDeatails", nDeatails)
            ## TODO please check your input data (Validation)
        
            if nIP is None or nIP == '' or len(nIP) < 3:
                QMessageBox.question(self, _IO._addCam, _IO._ip_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return

            if nUsername is None or nUsername == '' or len(nUsername) < 3:
                QMessageBox.question(self, _IO._addCam, _IO._username_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return

            if nPassword is None or nPassword == '' or len(nPassword) < 3:
                QMessageBox.question(self, _IO._addCam, _IO._password_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return    

            if nPort is None and nPort != '':
                QMessageBox.question(self, _IO._addCam, _IO._port_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return

            try:
                nPort = int(nPort)
            except:
                QMessageBox.question(self, _IO._addCam, _IO._port_err, QMessageBox.Ignore, QMessageBox.Ignore)
                return


            #nCam = Cam(1, None, '192.168.1.22', '554', 'admin', 'abcd1234', 'entrance')
            nCam = Cam(self.aRecord_Cams.getId(), str(self.aRecord_Cams.getCreatedAt()), nIP, nPort, nUsername, nPassword, nDeatails)

            isUpdateCam = _IO_sqlite.updateCam(nCam)
            print("isUpdateCam", isUpdateCam)
            if isUpdateCam:

                self.aRecord_Cams = nCam
                self.aRecordIndex_Cams = self.aRecordIndex_Cams

                self.CamTableWidget.setItem(self.aRecordIndex_Cams,0, QTableWidgetItem(str(self.aRecord_Cams.getCreatedAt())))
                self.CamTableWidget.setItem(self.aRecordIndex_Cams,1, QTableWidgetItem(str(self.aRecord_Cams.getIp())))
                self.CamTableWidget.setItem(self.aRecordIndex_Cams,2, QTableWidgetItem(str(self.aRecord_Cams.getPort())))
                self.CamTableWidget.setItem(self.aRecordIndex_Cams,3, QTableWidgetItem(str(self.aRecord_Cams.getUsername())))
                self.CamTableWidget.setItem(self.aRecordIndex_Cams,4, QTableWidgetItem(str(self.aRecord_Cams.getPassword())))
                self.CamTableWidget.setItem(self.aRecordIndex_Cams,5, QTableWidgetItem(str(self.aRecord_Cams.getDetails())))

                self.UpdateCamsInfo_CamInfo()

                QMessageBox.question(self, _IO._updateCam, _IO._update_Cam_DB_succ, QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.question(self, _IO._updateCam, _IO._update_Cam_DB_err, QMessageBox.Ignore, QMessageBox.Ignore)

class VideoThread(QThread):

    ListenerOnChangePixmapSignal = pyqtSignal(list)
    ListenerOnFaceDetect = pyqtSignal(list)
    ListenerOnLog = pyqtSignal(list)

    def __init__(self,xID, xCam, xVideoFrameQLabel):
        super(VideoThread,self).__init__()
        self.xID = xID
        self.xCam = xCam
        self.xVideoFrameQLabel = xVideoFrameQLabel
        self.anterior = 0
        self.timestamp = 0

    def run(self):

        cascPath = ROOT_DIR+"/config/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        #log.basicConfig(filename=ROOT_DIR+'/config/hikvision.log',level=log.INFO)

        cap = cv2.VideoCapture()
        #cap.open("rtsp://"+_IO._USERNAME_IPCAM+":"+_IO._PASSWORD_IPCAM+"@"+_IO._IP_IPCAM+":"+_IO._PORT_IPCAM+"/Streaming/channels/1")
        cap.open("rtsp://"+str(self.xCam.getUsername())+":"+str(self.xCam.getPassword())+"@"+str(self.xCam.getIp())+":"+str(self.xCam.getPort())+"/Streaming/channels/1")

        cap.set(cv2.CAP_PROP_SETTINGS, 1)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("default IPCamWidth",width)
        print("default IPCamHeight",height)

        self.ListenerOnLog.emit([self.xID, self.xCam, self.xVideoFrameQLabel , str("default IPCamWidth : "+str(width))])
        self.ListenerOnLog.emit([self.xID, self.xCam, self.xVideoFrameQLabel , str("default IPCamHeight : "+str(height))])

        while True:
            try:
                # when Unable to load camera
                if not cap.isOpened():
                    print('Unable to load camera.')
                    ## TODO Send Log on Error
                    self.ListenerOnLog.emit([self.xID, self.xCam, self.xVideoFrameQLabel , str("ERR:: Unfortunately, Camera could not be loaded, trying to reconnect...")])
                    sleep(5)
                    pass
                
                # Capture frame-by-frame
                ret, frame = cap.read()

                # tmp image
                img_1280w_720h = frame
                nWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                if float(nWidth) > 1280.0:
                    #print('nWidth', nWidth)
                    img_1280w_720h = imutils.resize(frame, width=1280, height=720)

                # Change Frame Size if more than 1280w 720h
                frame = imutils.resize(frame, width=_IO._widthCamFrame, height=_IO._heightCamFrame)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.6,
                    minNeighbors=2,
                    minSize=(30, 30)
                )
                    #scaleFactor=1.1,
                    #minNeighbors=5,
                    #minSize=(30, 30)

                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if ret:
                    ## TODO Send Img on Live Camera
                    self.ListenerOnChangePixmapSignal.emit([gray, self.xID, self.xCam, self.xVideoFrameQLabel])

                if self.anterior != len(faces):
                    self.anterior = len(faces)
                    #log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
                    cTime = int(round(datetime.timestamp(datetime.now())))
                    if float(cTime - self.timestamp) > _IO._FACE_AI_DETECT_TIME:
                        self.timestamp = cTime
                        ## TODO Send Img on Face Detect
                        self.ListenerOnFaceDetect.emit([img_1280w_720h, self.xID, self.xCam, self.xVideoFrameQLabel])

            except:    
                #self.ListenerOnLog.emit([self.xID, self.xCam, self.xVideoFrameQLabel , str("ERR:: Unfortunately, Camera could not be loaded, trying to reconnect...")])
                sleep(5)
                pass

        cap.release()
        #cv2.destroyAllWindows()

class DetectBinaryThread(QThread):

    ListenerOnResult = pyqtSignal(str,str,str)
    ListenerOnLog = pyqtSignal(str)

    def __init__(self,img):
        super(DetectBinaryThread,self).__init__()
        self.img=img

    def run(self):
        try:
            fTime = dt.datetime.now().timestamp()
            print("\n***DetectBinaryThread***")
            print("Start detecting...")
            self.ListenerOnLog.emit("\n***DetectBinaryThread***")
            self.ListenerOnLog.emit("Start detecting...")

            nImageID = str(str(dt.datetime.now()).replace(':','-')+".jpeg")
            nImagePath = (_DO_DIR+nImageID)
            # TODO Save jpeg
            cv2.imwrite(nImagePath, self.img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            try:
                nJSON = detect_id(nImagePath, _IO._FACE_AI_ACCURACY, _IO._FACE_AI_CPUs , _FACE_AI_ID_FOLDER_DIR )
                #print("try :: ", nJSON)
                self.ListenerOnResult.emit(nJSON, nImagePath, nImageID)
            except:
                self.ListenerOnLog.emit("ERR:: An exception occurred")
                self.ListenerOnLog.emit("os.remove :: "+nImagePath)
                #os.remove(nImagePath)
                print("An exception occurred")
                print("os.remove :: "+nImagePath)
            #finally:
            #    self.ListenerOnLog.emit("finally:: os.remove :: "+nImagePath)
            #    os.remove(nImagePath)
            sTime = dt.datetime.now().timestamp()
            diff = sTime - fTime
            self.ListenerOnLog.emit("Time :: "+str(diff)+" s")
            print(diff) 
            self.ListenerOnLog.emit("End detect")
            return
        except:
            return
    
    def kill(self):
        self.quit()
        #self.wait()
        #self.terminate()

class ImportCSVThread(QThread):

    ListenerOnFinish = pyqtSignal(str)
    ListenerOnLog = pyqtSignal(str)

    def __init__(self,csvFile):
        super(ImportCSVThread,self).__init__()
        self.csvFile = csvFile

    def run(self):
        fTime = dt.datetime.now().timestamp()
        print("\n***ImportCSVThread***")
        self.ListenerOnLog.emit("Start Importing...")

        _Err = open(ROOT_DIR+'/csv.error.log', 'w')
        
        print('csvFile:: ', self.csvFile)
        with open(self.csvFile , 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            count = 1
            for row in csv_dict_reader:
                # path,name,details,gender,age,skinColor
                print('row:: ', row)
                try:
                    count += 1
                    #print("count", count)
                    self.ListenerOnLog.emit(str('Work in progress on line '+str(count)))
                    imageFile = row['path']
                    name = row['name']
                    details = row['details']
                    gender = row['gender']
                    age = row['age']
                    skinColor = row['skinColor']
                        
                    isWrongData = False
                    if imageFile is None or imageFile == '' or (not os.path.exists(imageFile)):
                        isWrongData = True
                        _Err.write(str(row)+'[invalid path]\n')
                
                    if name is None or name == '' or len(name) < 3:
                        isWrongData = True
                        _Err.write(str(row)+'[invalid name]\n')

                    if gender is not None and gender != '' and gender not in _IO.gender_list:
                        isWrongData = True
                        _Err.write(str(row)+'[invalid gender]\n')

                    if age is not None and age != '':
                        try:
                            age = int(age)
                        except:    
                            isWrongData = True
                            _Err.write(str(row)+'[invalid age]\n')

                    if not isWrongData:

                        userKey = secrets.token_hex(24)

                        nUser = User(userKey, '', str(name), str(details), str(gender), str(age), str(skinColor))


                        try:
                            isGenerated = generate_id(imageFile, userKey, _IO._FACE_AI_CPUs, _FACE_AI_ID_FOLDER_DIR)
                            print("isGenerated", isGenerated)

                            if isGenerated == True:
                                #isInsertUser = _IO_Mysql.insertUser(nUser)
                                isInsertUser = _IO_sqlite.insertUser(nUser)
                                print("isInsertUser", isInsertUser)
                                if isInsertUser:
                                    print('OK:: ',count , row)
                                    #print('imageFile:: ', imageFile)
                                    #print('name:: ', name)
                                    #print('gender:: ', gender)
                                    #print('details:: ', details)
                                    #print('age:: ', age)
                                    #print('skinColor:: ', skinColor)
                                    print("userKey", userKey)
                                    #print("Done")
                                else:
                                    del_id( userKey, _FACE_AI_ID_FOLDER_DIR)
                                    _Err.write(str(row)+'[adapt error (The system could not save the information in the database)]\n')
                            else:
                                _Err.write(str(row)+'[adapt error (The picture does not contain facial features)]\n')

                        except:
                            _Err.write(str(row) + '[adapt error (The picture does not contain facial features)]\n')

                except:
                    _Err.write(str(row)+'[wrong content]\n')
                    print('Err:: ', row)

        _Err.close()

        self.ListenerOnFinish.emit(str('Visit this file for more information '+ROOT_DIR+'/csv.error.log'))
        
        sTime = dt.datetime.now().timestamp()
        diff = sTime - fTime
        print(diff)
        #sys.exit()   

if __name__ == '__main__':
    app = QApplication(sys.argv)


    ## TODO Auto Screen Resize
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    _IO._width_Screen_Available = rect.width()
    _IO._height_Screen_Available = rect.height()
    print('Available: %d x %d' % (_IO._width_Screen_Available, _IO._height_Screen_Available))

    ex = App()
    sys.exit(app.exec_())
