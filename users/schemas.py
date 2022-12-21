from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    password: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    token: str

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
