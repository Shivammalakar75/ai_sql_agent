# app/modules/product/product_router.py

from fastapi import APIRouter, HTTPException
from app.infrastructure.db.mysql_client import mysql_client
from app.modules.product.product_service import product_service
from app.modules.product.product_schema import (
    ProductCreate, ProductUpdate, ProductResponse
)

router = APIRouter(prefix="/product", tags=["CRUD"])


@router.post("/products", response_model=ProductResponse)
def create_product(data: ProductCreate):
    with mysql_client.get_session() as session:
        existing = product_service.get_by_id(session, data.id)
        if existing:
            raise HTTPException(400, f"Product {data.id} already exists")
        product = product_service.create(session, data)
        return ProductResponse.model_validate(product)

@router.get("/products", response_model=list[ProductResponse])
def get_all_products():
    with mysql_client.get_session() as session:
        return [ProductResponse.model_validate(p) for p in product_service.get_all(session)]

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    with mysql_client.get_session() as session:
        product = product_service.get_by_id(session, product_id)
        if not product:
            raise HTTPException(404, f"Product {product_id} not found")
        return ProductResponse.model_validate(product)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate):
    with mysql_client.get_session() as session:
        product = product_service.update(session, product_id, data)
        if not product:
            raise HTTPException(404, f"Product {product_id} not found")
        return ProductResponse.model_validate(product)

@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    with mysql_client.get_session() as session:
        success = product_service.delete(session, product_id)
        if not success:
            raise HTTPException(404, f"Product {product_id} not found")
        return {"message": f"Product {product_id} deleted successfully"}
