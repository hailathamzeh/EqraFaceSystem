import os
import _IO
from _User import User
from _AttendanceRecord import AttendanceRecord
from _Cam import Cam

import sqlite3
from sqlite3 import Error

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print("ROOT_DIR",ROOT_DIR)

_DB_NAME = 'config/IPCam.db'
_DB_DIR = ROOT_DIR+os.sep+_DB_NAME

cnx = None
try:
  cnx = sqlite3.connect(_DB_DIR, check_same_thread=False)
  print(sqlite3.version)
  # TODO Create users Table
  sql_Users_table = """
  CREATE TABLE IF NOT EXISTS `users` (
  `key` TEXT PRIMARY KEY,
  `createdAt` TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  `name` TEXT NOT NULL,
  `details` TEXT,
  `gender` TEXT CHECK( gender IN ('male','female','other') ) NOT NULL DEFAULT 'other',
  `age` INTEGER,
  `skinColor`TEXT
  );
  """

  sql_Logs_table = """
  CREATE TABLE IF NOT EXISTS `logs` (
  `id` INTEGER PRIMARY KEY,
  `key` TEXT NOT NULL,
  `createdAt` TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  `name` TEXT NOT NULL,
  `path` TEXT NOT NULL
  );
  """      

  sql_Cams_table = """
  CREATE TABLE IF NOT EXISTS `cams` (
  `id` INTEGER PRIMARY KEY,
  `details` TEXT,
  `createdAt` TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  `ip` TEXT NOT NULL,
  `port` INTEGER NOT NULL,
  `username` TEXT NOT NULL,
  `password` TEXT NOT NULL
  );
  """ 

  if cnx is not None:
    try:
      nCursor = cnx.cursor()
      
      try:
        nCursor.execute(sql_Users_table)
        cnx.commit()
      except Error as e:
        print(e)

      try:
        nCursor.execute(sql_Logs_table)
        cnx.commit()
      except Error as e:
        print(e)

      try:
        nCursor.execute(sql_Cams_table)
        cnx.commit()
      except Error as e:
        print(e)  

      #try:
      #  nCursor.execute("CREATE INDEX logs_key_index ON `logs` (key);")
      #  cnx.commit()
      #except Error as e:
      #  print(e)

      #try:
      #  nCursor.execute("CREATE INDEX logs_name_index ON `logs` (name);")
      #  cnx.commit()
      #except Error as e:
      #  print(e)

      try:
        nCursor.execute("PRAGMA auto_vacuum = FULL;")
        cnx.commit()
      except Error as e:
        print(e)
      
      try:
        nCursor.execute("PRAGMA main.auto_vacuum = 1;")
        cnx.commit()
      except Error as e:
        print(e)  
      
    except Error as e:
      print(e)
  else:
    print("Error! cannot create the database connection.")
except Error as e:
  print(e)
except:
  print("Error! cannot create the database connection.")

## TODO Users Table
def insertUser(nUser):

  key = nUser.getKey()
  name = nUser.getName()
  details = nUser.getDetails()
  gender = nUser.getGender()
  age = nUser.getAge()
  skinColor = nUser.getSkinColor()

  try:
    if (gender is None) or (gender == '') or (gender not in _IO.gender_list):
      gender = _IO.gender_list[2]
  except:
    gender = _IO.gender_list[2]

  try:
    if age is None or age == '':
      age = 1
    try:
      age = int(age)
    except:
      age = 1
  except:
    age = 1

  #print('--gender', gender)
  #print('--age', str(age))

  sql = "INSERT INTO `users` (`key`, `name`, `details`, `gender`, `age`, `skinColor`) VALUES (?, ?, ?, ?, ?, ?);"
  val = ( key, str(name), str(details), str(gender), str(age), str(skinColor))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    #print(nCursor.rowcount, "was inserted.")
    return True
  except Error as e:
    print("Error inserting data from SQLITE table", e)
    return False
  except:
    print("Error inserting data from SQLITE table")
    return False

