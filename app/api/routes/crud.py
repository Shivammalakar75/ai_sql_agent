# app/api/routes/crud.py

from fastapi import APIRouter, HTTPException
from app.infrastructure.db.mysql_client import mysql_client
from app.services.crud.user_service import user_service
from app.services.crud.product_service import product_service
from app.services.crud.order_service import order_service
from app.api.schemas.crud_schemas import (
    UserCreate, UserUpdate, UserResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    OrderCreate, OrderUpdate, OrderResponse,
)

router = APIRouter(prefix="/crud", tags=["CRUD"])


# ─── USERS ──────────────────────────────────────

@router.post("/users", response_model=UserResponse)
def create_user(data: UserCreate):
    with mysql_client.get_session() as session:
        existing = user_service.get_by_id(session, data.id)
        if existing:
            raise HTTPException(400, f"User {data.id} already exists")
        user = user_service.create(session, data)
        return UserResponse.model_validate(user)

@router.get("/users", response_model=list[UserResponse])
def get_all_users():
    with mysql_client.get_session() as session:
        return [UserResponse.model_validate(u) for u in user_service.get_all(session)]

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    with mysql_client.get_session() as session:
        user = user_service.get_by_id(session, user_id)
        if not user:
            raise HTTPException(404, f"User {user_id} not found")
        return UserResponse.model_validate(user)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate):
    with mysql_client.get_session() as session:
        user = user_service.update(session, user_id, data)
        if not user:
            raise HTTPException(404, f"User {user_id} not found")
        return UserResponse.model_validate(user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    with mysql_client.get_session() as session:
        success = user_service.delete(session, user_id)
        if not success:
            raise HTTPException(404, f"User {user_id} not found")
        return {"message": f"User {user_id} deleted successfully"}


# ─── PRODUCTS ───────────────────────────────────

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


# ─── ORDERS ─────────────────────────────────────

@router.post("/orders", response_model=OrderResponse)
def create_order(data: OrderCreate):
    with mysql_client.get_session() as session:
        existing = order_service.get_by_id(session, data.id)
        if existing:
            raise HTTPException(400, f"Order {data.id} already exists")
        order = order_service.create(session, data)
        return OrderResponse.model_validate(order)

@router.get("/orders", response_model=list[OrderResponse])
def get_all_orders():
    with mysql_client.get_session() as session:
        return [OrderResponse.model_validate(o) for o in order_service.get_all(session)]

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    with mysql_client.get_session() as session:
        order = order_service.get_by_id(session, order_id)
        if not order:
            raise HTTPException(404, f"Order {order_id} not found")
        return OrderResponse.model_validate(order)

@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, data: OrderUpdate):
    with mysql_client.get_session() as session:
        order = order_service.update(session, order_id, data)
        if not order:
            raise HTTPException(404, f"Order {order_id} not found")
        return OrderResponse.model_validate(order)

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    with mysql_client.get_session() as session:
        success = order_service.delete(session, order_id)
        if not success:
            raise HTTPException(404, f"Order {order_id} not found")
        return {"message": f"Order {order_id} deleted successfully"}