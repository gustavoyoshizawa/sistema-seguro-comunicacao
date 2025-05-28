from sqlalchemy.orm import Session
import models
import schemas
from auth import get_password_hash, verify_password # Assumindo que essas funções estão em auth.py


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)

    # A role do usuário agora virá diretamente do objeto 'user' (schemas.UserCreate)
    # schemas.UserCreate já deve ter 'role: Optional[str] = "user"' ou similar
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role, # <--- Agora usa a role vinda da requisição
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_log(db: Session, user_id: int, action: str):
    log = models.Log(user_id=user_id, action=action)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs(db: Session, user_id: int):
    return db.query(models.Log).filter(models.Log.user_id == user_id).all()