from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.schemas.product import ProductSchema, ProductUpdateSchema
from app.db.db_connection import get_db
router = APIRouter()

# {Product_id} inside the URL is a dynamic value. The value is extracted from the URL when the endpoint is called.


@router.get("/get_product_by_id/{product_id}")
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        product = await ProductService.get_by_id(product_id, db)
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.get("/get_product_by_name/{product_name}")
async def get_product_by_name(product_name: str, db: AsyncSession = Depends(get_db)):
    try:
        products = await ProductService.get_by_name(product_name, db)
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.get("/get_all_products")
async def get_all_products(db: AsyncSession = Depends(get_db)):
    try:
        products = await ProductService.get_all(db)
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.post("/add_new_product")
async def add_new_product(payload: ProductSchema, db: AsyncSession = Depends(get_db)):
    try:
        new_product = await ProductService.add(payload, db)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.put("/update_existing_product/{product_id}")
async def update_existing_product(product_id: int, payload: ProductUpdateSchema, db: AsyncSession=Depends(get_db)):
    try:
        updated_product = await ProductService.update(product_id, payload, db)
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")


@router.delete("/delete_existing_product/{product_id}")
async def delete_existing_product(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        product_deleted = await ProductService.delete(product_id, db)
        return product_deleted
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Occurred, Error: {e}")
