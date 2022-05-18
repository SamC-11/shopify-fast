from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID



app = FastAPI()


class Item(BaseModel):
    id: int = Field(gt=-1) #will be used as primary
    name: str = Field(min_length=1)
    quantity: int = Field(gt=-1)



INVENTORY = []


@app.get("/inventory")
def root():
    return INVENTORY


@app.post("/")
def add_item(item: Item):
    #ADD VALIDATION HERE
    INVENTORY.append(item)
    return item


@app.put('/{item_id}')
def update_inventory(item_id: int, newitem: Item):

    #TODO: put everything in db
    i = 0
    for item in INVENTORY:
        i += 1
        if item.id == item_id:
            INVENTORY[i-1] = newitem
            return INVENTORY[i-1]
    raise HTTPException(
        status_code = 404,
        detail = f"Item with ID {item_id} does not exist"
    )

def delete_item(item_id: int):
    #TODO: put everything in db 
    i = 0
    for item in INVENTORY:
        if item.id == item_id:
            del INVENTORY[i]
            return f"Item with ID {item_id} deleted"
        i += 1
    raise HTTPException(
        status_code = 404,
        detail = f"Item with ID {item_id} does not exist"
    )
        