
# app/modules/order/order_router.py

from fastapi import APIRouter, HTTPException
from app.infrastructure.db.mysql_client import mysql_client
from app.modules.order.order_service import order_service
from app.modules.order.order_schema import (
    OrderCreate, OrderUpdate, OrderResponse,
)

router = APIRouter(prefix="/order", tags=["CRUD"])


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