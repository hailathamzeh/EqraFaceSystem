class User:
    
  def __init__(self, key, createdAt, name, details, gender, age, skinColor):
    self.key = key
    self.createdAt = createdAt
    self.name = name
    self.details = details
    self.gender = gender
    self.age = age
    self.skinColor = skinColor

  def setKey(self, key):
    self.key = key
  
  def getKey(self):
    return self.key
  
  def getCreatedAt(self):
    return self.createdAt
  
  def getName(self):
    return self.name
  
  def getDetails(self):
    return self.details
  
  def getGender(self):
    return self.gender

  def getAge(self):
    return self.age

  def getSkinColor(self):
    return self.skinColor

  def toString(self):
    return str("key : "+self.key+" , createdAt: "+str(self.createdAt)+" , name: "+str(self.name)+" , details: "+self.details+" , gender: "+self.gender+" , age: "+str(self.age)+" , skinColor: "+self.skinColor)
    #return str("key : "+self.key+" , createdAt: "+self.createdAt+" , name: "+self.name+" , details: "+self.details+" , gender: "+self.gender+" , age: "+self.age+" , skinColor: "+self.skinColor)

#p1 = User("", 36)
#p1.setKey() 