def getUserInfo(key):
  
  sql = "SELECT `key`, `createdAt`, `name`, `details`, `gender`, `age`, `skinColor` FROM `users` WHERE `key` = ? LIMIT 0, 1;"
  val = (str(key),)

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    

    row = nCursor.fetchone()
    if row:
      #print(row)
      nUser = User(row[0], str(row[1]), row[2], row[3], row[4], int(row[5]), row[6])
      #print('toString',nUser.toString())
      return nUser
    else:
      print("Error reading data from SQLITE table")
      return False
      
    #ROWs = nCursor.fetchall()
    #for row in ROWs:
    #  print("row",row)
    
  except Error as e:
    print("Error reading data from SQLITE table", e)
    return False
  except:
    print("Error reading data from SQLITE table")
    return False

## TODO Logs Table
def insertLog(key, name, path):
 
  sql = "INSERT INTO `logs` (`key`, `name`, `path`) VALUES (?, ?, ?);"
  val = (str(key), str(name), str(path))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    #print(nCursor.rowcount, "was inserted.")
    return True
  except Error as e:
    print("Error inserting data from SQLITE table", e)
    return False
  except:
    print("Error inserting data from SQLITE table")
    return False

def isUserLogged_before_5_minutes(key):
  
  #sql = "SELECT * FROM `logs` WHERE `key` = ? AND ( `createdAt` > (datetime('now','localtime','-24 hour')) ) LIMIT 0, 1;"
  #sql = "SELECT * FROM `logs` WHERE `key` = ? AND ( `createdAt` > (datetime('now','localtime','-1 minutes')) ) LIMIT 0, 1;"
  sql = "SELECT * FROM `logs` WHERE `key` = ? AND ( `createdAt` > (datetime('now','localtime','-0.5 seconds')) ) LIMIT 0, 1;"
  val = (str(key),)

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    
    row = nCursor.fetchone()
    if row:
      print(row)
      return True
    else:
      #print("Error reading data from SQLITE table")
      return False

  except Error as e:
    print("Error reading data from SQLITE table", e)
    return False
  except:
    print("Error reading data from SQLITE table")
    return False

def getLogs(cSearchText, cDate, cSkip):
  print('-- getLogs == cSearchText: '+str(cSearchText)+"  , cDate: "+str(cDate)+"  , cSkip: "+str(cSkip))

  sDate = None
  eDate = None
  if cDate is not None:
    sDate = cDate + " 00:00:00"
    eDate = cDate + " 23:59:59"
    #print(' sDate: '+sDate+"  , eDate: "+ eDate)

  nQuery = ''

  if cSearchText and cSearchText is not None:
    if nQuery == '':
      nQuery += " WHERE"

    nQuery += " (l.`key` LIKE '%"+cSearchText+"%'"
    nQuery += " OR l.`name` LIKE '%"+cSearchText+"%')"

  if cDate and cDate is not None:
    if nQuery == '':
      nQuery += " WHERE"
    else:
      nQuery += " AND "

    nQuery+= " l.`createdAt` BETWEEN '"+sDate+"' AND '"+eDate+"'"

  sql = "SELECT l.`id`, l.`key`, l.`createdAt`, l.`name`, l.`path`, u.`details`, u.`gender`, u.`age`, u.`skinColor`"
  sql += " FROM `logs` as l"
  sql += " LEFT JOIN `users` as u ON (l.`key` = u.`key`)"
  sql += "  OR (l.`key` = '' AND u.`key` IS NULL)"
  sql += "  OR (l.`key` = 'Unknown' AND u.`key` IS NULL)"
  sql += "  OR (l.`key` = 'unknown' AND u.`key` IS NULL)"
  sql += nQuery
  sql += " ORDER BY l.`createdAt` DESC"
  sql += " LIMIT " + str(_IO._SQL_MAX_LIMIT_SELECT)
  sql += " OFFSET " + str(cSkip)
  sql += ";"
  #print(' sql: '+sql)
  #sql = "AND (`createdAt` BETWEEN (NOW() - INTERVAL 5 MINUTE) AND NOW())"

  try:
    logs = []
    nCursor = cnx.cursor()
    nCursor.execute(sql)
    cnx.commit()
    
    ROWs = nCursor.fetchall()
    for row in ROWs:
      #print("row",row)
      #print("row[5]",row[3])
      #print("row[5]",bool(row[3] and row[3].strip()))
      #print("row[7]",bool(row[7] is None))

      details = (('',row[5])[bool(row[5] is not None)])
      gender = (('',row[6])[bool(row[6] is not None)])
      age = (('',row[7])[bool(row[7] is not None and isinstance(row[7], int))])
      skinColor = (('',row[8])[bool(row[8] is not None)])

      #print("isinstance age",(row[7] and isinstance(row[7], int)))
      #print("age",((False,True)[row[7] is not None and isinstance(row[7], int)]))
      #print("age",str(age))
      
      aRecord = AttendanceRecord(int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), details, gender, skinColor, age)
      #aRecord = AttendanceRecord(int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), int(row[7]), str(row[8]))
      #print('toString',aRecord.toString())
      logs.append(aRecord)
      #return nUser
      #print("row",row)

    return logs

  except Error as e:
    print("Error reading data from SQLITE table", e)
    return False
  except:
    print("Error reading data from SQLITE table")
    return False

