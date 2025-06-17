import _IO
import string
from _User import User
from _AttendanceRecord import AttendanceRecord

import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(host=_IO._SQL_HOST, port=_IO._SQL_PORT, user=_IO._SQL_USER, password=_IO._SQL_PASS, database=_IO._SQL_DB_NAME)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
#else:
#  cnx.close()

## TODO Users Table
def insertUser(nUser):
    nCursor = cnx.cursor(buffered=True)
    
    sql = "INSERT INTO `users` (`users`.`key`, `users`.`name`, `users`.`details`, `users`.`gender`, `users`.`age`, `users`.`skinColor`) VALUES (%s, %s, %s, %s, %s, %s);"
   
    #val = [
    #(key, name, details, gender, age, skinColor),
    #('d', 'd'),
    #]
    #nCursor.executemany(sql, val)

    gender = nUser.getGender()
    if gender is None or gender == '' or gender not in _IO.gender_list:
      gender = _IO.gender_list[2]
    
    age = nUser.getAge()
    if age is None or age == '':
      age = 1
    try:
      age = int(age)
    except:
      age = 1

    val = (nUser.getKey(), str(nUser.getName()), nUser.getDetails(), gender, str(age), nUser.getSkinColor())
    try:
      nCursor.execute(sql, val)
      cnx.commit()
      #print(nCursor.rowcount, "was inserted.")
      return True
    except mysql.connector.Error as e:
      print("Error inserting data from MySQL table", e)
      return False
    except:
      print("Error inserting data from MySQL table")
      return False

def getUserInfo(key):
    nCursor = cnx.cursor(buffered=True)
    
    sql = "SELECT `users`.`key`, `users`.`createdAt`, `users`.`name`, `users`.`details`, `users`.`gender`, `users`.`age`, `users`.`skinColor` FROM `users` WHERE `users`.`key` = '"+key+"' LIMIT 0, 1;"
    #print(sql)

    try:
      nCursor.execute(sql)
      cnx.commit()
      

      row = nCursor.fetchone()
      if row:
        #print(row)
        nUser = User(row[0], str(row[1]), row[2], row[3], row[4], int(row[5]), row[6])
        #print('toString',nUser.toString())
        return nUser
      else:
        return False
        
      #ROWs = nCursor.fetchall()
      #for row in ROWs:
      #  print("row",row)
     
    except mysql.connector.Error as e:
      #print("Error reading data from MySQL table", e)
      return False
    except:
      return False


## TODO Logs Table
def insertLog(key, name, path):
    nCursor = cnx.cursor(buffered=True)
    
    sql = "INSERT INTO `logs` (`logs`.`key`, `logs`.`name`, `logs`.`path`) VALUES (%s, %s, %s);"
    
    val = (str(key), str(name), str(path))
    try:
      nCursor.execute(sql, val)
      cnx.commit()
      #print(nCursor.rowcount, "was inserted.")
      return True
    except mysql.connector.Error as e:
      #print("Error inserting data from MySQL table", e)
      return False
    except:
      #print("Error inserting data from MySQL table")
      return False

def isUserLogged_before_5_minutes(key):
    nCursor = cnx.cursor(buffered=True)
    
    sql = "SELECT * FROM `logs` WHERE `logs`.`key` = '"+key+"' AND (`logs`.`createdAt` BETWEEN (NOW() - INTERVAL 5 MINUTE) AND NOW()) LIMIT 0, 1;"

    try:
      nCursor.execute(sql)
      cnx.commit()
      
      row = nCursor.fetchone()
      if row:
        #print(row)
        return True
      else:
        print("Error reading data from MySQL table")
        return False

    except mysql.connector.Error as e:
      print("Error reading data from MySQL table", e)
      return False
    except:
      print("Error reading data from MySQL table")
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

    nCursor = cnx.cursor(buffered=True)
    
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

    except mysql.connector.Error as e:
      print("Error reading data from MySQL table", e)
      return False
    except:
      print("Error reading data from MySQL table")
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

    nCursor = cnx.cursor(buffered=True)
    
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
      nCursor.execute(sql)
      cnx.commit()
      
      row = nCursor.fetchone()
      if row:
        return row[0]
      else:
        return 0

    except mysql.connector.Error as e:
      print("Error reading data from MySQL table", e)
      return 0
    except:
      print("Error reading data from MySQL table")
      return 0

def deleteLog(cId, cKey, cName):
    
    nCursor = cnx.cursor(buffered=True)
    
    sql = "DELETE FROM `logs` "
    sql += " WHERE"
    sql += " `logs`.`id` = "+str(cId)+""
    sql += " AND `logs`.`key` = %s"
    sql += " AND `logs`.`name` = %s"
    print(' sql: '+sql)

    val = (str(cKey), str(cName))

    try:
      nCursor.execute(sql, val)
      cnx.commit()
      return nCursor.rowcount > 0
    except mysql.connector.Error as e:
      print("Error Delete data from MySQL table", e)
      return False
    except:
      print("Error Delete data from MySQL table")
      return False

def updateLog(cId, cKey, cName, imageFile):
    
    nCursor = cnx.cursor(buffered=True)
    
    sql = "UPDATE `logs` as l"
    sql += " SET"
    sql += " l.`key` = %s"
    sql += " , l.`name` =  %s"
    sql += " , l.`path` = %s"
    sql += " WHERE"
    sql += " l.`id` = "+str(cId)
    print(' sql: '+sql)

    val = (str(cKey), str(cName), str(imageFile))

    try:
      nCursor.execute(sql, val)
      cnx.commit()
      return nCursor.rowcount > 0
    except mysql.connector.Error as e:
      print("Error update data from MySQL table", e)
      return False
    except:
      print("Error update data from MySQL table")
      return False

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