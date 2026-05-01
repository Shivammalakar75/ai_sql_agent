# app/services/crud/user_service.py

from sqlalchemy.orm import Session
from app.infrastructure.db.models import User
from app.api.schemas.crud_schemas import UserCreate, UserUpdate
from app.shared.logger import get_logger

logger = get_logger(__name__)


class UserService:

    def create(self, session: Session, data: UserCreate) -> User:
        user = User(id=data.id, name=data.name, email=data.email)
        session.add(user)
        session.flush()
        logger.info(f"User created: {user.id}")
        return user

    def get_all(self, session: Session) -> list[User]:
        return session.query(User).all()

    def get_by_id(self, session: Session, user_id: int) -> User | None:
        return session.query(User).filter(User.id == user_id).first()

    def update(self, session: Session, user_id: int, data: UserUpdate) -> User | None:
        user = self.get_by_id(session, user_id)
        if not user:
            return None
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        session.flush()
        logger.info(f"User updated: {user_id}")
        return user

    def delete(self, session: Session, user_id: int) -> bool:
        user = self.get_by_id(session, user_id)
        if not user:
            return False
        session.delete(user)
        logger.info(f"User deleted: {user_id}")
        return True


user_service = UserService()