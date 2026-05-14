from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.local_db import get_local_db

router = APIRouter(prefix="/auth", tags=["auth"])

class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_local_db)):
    # Aqui entraria a lógica real de hash de senha e salvar no banco local
    return {"message": "Usuário registrado com sucesso no banco local", "username": user.username}

@router.post("/login")
def login_user(user: UserRegister, db: Session = Depends(get_local_db)):
    # Aqui entraria a lógica de verificação
    return {"token": "fake-jwt-token"}
