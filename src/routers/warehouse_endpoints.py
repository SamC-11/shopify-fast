from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import sys
sys.path.append('..')
from src import database, models, helper_objects



router = APIRouter()

# --------------------------------- WAREHOUSE ENDPOINT(S) -----------------------------------------------


@router.get("/warehouses", summary="Return a list of all existing warehouses as a JSON", tags=["WAREHOUSES"])
def warehouses(db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    return db.query(models.Warehouse).all()

@router.get("/warehouses/specific", summary="Return a specific warehouse given the id",tags=["WAREHOUSES"])
def warehouses(warehouse_id:int,db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with ID {warehouse_id} does not exist"
        )
    
    return warehouse_model


@router.post("/warehouses/new", summary="Create a new warehouse object given a JSON input",tags=["WAREHOUSES"])
def new_warehouse(warehouse: helper_objects.Warehouse, db:Session = Depends(database.get_db)):
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.name == warehouse.name).first()
    if warehouse_model is None:
        warehouse_model = models.Warehouse()
        warehouse_model.name = warehouse.name
        db.add(warehouse_model)
        db.commit()

    else:
        raise HTTPException(
            status_code = 404,
            detail = f"Warehouse with name {warehouse.name} already exist"
        )
    
    return db.query(models.Warehouse).filter(models.Warehouse.name == warehouse.name).first()
    


@router.put('/warehouses/edit', summary="Edit an existing warehouse given the id and a new name",tags=["WAREHOUSES"])
def edit_warehouse(warehouse_id: int, new_name: str, db: Session = Depends(database.get_db)):
    warehouse_model = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

    if warehouse_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {warehouse_id} does not exist"
        )

    db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).update({'name':new_name})
    db.commit()

    return db.query(models.Warehouse).filter(models.Warehouse.name == new_name).first()



@router.delete('/warehouses/delete', summary="Delete an existing warehouse",tags=["WAREHOUSES"])
def delete_item(warehouse_id: int, db:Session = Depends(database.get_db)):
    
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

