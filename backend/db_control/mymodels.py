# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import datetime
# from sqlalchemy import Column, Integer, String, create_engine


from sqlalchemy import ForeignKey, Integer, String, create_engine, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    product_code: Mapped[str] = mapped_column(String(13), unique=True)
    product_name: Mapped[str] = mapped_column(String(50))
    product_price: Mapped[int] = mapped_column(Integer)
    transaction_details = relationship("TransactionDetails", back_populates="product")


class Transactions(Base):
    __tablename__ = "transactions"
    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    trade_datetime: Mapped[datetime] = mapped_column(DateTime)
    emp_code: Mapped[str] = mapped_column(String(10))
    store_code: Mapped[str] = mapped_column(String(5))
    pos_number: Mapped[str] = mapped_column(String(3))
    total_amount: Mapped[int] = mapped_column(Integer)
    transaction_details = relationship("TransactionDetails", back_populates="transaction")


class TransactionDetails(Base):
    __tablename__ = "transaction_details"
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.transaction_id"), primary_key=True, nullable=False)
    detail_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), nullable=False)
    product_code: Mapped[str] = mapped_column(String(13))
    product_name: Mapped[str] = mapped_column(String(50))
    product_price: Mapped[int] = mapped_column(Integer)
    transaction = relationship("Transactions", back_populates="transaction_details")
    product = relationship("Products", back_populates="transaction_details")
