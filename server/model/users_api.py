from pydantic import BaseModel

from model.base import User


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    email: str
    password: str


class LoginUserResponse(BaseModel):
    token: str
    expiry: int
    user: User
