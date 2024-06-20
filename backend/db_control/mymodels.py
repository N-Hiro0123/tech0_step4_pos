from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    product_code: Mapped[str] = mapped_column(String(13))
    product_name: Mapped[str] = mapped_column(String(50))
    product_price: Mapped[int] = mapped_column(Integer)
