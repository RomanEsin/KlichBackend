from datetime import datetime
from typing import List, Any, Optional, Dict, Tuple
from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class User(UserCreate):
    id: Optional[int]


class UserToken(BaseModel):
    token: str

    class Config:
        orm_mode = True
