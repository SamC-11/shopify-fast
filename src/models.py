from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()

#Trying this out later, class for items. NOT the same as inventory for decoupling purposes
#ID IS PKEY AND ID IN ITEMS WILL BE FKEY IF I DECIDE TO IMPLEMENT THIS
class Items(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, index=True) 
    name = Column(String, nullable = False, unique = True)
    children = relationship("Inventory")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)

    item_id = Column(Integer, ForeignKey(Items.__table__.c['id']))


    quantity = Column(Integer, default = 0, nullable = False)


