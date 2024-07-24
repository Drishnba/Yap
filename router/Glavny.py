from fastapi import FastAPI, Request, Response, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from model import Survey
from db import get_session

router = APIRouter(prefix="/surveys", tags=["Surveys"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
def surveys(request: Request, session: Session = Depends(get_session)):
    surveys = session.exec(select(Survey)).all()
    return templates.TemplateResponse("Glavny.html", {"request": request, "surveys": surveys})

@router.get("/search")
def search_surveys(request: Request, title: str, session: Session = Depends(get_session)):
    surveys = session.exec(select(Survey).where(Survey.title.like(f"%{title}%"))).all()
    return templates.TemplateResponse("Glavny.html", {"request": request, "surveys": surveys})
