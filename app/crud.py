from sqlalchemy.orm import Session
import models, schemas, auth

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_pw = auth.hash_password(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_pw, email=user_in.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_google_id(db: Session, google_id: str):
    return db.query(models.User).filter(models.User.google_id == google_id).first()

def create_stock(db: Session, stock_in: schemas.StockCreate, owner_id: int):
    db_stock = models.Stock(ticker=stock_in.ticker, price=stock_in.price, owner_id=owner_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stocks(db: Session, owner_id: int):
    return db.query(models.Stock).filter(models.Stock.owner_id == owner_id).all()

def create_or_update_user_from_google(db: Session, user_info: dict):
    """
    Cria usuário novo OU associa google_id a um usuário já existente (pelo email).
    """
    # Primeiro tenta achar pelo google_id
    user = get_user_by_google_id(db, user_info.get("sub"))
    if user:
        return user

    # Se não achou, tenta pelo email
    user = get_user_by_email(db, user_info.get("email"))
    if user:
        # Se já tinha conta mas sem google_id, associa
        if not user.google_id:
            user.google_id = user_info.get("sub")
            db.commit()
            db.refresh(user)
        return user

    # Se não existe, cria do zero
    db_user = models.User(
        username=user_info.get("name"),
        email=user_info.get("email"),
        hashed_password=None,  # login só via Google
        google_id=user_info.get("sub"),
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
