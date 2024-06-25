from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# 商品マスタ用のPydanticモデル
class ProductBase(BaseModel):  # /product GET query_parameter
    product_code: str


class ProductCreate(ProductBase):
    product_name: str
    product_price: int


class Product(ProductBase):  # /product GET　response_body
    product_id: int
    product_name: str
    product_price: int

    class Config:
        from_attributes = True  # Pydantic v2における設定（orm_mode = Trueに相当）


# 取引および取引詳細用のPydanticモデル


class TransactionDetail(BaseModel):
    product_code: str
    product_id: int
    product_name: str
    product_price: int
    product_count: int


class Transaction(BaseModel):
    employee_code: str
    store_code: int
    pos_number: int


class TransactionRequest(BaseModel):
    transaction: Transaction
    transactiondetails: List[TransactionDetail]

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    total_amount: int

    class Config:
        from_attributes = True
