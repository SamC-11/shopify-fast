from pydantic import BaseModel, Field

#This class is to add new items
class Item(BaseModel):
    name: str = Field(min_length=1)
    


#This class is the object used to add inventory entries
class Inventory(BaseModel):
    item_id: int = Field(gt=-1)
    warehouse_id: int = Field(gt=-1)
    quantity: int = Field(gt=-1)


#This class is the object used to add warehouse(s)
class Warehouse(BaseModel):
    name: str = Field(min_length=1)
