from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    day: str
    date: str
    amount: Optional[float] = None 

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    todo: Optional[Todo] = None

    class Config:
        orm_mode = True
