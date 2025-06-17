class Cam:
    
  def __init__(self, id, createdAt, ip, port, username, password, details):
    self.id = id
    self.createdAt = createdAt
    self.ip = ip
    self.port = port
    self.username = username
    self.password = password
    self.details = details

  def setId(self, id):
    self.id = id
  
  def getId(self):
    return self.id
  
  def getCreatedAt(self):
    return self.createdAt

  def setIp(self, ip):
    self.ip = ip

  def getIp(self):
    return self.ip
  
  def getPort(self):
    return self.port
  
  def getUsername(self):
    return self.username

  def getPassword(self):
    return self.password

  def getDetails(self):
    return self.details
 

  def toString(self):
    return str("id : "+str(self.id)+" , createdAt: "+str(self.createdAt)+" , ip: "+str(self.ip)+" , port: "+str(self.port)+" , username: "+str(self.username)+" , password: "+str(self.password)+" , details: "+str(self.details))
