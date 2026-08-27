"""Runtime configuration for the Eqra Face System.

Secrets and machine-specific values are read from environment variables so
they are never committed to source control. A project-level ``.env`` file can
be used during local development; see ``.env.example``.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    # Environment variables still work when python-dotenv is unavailable.
    pass


_FACE_AI_CPUs = int(os.getenv("EQRA_FACE_AI_CPUS", "1"))
_FACE_AI_ACCURACY = float(os.getenv("EQRA_FACE_AI_TOLERANCE", "0.7"))
_FACE_AI_DETECT_TIME = float(os.getenv("EQRA_FACE_AI_DETECT_TIME", "0.75"))

_USERNAME_IPCAM = os.getenv("EQRA_CAMERA_USERNAME", "")
_PASSWORD_IPCAM = os.getenv("EQRA_CAMERA_PASSWORD", "")
_IP_IPCAM = os.getenv("EQRA_CAMERA_IP", "")
_PORT_IPCAM = os.getenv("EQRA_CAMERA_PORT", "554")
_URL_CAPTURE_PICTURE_IPCAM = (
    f"http://{_IP_IPCAM}/ISAPI/Streaming/channels/1/picture"
    if _IP_IPCAM
    else ""
)

_SQL_HOST = os.getenv("EQRA_MYSQL_HOST", "127.0.0.1")
_SQL_PORT = os.getenv("EQRA_MYSQL_PORT", "3306")
_SQL_USER = os.getenv("EQRA_MYSQL_USER", "IPCam")
_SQL_PASS = os.getenv("EQRA_MYSQL_PASSWORD", "")
_SQL_DB_NAME = os.getenv("EQRA_MYSQL_DATABASE", "IPCam")
_SQL_MAX_LIMIT_SELECT = int(os.getenv("EQRA_SQL_PAGE_SIZE", "25"))

_SERIAL_PORT = os.getenv("EQRA_SERIAL_PORT", "")
_SERIAL_BAUD_RATE = int(os.getenv("EQRA_SERIAL_BAUD_RATE", "9600"))
_RELAY_AUTHORIZED_IDS = {
    user_id.strip()
    for user_id in os.getenv("EQRA_RELAY_AUTHORIZED_IDS", "").split(",")
    if user_id.strip()
}

_titale = "Eqra IP-Camera"
_allRightsReserved = "Eqra Tech Company. All rights reserved. Copyright © 2011-2022"
_addNewPerson = "Add New Person"
_liveCamera = "Live Camera"
_attendanceRecord = "Attendance Record"

_Cams = "IP Camera"
_camInfo = "Camera Info"
_IP = "IP"
_Port = "Port"
_Username = "Username"
_Password = "Password"
_Details = "Details"
_CreatedAt = "CreatedAt"

_deleteCam = "Delete Camera"
_deleteCamAsk = "Are you sure to delete camera"
_deleteCamSucc = "The system has been successfully delete this camera"
_deleteCamErr = "Unfortunately, the system was unable to delete this camera"

_addCam = "Add new Camera"
_ip_err = "Unfortunately, you did not type a correct IP"
_port_err = "Unfortunately, you did not type a correct Port"
_username_err = "Unfortunately, you did not type a correct Username"
_password_err = "Unfortunately, you did not type a correct Password"
_add_Came_DB_err = "Unfortunately, Duplicate Camera info"
_add_Came_DB_succ = "The system has been successfully add new Camera"

_updateCam = "Update Camera info"
_update_Cam_DB_err = "Unfortunately, Duplicate Camera info"
_update_Cam_DB_succ = "The system has been successfully update Camera info"



_search = "Search"
#_search_holderText = "Type user name , key , age , or gender (eg. Unknown)"
_search_holderText = "Type user name or key (eg. Unknown)"
_date_holderText = "click here to select date"
_userInfo = "User Info"

_adapt = "Adapt"
_log = "Log"
_save = "Save"
_update = "Update"
_add = "Add"
_delete = "Delete"
_clean = "Clean"
_deleteLog = "Delete Log"
_deleteLogAsk = "Are you sure to delete log"
_deleteLogSucc = "The system has been successfully delete this log"
_deleteLogErr = "Unfortunately, the system was unable to delete this log"
_selectImageFile = "Please choose a person's photo for the purpose of adding"
_adapt_succ = "The system has been successfully adapted on the new person"
_adapt_err = "Unfortunately, the addition process was not completed, use another image"
_insertAdapt_DB_err = "Unfortunately, Duplicate User info"
_img_err = "Unfortunately, you did not select the image"
_name_err = "Unfortunately, you did not type a correct name"
_age_err = "Unfortunately, you did not type a correct age"
_gender_err = "Unfortunately, you did not select the gender"

_unknown = "Unknown"
_imageType = "Image Type"
_imageFile = "Image File"
_imageFile_hint_msg = "Click here to select the image"
_name = "Name"
_details = "Details"
_gender = "Gender"
_age = "Age"
_skinColor = "Skin Color"

_import_csv_file = "Import CSV File"
_csv_file_header_note = "# csv header { \n\t 1. 'path' (String : Image Path jpeg ) , \n\t 2. 'name' (String : Full User Name at lesst three character ) , \n\t 3. 'details' (String : Optional ) , \n\t 4. 'gender' (String : Optional : select on of 'male','female','other') , \n\t 5. 'age' (Integer : Optional ) , \n\t 6. 'skinColor' (String : Optional ) }"
_csv_file = "CSV File"
_csv_file_hint_msg = "Click here to select the csv file"
_process = "Process"


# TODO init Values
imageType_list = ["jpeg", "jpg", "gif", "png", "bmp"]
gender_list = ["male", "female", "other"]

_width_Screen_Available = 1280
_height_Screen_Available = 720

_widthUIFrame = 1280
_heightUIFrame = 720

_widthCamFrame = 960
_heightCamFrame = 540
