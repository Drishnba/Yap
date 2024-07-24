from fastapi import APIRouter, HTTPException, Response, Depends
from sqlmodel import Session, select
from db import get_session
from model import User
from schem import UserCreate
from pydantic import EmailStr



router = APIRouter(tags=['user'],responses={404: {"description": "Not found"}})

@router.post('/register/')
def reg_user(first_name: str,surname: str,email: EmailStr,password: str,session: Session = Depends(get_session)):
    existing_user = session.scalars(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email address is already in use")
    database_user = User(first_name=first_name, surname=surname, email=email, password=password)
    session.add(database_user)
    session.commit()
    raise HTTPException(status_code=200)