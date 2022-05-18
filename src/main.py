from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models



app = FastAPI()

#creates db and table if it doesn't already exist
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Item(BaseModel):
    id: int = Field(gt=-1)
    name: str = Field(min_length=1)
    quantity: int = Field(gt=-1)




@app.get("/inventory")
def inventory(db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    return db.query(models.Inventory).all()


@app.post("/")
def add_item(item: Item, db:Session = Depends(get_db)):
    

    #CHECK IF ITEM ALREADY EXISTS 
    item_model = db.query(models.Items).filter(models.Items.id == item.id).first()
    inventory_item_model = models.Inventory()

    if item_model is None:
        #create new item
        item_model = models.Items()
        item_model.name = item.name

        #add item to inventory
        inventory_item_model = models.Inventory()
        inventory_item_model.warehouse_id = 5
        inventory_item_model.item_id = item.id
        inventory_item_model.quantity = item.quantity
        
    
    db.add(item_model)
    db.add(inventory_item_model)
    db.commit()

    return item


@app.put('/{item_id}')
def update_inventory(item_id: int, newItem: Item, db:Session = Depends(get_db)):

    item_model = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )

    item_model.quantity = newItem.quantity
    item_model.name = newItem.name

    db.add(item_model)
    db.commit()

    return newItem


@app.delete('/{item_id}')
def delete_item(item_id: int, db:Session = Depends(get_db)):
    
    item_model = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )
        
    db.query(models.Inventory).filter(models.Inventory.id == item_id).delete()
    db.commit()