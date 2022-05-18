from sqlalchemy import Column, Integer, String
from database import Base

class Inventory(Base):
    __tablename__ = "Inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer, default = 0, nullable = False)


#Trying this out later, class for individual item for decoupling purposes
#ID IS PKEY AND ID IN ITEMS WILL BE FKEY IF I DECIDE TO IMPLEMENT THIS
class Items(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)