
# app/modules/user/user_router.py

from fastapi import APIRouter, HTTPException
from app.infrastructure.db.mysql_client import mysql_client
from app.modules.user.user_service import user_service
from app.modules.user.user_schema import (
    UserCreate, UserUpdate, UserResponse
)

router = APIRouter(prefix="/user", tags=["CRUD"])


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
