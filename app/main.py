import os
from frontend import login
from fastapi import FastAPI
from dotenv import load_dotenv
from database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from routers import users, stocks, google_auth

load_dotenv()

app = FastAPI(title="Monitor de Ações", version="0.1")

# Middleware de sessão obrigatório para Authlib
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "CHAVE_TEMPORARIA"),
    session_cookie="my_session",
    same_site="lax",
    https_only=False
)

# Frontend (HTML templates)
app.include_router(login.router, prefix="", tags=["frontend"])  # Prefixo vazio para rotas raiz

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Opcional: criar tabelas na inicialização (útil para dev)
if os.getenv("INIT_DB", "true").lower() in ("1", "true", "yes"):
    Base.metadata.create_all(bind=engine)

# APIs (JSON)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
app.include_router(google_auth.router)





