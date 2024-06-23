from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.orm import sessionmaker, Session

from db_control import crud, mymodels, schemas

from db_control.connect import engine

app = FastAPI()


# データベースセッションの取得
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/product", response_model=Optional[schemas.Product])
def read_product(product_code: str, db: Session = Depends(get_db)):
    result = crud.selectProduct(db, product_code)
    if result is None:
        return None
    return result


# @app.post("/transaction", response_model=schemas.Transaction)
# def insert_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
#     model = mymodels.Transactions
#     result = crud.insertTransaction(db, transaction)
