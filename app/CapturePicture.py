import os
import requests
from requests.auth import HTTPBasicAuth
import shutil
import datetime as dt
import _IO
import _IO_sqlite


## TODO Settings
##   Network >> adv. >>  Integration Protocol
# 1. Enable Hikvision - CGI
# 2. Hikvision-CGI Authentication :: digest/basic
# 3. Enable Open Network Video Interface
## TODO go to EqraTech-IPCam/config/Cam_settings
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

_OUTPUT_FOLDER_NAME = '_Output'
_CAM_FOLDER_NAME = _OUTPUT_FOLDER_NAME+os.sep+'_Cam'
_CAM_DIR = ROOT_DIR+os.sep+_CAM_FOLDER_NAME+os.sep
os.makedirs(_CAM_DIR, exist_ok=True)

def getPhoto():
  try:
    
    LiveCams_Models = _IO_sqlite.getCams()
    LiveCam_Model = None
    if LiveCams_Models is not None and len(LiveCams_Models) > 0:
      LiveCam_Model = LiveCams_Models[0]

    if LiveCam_Model is None:
      return None
    nImageID = str(str(dt.datetime.now()).replace(':','-')+".jpeg")
    nImagePath = (_CAM_DIR+nImageID)
    r = requests.get(
      str("http://"+LiveCam_Model.getIp()+"/ISAPI/Streaming/channels/1/picture"),
      auth=HTTPBasicAuth(LiveCam_Model.getUsername(), LiveCam_Model.getPassword()),
      stream=True,
      timeout=15,
    )
    print(str(r.status_code))
    if r.status_code == 200:
      with open(nImagePath, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        return nImagePath
        
  except:
    return None
  
  return None
