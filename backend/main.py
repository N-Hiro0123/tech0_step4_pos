from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import sessionmaker, Session

from db_control import crud, mymodels, schemas
from db_control.connect import engine

app = FastAPI()

# 許可するオリジンを設定
origins = [
    "http://localhost:3000",  # Reactアプリがホストされている場所
    # 必要に応じて他のオリジンも追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッドを指定
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定
)


# データベースセッションの取得
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/product", response_model=Optional[schemas.Product])
# def read_product(product_code: str, db: Session = Depends(get_db)):
#     result = crud.selectProduct(db, product_code)
#     if result is None:
#         return None
#     return result


# dummy
@app.get("/product", response_model=Optional[schemas.Product])
async def read_product():
    result = {
        "product_code": "2222222222222",
        "product_id": 2,
        "product_name": "商品２",
        "product_price": 2000,
    }
    return result


# @app.post("/transaction", response_model=schemas.Transaction)
# def insert_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
#     model = mymodels.Transactions
#     result = crud.insertTransaction(db, transaction)
