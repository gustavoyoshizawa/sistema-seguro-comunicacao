from pydantic import BaseModel, EmailStr
from typing import Optional # Importe Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user" # Permite receber 'role', com padrão 'user' se não for enviado

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: str # Garante que 'role' é incluído na saída
    
    # Adicione esta linha para compatibilidade com Pydantic V2 e SQLAlchemy
    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic V1

class Token(BaseModel):
    access_token: str
    token_type: str

class LogOut(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime # Assumindo que datetime está importado e usado para o tipo
    
    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic V1