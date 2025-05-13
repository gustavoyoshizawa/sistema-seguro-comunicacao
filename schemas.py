from pydantic import BaseModel

class UserResponse(BaseModel):
    email: str
    is_active: bool
    role: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str