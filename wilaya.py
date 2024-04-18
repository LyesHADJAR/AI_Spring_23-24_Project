# Class wilaya for Introduction to AI Project

class wilaya:
  def __init__(self, name = '', code = 0, totalArea = 0, totalAgriculturalArea = 0, usedAgriculturalArea =  0, prodectsList = []):
    self.name = name
    self.code = code
    self.totalArea = totalArea
    self.totalAgriculturalArea = totalAgriculturalArea
    self.usedAgriculturalArea = usedAgriculturalArea
    self.profucts = prodectsList
    
    
  def __str__(self):
    return f"{self.name} ({self.code})"
  
  def getName(self):
    return self.name
  
  def getCode(self):
    return self.code
  
  def getAgriculturalArea(self):
    return self.totalAgriculturalArea
  
  def getAgriAreaUsed(self):
    return self.usedAgriculturalArea
  
  def getAgriAreaUnused(self):
    return self.totalAgriculturalArea - self.usedAgriculturalArea
  
  def getProducts(self):
    return self.profucts
  
  def addProduct(self, prd):
    self.profucts.append(prd)
    
  def dropProduct(self, prd):
    self.profucts.remove(prd)
  
  
