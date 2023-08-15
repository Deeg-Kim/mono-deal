from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    email: str
    password: str
