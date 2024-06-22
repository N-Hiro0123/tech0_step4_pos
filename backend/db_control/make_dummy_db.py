# uname() error回避
import platform

print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from datetime import date, datetime
import pandas as pd

from connect import engine
import mymodels as mymodels


def InsertValue(mymodel, valuse):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # 新規データの挿入
    query = insert(mymodel).values(values)

    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()

    return


##################################################################################

# Users
mymodel = mymodels.Products

values = {
    "product_code": "1111111111111",
    "product_name": "1st_product",
    "product_price": 1000,
}

InsertValue(mymodel, values)  # DBへ値を挿入

values = {
    "product_code": "2222222222222",
    "product_name": "商品２",
    "product_price": 2000,
}

InsertValue(mymodel, values)  # DBへ値を挿入

values = {
    "product_code": "3333333333333",
    "product_name": "3rd_product",
    "product_price": 3000,
}

InsertValue(mymodel, values)  # DBへ値を挿入
