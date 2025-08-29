from sqlalchemy.orm import Session
from app import models, schemas, auth

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_pw = auth.hash_password(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_stock(db: Session, stock_in: schemas.StockCreate, owner_id: int):
    db_stock = models.Stock(ticker=stock_in.ticker, price=stock_in.price, owner_id=owner_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stocks(db: Session, owner_id: int):
    return db.query(models.Stock).filter(models.Stock.owner_id == owner_id).all()
