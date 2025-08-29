import os
from fastapi import FastAPI
from app.routers import users, stocks
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Monitor de Ações", version="0.1")

# include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])

@app.get("/")
def root():
    return {"msg": "API de Monitoramento de Ações rodando 🚀"}

# opcional: criar tabelas na inicialização (útil para dev)
if os.getenv("INIT_DB", "true").lower() in ("1","true","yes"):
    Base.metadata.create_all(bind=engine)
