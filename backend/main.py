from fastapi import FastAPI
from typing import Optional

from db_control import crud, mymodels

app = FastAPI()


@app.get("/allproducts/")
def read_all_customer():
    model = mymodels.Products
    result = crud.myselectAll(model)
    return result, 200
