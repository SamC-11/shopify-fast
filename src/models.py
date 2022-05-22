from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()


#LIST OF THE AMOUNT OF ITEMS IN YOUR INVENTORY AND THE WAREHOUSE THEY ARE STORED IN
class Inventory(Base):
    __tablename__ = "Inventory"
    
    id = Column(Integer, primary_key=True)

    warehouse_id = Column("warehouse_id", Integer, ForeignKey('Warehouse.id'))
    item_id = Column("item_id", Integer, ForeignKey('Item.id'))

    quantity = Column(Integer, default = 0, nullable = False)

#LIST OF ITEMS THAT EXIST
class Item(Base):
    __tablename__ = "Item"
    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable = False)

    warehouses = relationship('Warehouse', secondary=Inventory.__table__, backref='Item')


    


class Warehouse(Base):
    __tablename__ = "Warehouse"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False, unique = True)

    items = relationship('Item', secondary=Inventory.__table__, backref='Warehouse')

    

    



