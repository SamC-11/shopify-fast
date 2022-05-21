from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import sys
sys.path.append('..')
from src import database, models, helper_objects



router = APIRouter()



# --------------------------------- ITEM ENDPOINT(S) -----------------------------------------------

@router.get("/items", summary="Return a list of all existing items",tags=["ITEMS"])
def items(db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    return db.query(models.Items).all()


@router.get("/items/specific", summary="Return a specific item given the id",tags=["ITEMS"])
def items(item_id: int, db: Session = Depends(database.get_db)): #Depends handles dependency injections for db session
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()
    
    if item_model is None:
        raise HTTPException(
                status_code = 404,
                detail = f"Item with ID {item_id} does not exist"
        )
    
    return item_model


@router.post("/items/new", summary="Create a new item object given a JSON input",tags=["ITEMS"])
def new_item(item: helper_objects.Item, db:Session = Depends(database.get_db)):

    #CHECK IF ITEM DOES NOT EXIST AT ALL
    item_model = db.query(models.Items).filter(models.Items.id == item.id).first()

    if item_model is None:
        #create new Item
        item_model = models.Items()
        item_model.id = item.id
        item_model.name = item.name

        db.add(item_model)
        db.commit()
    else:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item.id} already exist"
        )

    return item


@router.put('/items/edit', summary="Edit an existing item given the id and a new name",tags=["ITEMS"])
def edit_item(item_id: int, new_name: str, db: Session = Depends(database.get_db)):
    item_model = db.query(models.Items).filter(models.Items.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Item with ID {item_id} does not exist"
        )

    db.query(models.Items).filter(models.Items.id == item_id).update({'name':new_name})
    db.commit()

    return new_name

    
    


@router.delete('/items/delete', summary="Delete an existing warehouse given the id",tags=["ITEMS"])
def delete_item(item_id: int, db:Session = Depends(database.get_db)):
    
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





