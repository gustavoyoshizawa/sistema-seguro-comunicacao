from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
import crud
import models
# from database import SessionLocal # Removido, pois get_db será importado de database.py

# Se você vai usar get_db de database.py, você deve importá-lo:
from database import SessionLocal, get_db # Importa SessionLocal e get_db

# Configurações do Token
SECRET_KEY = "sua-chave-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --- FUNÇÃO 'authenticate_user' ADICIONADA/CORRIGIDA ---
def authenticate_user(db: Session, username: str, password: str):
    """
    Autentica um usuário verificando suas credenciais.
    Retorna o objeto User se a autenticação for bem-sucedida, caso contrário, False.
    """
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False  # Usuário não encontrado
    # Assumindo que seu modelo de usuário tem um atributo 'hashed_password'
    if not verify_password(password, user.hashed_password):
        return False  # Senha incorreta
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- ATENÇÃO: DUPLICAÇÃO DA FUNÇÃO get_db ---
# Você tem uma função get_db definida aqui e também em database.py.
# É uma boa prática ter apenas uma definição centralizada (em database.py).
# Se main.py importa get_db de database.py, você pode REMOVER esta função daqui
# para evitar confusão e garantir que a lógica de DB esteja em um só lugar.
# Se você remover esta função, certifique-se de que get_current_user
# e outras funções que a usam importem get_db de database.py.
# Por exemplo, no início deste arquivo: from database import get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user