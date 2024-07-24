from fastapi import APIRouter,Request,HTTPException, Response, Depends, Request,responses,status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session,select
from model import User
from db import get_session
from fastapi.responses import RedirectResponse
from pydantic import EmailStr


router = APIRouter(prefix="/register",tags=["Registration"])
templates = Jinja2Templates(directory="templates")

@router.get("/register")
def reg(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@router.post("/register")
async def reg(request: Request, database: Session = Depends(get_session)):
    form_data = await request.form()
    first_name = form_data["first_name"]
    surname = form_data["surname"]
    email = form_data["email"]
    password = form_data["password"]
    user = database.scalars(select(User).where(User.email == email)).first()
    if user:
        return Response(content="Такой Email уже используется", media_type="text/plain", status_code=400)

    user = User(first_name=first_name, surname=surname, email=email, password=password)
    database.add(user)
    database.commit()
    return RedirectResponse(url="/surveys/", status_code=302)