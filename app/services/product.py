from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import ProductModel
from app.schemas.product import ProductSchema, ProductUpdateSchema
from fastapi import HTTPException, status


class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: int = None, product_name: str = None):
        self.product_id = product_id
        if product_id:
            self.detail = f"Product with Id {product_id} not found."
        elif product_name:
            self.detail = f"Product with Name {product_name} doesn't exist."
        else:
            self.detail = "Product not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class EmptyProductTableError(HTTPException):
    def __init__(self):
        self.detail = "Product Table is empty."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.detail)


class ProductService:
    @staticmethod
    async def get_by_id(product_id: int, db: AsyncSession):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await db.execute(query)
        product = result.scalars().first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return product

    @staticmethod
    async def get_by_name(product_name: str, db: AsyncSession):
        query = select(ProductModel).where(func.lower(ProductModel.name) == product_name.lower())
        result = await db.execute(query)
        products = result.scalars().all()
        if not products:
            raise ProductNotFoundError(product_name=product_name)
        return products

    @staticmethod
    async def get_all(db: AsyncSession):
        query = select(ProductModel)
        result = await db.execute(query)
        products = result.scalars().all()
        if not products:
            raise EmptyProductTableError
        return products

    @staticmethod
    async def add(payload: ProductSchema, db: AsyncSession):
        data = ProductModel(
            name=payload.name,
            price=payload.price,
            stock=payload.stock
        )
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data

    @staticmethod
    async def update(product_id: int, payload: ProductUpdateSchema, db: AsyncSession):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await db.execute(query)
        existing_product = result.scalars().first()
        if not existing_product:
            raise ProductNotFoundError(product_id=product_id)
        for key, value in payload.dict(exclude_unset = True).items():
            setattr(existing_product, key, value)

        await db.commit()
        await db.refresh(existing_product)
        return existing_product

    @staticmethod
    async def delete(product_id: int, db: AsyncSession):
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await db.execute(query)
        product = result.scalars().first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        await db.delete(product)
        await db.commit()
        return "product deleted"




