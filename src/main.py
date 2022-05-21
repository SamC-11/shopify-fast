from fastapi import FastAPI, APIRouter
import uvicorn
from database import engine, get_db
import models
from routers import warehouse_endpoints, item_endpoints, inventory_endpoints



app = FastAPI()

app.include_router(warehouse_endpoints.router)
app.include_router(item_endpoints.router)
app.include_router(inventory_endpoints.router)


#creates db and table if it doesn't already exist
models.Base.metadata.create_all(bind=engine)



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port = 8000, log_level = "info")
