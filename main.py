from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User, Base
from schemas import UserCreate
from security import verify_password, get_password_hash, create_access_token, get_current_user
from logs import log_attempt
from schemas import UserResponse


app = FastAPI()

@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
