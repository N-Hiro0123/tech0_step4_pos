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
        orm_mode = True


# 取引および取引詳細用のPydanticモデル
class TransactionDetailBase(BaseModel):
    product_id: int
    product_code: str
    product_name: str
    product_price: int


class TransactionDetailCreate(TransactionDetailBase):
    pass


class TransactionDetail(TransactionDetailBase):  # request_boyの中で使う
    transaction_id: int
    detail_id: int

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    employee_code: str
    store_code: str
    pos_number: str


class TransactionCreate(TransactionBase):
    transaction_details: List[TransactionDetailCreate]


class Transaction(TransactionBase):  # /transition POST request_body
    transaction_id: int
    trade_datetime: datetime
    total_amount: int
    transaction_details: List[TransactionDetail]

    class Config:
        orm_mode = True

class PurchaseItem(BaseModel):
    product_id: int
    product_code: str
    product_name: str
    product_price: int

class PurchaseRequest(BaseModel):
    employee_code: str
    items: List[PurchaseItem]

class PurchaseResponse(BaseModel):
    success: bool
    total_amount: int
