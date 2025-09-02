from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import crud, auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_action(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciais inválidas", "username": username})
    token = auth.create_access_token(user.username)
    response = RedirectResponse(url="/welcome", status_code=303)
    response.set_cookie("access_token", token)
    return response

@router.get("/welcome", response_class=HTMLResponse)
def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})
