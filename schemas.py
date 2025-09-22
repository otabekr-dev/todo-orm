from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    first_name: str = Field(min_length=5, max_length=64)
    last_name: Annotated[str | None, Field(min_length=5, max_length=64)] = None
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class TaskCreation(BaseModel):
    name: str
    description: str | None = None