def getLogsCount(cSearchText, cDate):
  print('-- getLogsCount == cSearchText: '+str(cSearchText)+"  , cDate: "+str(cDate))

  sDate = None
  eDate = None
  if cDate is not None:
    sDate = cDate + " 00:00:00"
    eDate = cDate + " 23:59:59"
    #print(' sDate: '+sDate+"  , eDate: "+ eDate)

  nQuery = ''

  if cSearchText and cSearchText is not None:
    if nQuery == '':
      nQuery += " WHERE"

    nQuery += " (l.`key` LIKE '%"+cSearchText+"%'"
    nQuery += " OR l.`name` LIKE '%"+cSearchText+"%')"

  if cDate and cDate is not None:
    if nQuery == '':
      nQuery += " WHERE"
    else:
      nQuery += " AND "

    nQuery+= " l.`createdAt` BETWEEN '"+sDate+"' AND '"+eDate+"'"
 
  sql = "SELECT COUNT(*) as c"
  sql += " FROM `logs` as l"
  sql += " LEFT JOIN `users` as u ON (l.`key` = u.`key`)"
  sql += "  OR (l.`key` = '' AND u.`key` IS NULL)"
  sql += "  OR (l.`key` = 'Unknown' AND u.`key` IS NULL)"
  sql += "  OR (l.`key` = 'unknown' AND u.`key` IS NULL)"
  sql += nQuery
  sql += " ORDER BY l.`createdAt` DESC"
  #print(' sql: '+sql)

  sql += ";"
  #sql = "AND (`createdAt` BETWEEN (NOW() - INTERVAL 5 MINUTE) AND NOW())"

  try:
    logs = []
    nCursor = cnx.cursor()
    nCursor.execute(sql)
    cnx.commit()
    
    row = nCursor.fetchone()
    if row:
      return row[0]
    else:
      print("Error reading data from SQLITE table")
      return 0

  except Error as e:
    print("Error reading data from SQLITE table", e)
    return 0
  except:
    print("Error reading data from SQLITE table")
    return 0

def deleteLog(cId, cKey, cName):   
 
  sql = "DELETE FROM `logs`"
  sql += " WHERE"
  sql += " `id` = "+str(cId)+""
  sql += " AND `key` = ?"
  sql += " AND `name` = ?"
  print(' sql: '+sql)

  val = (str(cKey), str(cName))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    return nCursor.rowcount > 0
  except Error as e:
    print("Error Delete data from SQLITE table", e)
    return False
  except:
    print("Error Delete data from SQLITE table")
    return False

def updateLog(cId, cKey, cName, imageFile):
    
  sql = "UPDATE `logs` "
  sql += " SET"
  sql += " `key` = ?"
  sql += " , `name` =  ?"
  sql += " , `path` = ?"
  sql += " WHERE"
  sql += " `id` = "+str(cId)
  print(' sql: '+sql)

  val = (str(cKey), str(cName), str(imageFile))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    return nCursor.rowcount > 0
  except Error as e:
    print("Error update data from SQLITE table", e)
    return False
  except:
    print("Error update data from SQLITE table")
    return False


## TODO Cams Table
def insertCam(nCam):

  if nCam is None:
    return False
 
  sql = "INSERT INTO `cams` (`ip`, `port`, `username`, `password`, `details`) VALUES (?, ?, ?, ?, ?);"
  val = (str(nCam.getIp()), str(nCam.getPort()), str(nCam.getUsername()), str(nCam.getPassword()), str(nCam.getDetails()))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    #print(nCursor.rowcount, "was inserted.")
    return True
  except Error as e:
    print("Error inserting data from SQLITE table", e)
    return False
  except:
    print("Error inserting data from SQLITE table")
    return False

