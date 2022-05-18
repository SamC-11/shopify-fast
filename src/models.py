from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()



#LIST OF ITEMS THAT EXIST
class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable = False)

    #establishing relationship with Inventory
    children = relationship("Inventory",backref="items")


#LIST OF THE AMOUNT OF ITEMS IN YOUR INVENTORY
class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)

    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

    quantity = Column(Integer, default = 0, nullable = False)

    


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False, unique = True)

    #establishing relationship with Inventory
    children = relationship("Inventory",backref="warehouses")
    

    



