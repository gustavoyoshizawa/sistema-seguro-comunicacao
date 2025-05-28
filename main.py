# main.py

# ... (seus imports no início do arquivo) ...
# Certifique-se que você tem todos os imports que já discutimos:
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session # Para anotação de tipo

import models
import schemas
import crud
from database import engine, Base, get_db
from auth import (
    create_access_token,
    authenticate_user,
    get_current_active_user,
    get_admin_user,
    oauth2_scheme, # Mantenha importado, pois é usado em outras rotas
    get_current_user # Mantenha importado, pois é usado em outras rotas
)

from datetime import timedelta

# Cria as tabelas no banco (execute isso apenas uma vez na inicialização da aplicação)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Módulo de Autenticação e Gestão de Usuários")

# Configuração para templates HTML
templates = Jinja2Templates(directory="templates")

# --- ROTAS PARA SERVIR AS PÁGINAS HTML DE TESTE ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Redireciona para a página de login por padrão."""
    return RedirectResponse(url="/login_page")

@app.get("/register_page", response_class=HTMLResponse)
async def get_register_page(request: Request):
    """Página para registro de novos usuários."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login_page", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Página para login de usuários existentes."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/me_page", response_class=HTMLResponse)
async def get_me_page(request: Request):
    """Página para visualizar informações do usuário logado e seus logs."""
    return templates.TemplateResponse("me.html", {"request": request})

# --- ROTA PARA A PÁGINA DE ADMIN LOGS (HTML) ---
# Esta rota serve a página HTML. A proteção agora é feita no JavaScript DA PÁGINA HTML.
@app.get("/admin_logs_page", response_class=HTMLResponse)
async def get_admin_logs_page(request: Request):
    """
    Página para visualizar todos os logs do sistema.
    A verificação de permissão de admin é feita no frontend (JavaScript)
    após o carregamento da página, redirecionando o usuário se não for admin.
    Os dados da API (/admin/logs) continuam protegidos pelo backend.
    """
    return templates.TemplateResponse("admin_logs.html", {"request": request})

# --- FIM DAS ROTAS DE PÁGINAS HTML ---


# --- ENDPOINTS DA API (APENAS PARA REFERÊNCIA, ESTES ESTÃO CORRETOS) ---

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário no sistema."""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    db_email = crud.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = crud.create_user(db=db, user=user)
    crud.create_log(db, user_id=new_user.id, action="Registro")
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    crud.create_log(db, user_id=user.id, action="Login")

    # --- MODIFIQUE ESTA LINHA PARA TESTE ---
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "hashed_password": user.hashed_password # <--- ADICIONE ESTA LINHA
    }


@app.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_active_user)):
    """Obtém as informações do usuário logado."""
    return current_user


@app.get("/logs", response_model=list[schemas.LogOut])
def get_user_logs(
    current_user: schemas.UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Obtém os logs de atividade do usuário logado."""
    return crud.get_logs(db, user_id=current_user.id)


@app.get("/admin/logs", response_model=list[schemas.LogOut])
def get_all_logs(
    admin_user: schemas.UserOut = Depends(get_admin_user), # ESTA É A PROTEÇÃO REAL DA API
    db: Session = Depends(get_db),
):
    """Obtém todos os logs do sistema (requer permissão de administrador)."""
    return db.query(models.Log).all()