def deleteCam(nCam):   

  if nCam is None:
    return False

  sql = "DELETE FROM `cams`"
  sql += " WHERE"
  sql += " `id` = "+str(nCam.getId())+""
  sql += " AND `ip` = ?"
  sql += " AND `port` = ?"
  print(' sql: '+sql)

  val = (str(nCam.getIp()), str(nCam.getPort()))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    return nCursor.rowcount > 0
  except Error as e:
    print("Error Delete data from SQLITE table", e)
    return False
  except:
    print("Error Delete data from SQLITE table")
    return False

def updateCam(nCam):

  if nCam is None:
    return False

  sql = "UPDATE `cams` "
  sql += " SET"
  sql += " `ip` = ?"
  sql += " , `port` =  ?"
  sql += " , `username` = ?"
  sql += " , `password` = ?"
  sql += " , `details` = ?"
  sql += " WHERE"
  sql += " `id` = "+str(nCam.getId())
  print(' sql: '+sql)

  val = (str(nCam.getIp()), int(nCam.getPort()), str(nCam.getUsername()), str(nCam.getPassword()), str(nCam.getDetails()))

  try:
    nCursor = cnx.cursor()
    nCursor.execute(sql, val)
    cnx.commit()
    return nCursor.rowcount > 0
  except Error as e:
    print("Error update data from SQLITE table", e)
    return False
  except:
    print("Error update data from SQLITE table")
    return False

def getCams():
  
  sql = "SELECT `id`, `createdAt`, `ip`, `port`, `username`, `password`, `details` FROM `cams` ORDER BY `createdAt` DESC;"
  
  try:
    cams = []
    nCursor = cnx.cursor()
    nCursor.execute(sql)
    cnx.commit()
    
    ROWs = nCursor.fetchall()
    for row in ROWs:
      #print("row",row)
      #row (1, '2022-09-22 13:25:56', '192.168.1.22', 554, 'admin', 'abcd1234', 'entrance')
  
      details = (('',row[6])[bool(row[6] is not None)])
      
      aRecord = Cam(int(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]), str(row[5]), details)
      #print('toString',aRecord.toString())
      cams.append(aRecord)
      
    return cams

  except Error as e:
    print("Error reading data from SQLITE table", e)
    return False
  except:
    print("Error reading data from SQLITE table")
    return False


## TODO Test Query
#nUser = User('81f87451da71ca69e8c226b61d9e3d942dc2a8e5335c365b', '', 'FaisalObeid', '', 'Male', 30, 'Black')
nUser = User('81f87451da71ca69e8c226b61d9e3d942dc2a8e5335c365b', '', '', '', '', '', '')

#print('insertUser', insertUser(nUser))
#print('insertUser', insertUser(nUser))

#print('getUserInfo', getUserInfo(nUser.getKey()))

#print('insertLog', insertLog(nUser.getKey(), nUser.getName(), "/home/fobeid/fobeid/Code-Python/HikVision-IP-Camera-UI-Python/Known/2022-09-11 15-28-48.848529.jpeg"))

#print('isUserLogged_before_5_minutes', str(isUserLogged_before_5_minutes(nUser.getKey())))

#print('getLogsCount', getLogsCount(None, None))
#print('getLogsCount', getLogsCount('Faisal', '2022-09-18'))
#print('getLogs', getLogs(None, None, 0))
#print('getLogs', getLogs('Faisal', '2022-09-18', 0))

#print('updateLog', updateLog(1,nUser.getKey(),"Faisal","/home/fobeid/fobeid/Code-Python/HikVision-IP-Camera-UI-Python/Unknown/2022-09-11 15-28-48.848529.jpeg"))
#print('deleteLog', deleteLog(2,nUser.getKey(),nUser.getName()))


nCam = Cam(1, None, '192.168.1.22', '554', 'admin', 'abcd1234', 'entrance')

#print('insertCam', insertCam(nCam))
#nCam.setIp('192.168.1.23')
#print('updateCam', updateCam(nCam))
#nCam.setId(2)
#print('deleteCam', deleteCam(nCam))
#print('getCams', getCams())
