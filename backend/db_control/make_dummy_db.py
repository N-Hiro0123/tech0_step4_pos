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


def InsertValue(mymodel, values):
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

# values = {
#     "product_code": "1111111111111",
#     "product_name": "1st_product",
#     "product_price": 1000,
# }

# InsertValue(mymodel, values)  # DBへ値を挿入

# values = {
#     "product_code": "2222222222222",
#     "product_name": "商品２",
#     "product_price": 2000,
# }

# InsertValue(mymodel, values)  # DBへ値を挿入

# values = {
#     "product_code": "3333333333333",
#     "product_name": "3rd_product",
#     "product_price": 3000,
# }

# InsertValue(mymodel, values)  # DBへ値を挿入

dummy_data_list = [
    {"product_code": "1234567890123", "product_name": "りんご", "product_price": 150},
    {"product_code": "2345678901234", "product_name": "牛乳", "product_price": 200},
    {"product_code": "3456789012345", "product_name": "食パン", "product_price": 100},
    {"product_code": "4567890123456", "product_name": "卵", "product_price": 300},
    {"product_code": "5678901234567", "product_name": "バター", "product_price": 400},
    {"product_code": "6789012345678", "product_name": "チーズ", "product_price": 350},
    {"product_code": "7890123456789", "product_name": "鶏胸肉", "product_price": 600},
    {"product_code": "8901234567890", "product_name": "オレンジジュース", "product_price": 250},
    {"product_code": "9012345678901", "product_name": "パスタ", "product_price": 300},
    {"product_code": "0123456789012", "product_name": "トマトソース", "product_price": 200},
]

for i in range(len(dummy_data_list)):
    InsertValue(mymodel, dummy_data_list[i])  # DBへ値を挿入


# userデータの挿入

from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードのハッシュ化と検証
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


values = {
    "user_name": "user1",
    "user_password": get_password_hash("user1"),
}

mymodel = mymodels.UserDatas
InsertValue(mymodel, values)
