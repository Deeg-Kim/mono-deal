import hashlib
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from model.base import User
from model.exception import InvalidRequestError
from model.users_api import RegisterUserRequest
from storage.user_db import UsersDB, get_users_db

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", name="Register new user", description="Register new user")
async def register_user(
        body: RegisterUserRequest,
        users_db: Annotated[UsersDB, Depends(get_users_db)]
) -> User:
    user_id = str(uuid.uuid4())

    maybe_user = users_db.get_user_by_email(body.email)

    if maybe_user is not None:
        raise InvalidRequestError(f"User with email {body.email} already exists")

    user = User(
        id=user_id,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        password=hashlib.md5(body.password.encode()).hexdigest()
    )

    users_db.create_user(user)

    return user


@router.get("/{id}", name="Get user by ID", description="Get user by id")
async def get_user(
        id: str,
        users_db: Annotated[UsersDB, Depends(get_users_db)]
) -> User:
    return users_db.get_user(id)
