from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List
from datetime import datetime

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

@app.get("/product/{code}", response_model=Optional[schemas.Product])
def read_product(code: str, db: Session = Depends(get_db)):
    result = crud.selectProduct(db, code)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@app.post("/purchase", response_model=schemas.PurchaseResponse)
def create_purchase(purchase: schemas.PurchaseRequest, db: Session = Depends(get_db)):
    try:
        total_amount = 0

        # 取引テーブルへ登録
        transaction = mymodels.Transactions(
            datetime=datetime.now(),
            employee_code=purchase.employee_code,
            store_code='30',
            pos_no='90',
            total_amt=0
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        transaction_id = transaction.transaction_id

        # 取引明細へ登録
        for idx, item in enumerate(purchase.items):
            detail = mymodels.TransactionDetails(
                transaction_id=transaction_id,
                detail_id=idx + 1,
                product_id=item.product_id,
                product_code=item.product_code,
                product_name=item.product_name,
                product_price=item.product_price
            )
            db.add(detail)
            total_amount += item.product_price

        # 取引テーブルを更新
        transaction.total_amt = total_amount
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return schemas.PurchaseResponse(success=True, total_amount=total_amount)




