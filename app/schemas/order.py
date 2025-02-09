from pydantic import BaseModel
import datetime
from typing import Optional # Optional[T]: A type hint from typing that allows a field to be either of type T or None.
from app.schemas.product import ProductSchema

# Schemas ensure that input data has the correct type and structure.


class OrderSchema(BaseModel):
    product_id: int
    quantity: int
    status: str
    ordered_date: datetime.datetime
    product: Optional[ProductSchema] = None

    class Config: # Config: A subclass that configures Pydantic behavior.
        from_attributes = True # from_attributes = True: Allows creating OrderSchema from ORM (SQLAlchemy) models.

    # Example: If you retrieve an SQLAlchemy object, Pydantic will convert it into a schema.
