from app.db.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Computed
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import datetime


class OrderModel(Base):
    __tablename__ = "order_table"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product_table.product_id'), nullable=False)
    quantity = Column(Integer, default=0)
    # total_price = Column(Float, Computed("quantity * (select price from product_table))", persisted=True))
    status = Column(String, nullable=False, default='pending')
    ordered_date = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship('ProductModel')  # allows access to the ProductModel from an OrderModel object.

    # It allows accessing total_price like a normal column while keeping it computed dynamically.
    # Works both in Python and in database queries.

    @hybrid_property
    def total_price(self):
        return self.quantity * self.product.price if self.product else 0.0
