
# app/modules/__init__.py
from fastapi import APIRouter

from app.modules.user.user_router import router as user_router
from app.modules.product.product_router import router as product_router
from app.modules.order.order_router import router as order_router

crud_router = APIRouter()

crud_router.include_router(user_router)
crud_router.include_router(product_router)
crud_router.include_router(order_router)