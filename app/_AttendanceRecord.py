class AttendanceRecord:
    
  def __init__(self, id, key, createdAt, name, path, details, gender, skinColor, age):
    self.id = id
    self.key = key
    self.createdAt = createdAt
    self.name = name
    self.path = path
    self.details = details
    self.gender = gender
    self.skinColor = skinColor
    self.age = age
  
  def getId(self):
    return self.id

  def setKey(self, key):
    self.key = key

  def getKey(self):
    return self.key
  
  def getCreatedAt(self):
    return self.createdAt
  
  def setName(self, name):
    self.name = name

  def getName(self):
    return self.name

  def getPath(self):
    return self.path

  def getDetails(self):
    return self.details
  
  def getGender(self):
    return self.gender

  def getSkinColor(self):
    return self.skinColor

  def getAge(self):
    return self.age

  def toString(self):
    return str("id : "+str(self.id)+" , key : "+self.key+" , createdAt: "+str(self.createdAt)+" , name: "+str(self.name)+" , path: "+self.path+" , details: "+self.details+" , gender: "+self.gender+" , skinColor: "+self.skinColor+" , age: "+str(self.age))
