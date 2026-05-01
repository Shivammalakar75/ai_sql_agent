# app/services/crud/product_service.py

from sqlalchemy.orm import Session
from app.infrastructure.db.models import Product
from app.api.schemas.crud_schemas import ProductCreate, ProductUpdate
from app.shared.logger import get_logger

logger = get_logger(__name__)


class ProductService:

    def create(self, session: Session, data: ProductCreate) -> Product:
        product = Product(id=data.id, name=data.name, price=data.price)
        session.add(product)
        session.flush()
        logger.info(f"Product created: {product.id}")
        return product

    def get_all(self, session: Session) -> list[Product]:
        return session.query(Product).all()

    def get_by_id(self, session: Session, product_id: int) -> Product | None:
        return session.query(Product).filter(Product.id == product_id).first()

    def update(self, session: Session, product_id: int, data: ProductUpdate) -> Product | None:
        product = self.get_by_id(session, product_id)
        if not product:
            return None
        if data.name is not None:
            product.name = data.name
        if data.price is not None:
            product.price = data.price
        session.flush()
        logger.info(f"Product updated: {product_id}")
        return product

    def delete(self, session: Session, product_id: int) -> bool:
        product = self.get_by_id(session, product_id)
        if not product:
            return False
        session.delete(product)
        logger.info(f"Product deleted: {product_id}")
        return True


product_service = ProductService()