import os
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client.errors import OAuthError

import crud
import auth
from database import SessionLocal

router = APIRouter()
oauth = OAuth()

# Helper para pegar DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuração do Google OAuth
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Início do login com Google
@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

#Retorna a URL que o frontend deve usar para redirecionar o usuário ao Google.
@router.get("/login/google-url")
async def get_google_login_url(request: Request):

    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    url = await oauth.google.authorize_redirect(request, redirect_uri)
    return {"url": str(url.url)}


# Callback do Google
@router.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        return {"error": "Falha no OAuth", "details": str(e)}

    print("TOKEN RECEBIDO:", token)  # <-- já vimos que vem completo

    # Proteção extra: se não tiver id_token, vamos forçar pegar o userinfo
    if "id_token" not in token:
        return {"error": "Google não retornou id_token", "token": token}

    # Pegando dados do userinfo
    user_info = token.get("userinfo")
    if not user_info:
        user_info = await oauth.google.parse_id_token(request, token)

    print("USER_INFO:", user_info)

    # Verifica se usuário existe no banco
    print(crud.get_user_by_username(db, "vitor"))
    user = crud.get_user_by_email(db, user_info["email"])
    if not user:
        user = crud.create_or_update_user_from_google(db, user_info)

    # Aqui você pode criar a sessão ou gerar JWT
    request.session["user"] = dict(user_info)

    return RedirectResponse(url="/welcome")


