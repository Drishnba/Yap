from fastapi import APIRouter,Request,HTTPException, Response, Depends, Request,responses,status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session,select
from model import User
from db import get_session
from fastapi.responses import RedirectResponse
from pydantic import EmailStr


router = APIRouter(prefix="/login",tags=["Login"])
templates = Jinja2Templates(directory="templates")

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@router.post("/login")
async def login(request: Request, database: Session = Depends(get_session)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = database.exec(select(User).where(User.email == email)).first()
    if not user or user.password != password:
        return Response(content="Неправильный email или пароль",media_type="text/plain",status_code=401)
    return RedirectResponse(url="/surveys/", status_code=302)