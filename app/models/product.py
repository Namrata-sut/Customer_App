from app.db.db_connection import Base
from sqlalchemy import Column, Integer, String, Float


class ProductModel(Base):
    __tablename__ = "product_table"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
