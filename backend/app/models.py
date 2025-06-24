from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_wb = Column(BigInteger, unique=True) # id on wildberries
    name = Column(String, nullable=False)
    price_basic = Column(Float, nullable=True)
    price_with_discount = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    feedbacks = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Product(name={self.name}, price_basic={self.price_basic}, " \
               f"price_with_discount={self.price_with_discount}, rating={self.rating}, feedbacks={self.feedbacks})>"
