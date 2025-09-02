from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, auth
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.StockOut)
def add_stock(stock: schemas.StockCreate, db: Session = Depends(auth.get_db), current_user = Depends(auth.get_current_user)):
    return crud.create_stock(db, stock, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.StockOut])
def list_stocks(db: Session = Depends(auth.get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_stocks(db, owner_id=current_user.id)
