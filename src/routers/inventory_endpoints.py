from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import sys
sys.path.append('..')
from src import database, models, helper_objects



router = APIRouter()





# --------------------------------- INVENTORY ENDPOINT(S) -----------------------------------------------
@router.get("/inventory", summary="Return a list of all existing inventory entries",tags=["INVENTORY"])
def inventory(db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    return db.query(models.Inventory).all()

@router.get("/inventory/specific", summary="Return a specific item given the id",tags=["INVENTORY"])
def inventory(item_id: int, warehouse_id: int,db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    inventory_model = db.query(models.Inventory).filter(models.Inventory.item_id == item_id).filter(models.Inventory.warehouse_id == warehouse_id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )
    
    return inventory_model
   

@router.get("/inventory/warehouse", summary="Return a all inventory entries associated with the warehouse_id",tags=["INVENTORY"])
def inventory(warehouse_id: int,db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    inventory_chunk = db.query(models.Inventory).filter(models.Inventory.warehouse_id == warehouse_id).all()

    if inventory_chunk is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse_id} does not exist"
        )
    
    return inventory_chunk

    
@router.get("/inventory/item", summary="Return a all inventory entries associated with the item_id",tags=["INVENTORY"])
def inventory(item_id: int,db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    inventory_chunk = db.query(models.Inventory).filter(models.Inventory.item_id == item_id).all()

    if inventory_chunk is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )
    
    return inventory_chunk
   

@router.post("/inventory/new", summary="Create a new inventory entry given a JSON objec", 
                            description="If an entry with an identical item_id and warehouse_id exists, the quantity of this new object will be added to the existing one",
                            tags=["INVENTORY"])
def inventory_entry(inventory: helper_objects.Inventory, db:Session = Depends(database.get_db)):

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    item_model = db.query(models.Item).filter(models.Item.id == inventory.item_id).first()

    if item_model is None:
       raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {inventory.item_id} does not exist"
        )

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == inventory.warehouse_id).first()

    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {inventory.warehouse_id} does not exist"
        )

    #create inventory entry object
    inventory_model = models.Inventory()
    inventory_model.item_id = inventory.item_id
    inventory_model.quantity = inventory.quantity
    inventory_model.warehouse_id = inventory.warehouse_id

    #if the item already exists at that warehouse, then add the quantities
    existing_item_quantity = db.query(models.Inventory.quantity).filter(models.Inventory.item_id == inventory.item_id).filter(models.Inventory.warehouse_id == inventory.warehouse_id).first()

    if existing_item_quantity is not None:
        inventory_model.quantity += existing_item_quantity[0]
        db.query(models.Inventory).filter(models.Inventory.item_id == inventory.item_id).filter(models.Inventory.warehouse_id == inventory.warehouse_id).delete()

    db.add(inventory_model)
    db.commit()

    return inventory



@router.put('/inventory/edit', summary="Edit an inventory entry given the id, warehouse_id, and quantity ",tags=["INVENTORY"])
def edit_inventory(item_id: int, warehouse_id: int, quantity: int, id:int, db:Session = Depends(database.get_db)):

    #does item to change exist in this warehouse
    inventory_model = db.query(models.Inventory).filter(models.Inventory.id == id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Inventory entry with ID {item_id} does not exist"
        )

    db.query(models.Item).filter(models.Item.id == item_id).update({'warehouse_id':warehouse_id})
    db.query(models.Item).filter(models.Item.id == item_id).update({'item_id':item_id})
    db.query(models.Item).filter(models.Item.id == item_id).update({'quantity':quantity})


    db.commit()

    return inventory_model

@router.delete('/inventory/delete', summary="Deletes an inventory entry given the id",tags=["INVENTORY"])
def delete_inventory_item(id:int, db:Session = Depends(database.get_db)):
    
    inventory_model = db.query(models.Inventory).filter(models.Inventory.id == id).first()

    if inventory_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Inventory entry with ID {id} does not exist"
        )
        
    db.query(models.Inventory).filter(models.Inventory.id == id).delete()
    db.commit()

    return f"Inventory Entry with ID {id} deleted"

