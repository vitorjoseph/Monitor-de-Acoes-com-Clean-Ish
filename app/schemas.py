from pydantic import BaseModel
from typing import Optional

# Users
class UserCreate(BaseModel):
    username: str
    password: str
    email   : str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

# Stocks
class StockBase(BaseModel):
    ticker: str
    price: Optional[float] = None

class StockCreate(StockBase):
    pass

class StockOut(StockBase):
    id: int
    class Config:
        orm_mode = True
