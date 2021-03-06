from datetime import datetime
from typing import List, Any, Optional, Dict, Tuple
from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    username: str
    password: str
    user_type: int

    class Config:
        orm_mode = True


class User(UserCreate):
    id: Optional[int]


class UserToken(BaseModel):
    token: str
    user_type: int

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    full_name: Optional[str]
    about: Optional[str]
    username: Optional[str]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class OrgProfile(UserProfile):
    pass


class Category(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True
