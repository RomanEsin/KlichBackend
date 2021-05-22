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
    full_name: str
    about: str
    user_id: int

    class Config:
        orm_mode = True
