# uname() error回避
import platform

print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import Session
import json
import pandas as pd
from datetime import datetime, date

from db_control.connect import engine
from db_control import mymodels, schemas


def selectProduct(db: Session, product_code):
    mymodel = mymodels.Products
    stmt = select(mymodel).where(mymodel.product_code == product_code)

    # トランザクションを開始
    with db.begin():
        df = pd.read_sql_query(stmt, con=engine)
        if df.empty:
            result_dict = None
        else:
            result_dict = df.to_dict(orient="records")[0]  # リストの１つ目

    return result_dict


# def insertTransaction(db: Session, transaction):
#     mymodel = mymodels.Transaction
