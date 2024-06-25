from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session

# from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, ValidationError

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


@app.get("/product", response_model=Optional[schemas.Product])
async def read_product(product_code: str, db: Session = Depends(get_db)):
    result = crud.selectProduct(db, product_code)
    return result


@app.post("/purchase", response_model=schemas.TransactionResponse)
def create_purchase(purchase: schemas.TransactionRequest, db: Session = Depends(get_db)):
    try:
        total_amount = 0

        # 取引テーブルへ登録
        transaction = mymodels.Transactions(
            # datetime=datetime.now(),
            employee_code=purchase.transaction.employee_code,
            store_code=purchase.transaction.store_code,
            pos_number=purchase.transaction.pos_number,
            total_amount=0,
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        transaction_id = transaction.transaction_id

        # 取引明細へ登録
        detail_id = 0
        for idx, item in enumerate(purchase.transactiondetails):
            for count in range(item.product_count):
                detail_id += 1
                detail = mymodels.TransactionDetails(
                    transaction_id=transaction_id,
                    detail_id=detail_id,
                    product_id=item.product_id,
                    product_code=item.product_code,
                    product_name=item.product_name,
                    product_price=item.product_price,
                )
                db.add(detail)
                total_amount += item.product_price

        # 取引テーブルを更新
        transaction.total_amount = total_amount
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return schemas.TransactionResponse(total_amount=total_amount)


# # dummy
# @app.get("/product", response_model=Optional[schemas.Product])
# async def read_product():
#     result = {
#         "product_code": "2222222222222",
#         "product_id": 2,
#         "product_name": "商品２",
#         "product_price": 2000,
#     }
#     return result


# # dummy
# @app.post("/transaction", response_model=schemas.TransactionResponse)
# async def insert_transaction(transaction_request: schemas.TransactionRequest):
#     result = {"total_amount": 1500}
#     # print(result)
#     return result


# エラーを確認する際に使ったもの
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": exc.errors()},
#     )
