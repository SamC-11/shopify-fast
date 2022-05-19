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

#This class is to add new items
class Item(BaseModel):
    id: int = Field(gt=-1)
    name: str = Field(min_length=1)
    


#This class is the object used to add inventory entries
class Inventory(BaseModel):
    item_id: int = Field(gt=-1)
    warehouse_id: int = Field(gt=-1)
    quantity: int = Field(gt=-1)


#This class is the object used to add warehouse(s)
class Warehouse(BaseModel):
    id: int = Field(gt=-1)
    name: str = Field(min_length=1)



# --------------------------------- WAREHOUSE ENDPOINT(S) -----------------------------------------------


@app.get("/warehouses", summary="Return a list of all existing warehouses as a JSON", tags=["Routes"])
def warehouses(db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    return db.query(models.Warehouse).all()

@app.get("/warehouses/specific", summary="Return a specific warehouse given the id",tags=["Routes"])
def warehouses(warehouse_id:int,db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse_id} does not exist"
        )
    
    return warehouse_model


@app.post("/warehouses/new", summary="Create a new warehouse object given a JSON input",tags=["Routes"])
def new_warehouse(warehouse: Warehouse, db:Session = Depends(get_db)):
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse.id).first()
    if warehouse_model is None:
        warehouse_model = models.Warehouse()
        warehouse_model.id = warehouse.id
        warehouse_model.name = warehouse.name
        db.add(warehouse_model)
        db.commit()
    else:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse.id} already exist"
        )
    
    return warehouse_model


@app.put('/warehouses/edit', summary="Edit an existing warehouse given the id and a new name",tags=["Routes"])
def edit_warehouse(warehouse_id: int, new_name: str, db: Session = Depends(get_db)):
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {warehouse_id} does not exist"
        )

    db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).update({'name':new_name})
    db.commit()

    return new_name



@app.delete('/warehouses/delete', summary="Delete an existing warehouse",tags=["Routes"])
def delete_item(warehouse_id: int, db:Session = Depends(get_db)):
    
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id ==warehouse_id).first()
 
    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse_id} does not exist"
        )
        
    db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).delete()
    db.query(models.Inventory).filter(models.Inventory.warehouse_id == warehouse_id).delete()
    db.commit()

    return f"Warehouse with ID {warehouse_id} deleted"



# --------------------------------- ITEM ENDPOINT(S) -----------------------------------------------

@app.get("/items", summary="Return a list of all existing items",tags=["Routes"])
def items(db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    return db.query(models.Items).all()


@app.get("/items/specific", summary="Return a specific item given the id",tags=["Routes"])
def items(item_id: int, db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()
    
    if item_model is None:
        raise HTTPException(
                status_code = 404,
                detail = f"Item with ID {item_id} does not exist"
        )
    
    return item_model


@app.post("/items/new", summary="Create a new item object given a JSON input",tags=["Routes"])
def new_item(item: Item, db:Session = Depends(get_db)):

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    item_model = db.query(models.Items).filter(models.Items.id == item.id).first()

    if item_model is None:
        #create new Item
        item_model = models.Items()
        item_model.id = item.id
        item_model.name = item.name

        db.add(item_model)
        db.commit()

    return item


@app.put('/items/edit', summary="Edit an existing item given the id and a new name",tags=["Routes"])
def edit_item(item_id: int, new_name: str, db: Session = Depends(get_db)):
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )

    db.query(models.Items).filter(models.Items.id == item_id).update({'name':new_name})
    db.commit()

    return new_name

    
    


@app.delete('/items/delete', summary="Delete an existing warehouse given the id",tags=["Routes"])
def delete_item(item_id: int, db:Session = Depends(get_db)):
    
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()
 
    if item_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )
        
    db.query(models.Items).filter(models.Items.id == item_id).delete()
    db.query(models.Inventory).filter(models.Inventory.item_id == item_id).delete()
    db.commit()

    return f"Item with ID {item_id} deleted"









# --------------------------------- INVENTORY ENDPOINT(S) -----------------------------------------------
@app.get("/inventory", summary="Return a list of all existing inventory entries",tags=["Routes"])
def inventory(db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    return db.query(models.Inventory).all()

@app.get("/inventory/specific", summary="Return a specific item given the id",tags=["Routes"])
def inventory(item_id: int, warehouse_id: int,db: Session = Depends(get_db)): #Depends handles dependency injections for db session
    inventory_model = db.query(models.Inventory).filter(models.Inventory.item_id == item_id).filter(models.Inventory.warehouse_id == warehouse_id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )
    
    return inventory_model
   

@app.post("/inventory/new", summary="Create a new inventory entry given a JSON objec", 
                            description="If an entry with an identical item_id and warehouse_id exists, the quantity of this new object will be added to the existing one",
                            tags=["Routes"])
def inventory_entry(item_id: int, warehouse_id:int, quantity:int, db:Session = Depends(get_db)):

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()

    if item_model is None:
       raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse_id} does not exist"
        )

    #create inventory entry object
    inventory_model = models.Inventory()
    inventory_model.item_id = item_id
    inventory_model.quantity = quantity
    inventory_model.warehouse_id = warehouse_id

    #if the item already exists at that warehouse, then add the quantities
    existing_item_quantity = db.query(models.Inventory.quantity).filter(models.Inventory.item_id == item_id).filter(models.Inventory.warehouse_id == warehouse_id).first()

    if existing_item_quantity is not None:
        inventory_model.quantity += existing_item_quantity[0]
        db.query(models.Inventory).filter(models.Inventory.item_id == item_id).filter(models.Inventory.warehouse_id == warehouse_id).delete()

    db.add(inventory_model)
    db.commit()

    return inventory_model



@app.put('/inventory/edit', summary="Edit an inventory entry given the id, warehouse_id, and quantity ",tags=["Routes"])
def edit_inventory(item_id: int, warehouse_id: int, quantity: int, id:int, db:Session = Depends(get_db)):

    #does item to change exist in this warehouse
    inventory_model = db.query(models.Inventory).filter(models.Inventory.id == id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Inventory entry with ID {item_id} does not exist"
        )

    db.query(models.Items).filter(models.Items.id == item_id).update({'warehouse_id':warehouse_id})
    db.query(models.Items).filter(models.Items.id == item_id).update({'item_id':item_id})
    db.query(models.Items).filter(models.Items.id == item_id).update({'quantity':quantity})


    db.commit()

    return inventory_model

@app.delete('/inventory/delete', summary="Deletes an inventory entry given the id",tags=["Routes"])
def delete_inventory_item(id:int, db:Session = Depends(get_db)):
    
    inventory_model = db.query(models.Inventory).filter(models.Inventory.id == id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Inventory entry with ID {id} does not exist"
        )
        
    db.query(models.Inventory).filter(models.Inventory.id == id).delete()
    db.commit()

    return f"Inventory Entry with ID {id} deleted"

