from sqlalchemy import ForeignKey, Integer, String, CHAR, VARCHAR, create_engine, Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    product_code: Mapped[str] = mapped_column(CHAR(13), unique=True)
    product_name: Mapped[str] = mapped_column(VARCHAR(50))
    product_price: Mapped[int] = mapped_column(Integer)
    transaction_details = relationship("TransactionDetails", back_populates="products")

    # # テーブル毎に設定する場合を参考までにメモ（今回はengineで全体に設定するため使わない）
    # __table_args__ = {
    #     'mysql_charset': 'utf8mb4',  # mysqlの文字セット（エンコード方式）
    #     'mysql_collate': 'utf8mb4_unicode_ci',  # mysqlのコレーション（比較・並べ替えの順序）
    # }


class Transactions(Base):
    __tablename__ = "transactions"
    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    trade_datetime: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    employee_code: Mapped[str] = mapped_column(CHAR(10), default="9999999999")
    store_code: Mapped[str] = mapped_column(CHAR(5))
    pos_number: Mapped[str] = mapped_column(CHAR(3))
    total_amount: Mapped[int] = mapped_column(Integer)
    transaction_details = relationship("TransactionDetails", back_populates="transactions")


class TransactionDetails(Base):
    __tablename__ = "transaction_details"
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.transaction_id"), primary_key=True, nullable=False)
    detail_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), nullable=False)
    product_code: Mapped[str] = mapped_column(CHAR(13))
    product_name: Mapped[str] = mapped_column(VARCHAR(50))
    product_price: Mapped[int] = mapped_column(Integer)
    transactions = relationship("Transactions", back_populates="transaction_details")
    products = relationship("Products", back_populates="transaction_details")
