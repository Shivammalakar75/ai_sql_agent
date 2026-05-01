# app/services/crud/order_service.py

from sqlalchemy.orm import Session
from app.infrastructure.db.models import Order
from app.api.schemas.crud_schemas import OrderCreate, OrderUpdate
from app.shared.logger import get_logger

logger = get_logger(__name__)


class OrderService:

    def create(self, session: Session, data: OrderCreate) -> Order:
        order = Order(
            id=data.id,
            user_id=data.user_id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        session.add(order)
        session.flush()
        logger.info(f"Order created: {order.id}")
        return order

    def get_all(self, session: Session) -> list[Order]:
        return session.query(Order).all()

    def get_by_id(self, session: Session, order_id: int) -> Order | None:
        return session.query(Order).filter(Order.id == order_id).first()

    def update(self, session: Session, order_id: int, data: OrderUpdate) -> Order | None:
        order = self.get_by_id(session, order_id)
        if not order:
            return None
        if data.quantity is not None:
            order.quantity = data.quantity
        session.flush()
        logger.info(f"Order updated: {order_id}")
        return order

    def delete(self, session: Session, order_id: int) -> bool:
        order = self.get_by_id(session, order_id)
        if not order:
            return False
        session.delete(order)
        logger.info(f"Order deleted: {order_id}")
        return True


order_service = OrderService()