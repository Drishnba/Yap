from fastapi import FastAPI, Request, Response, Depends, APIRouter,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasicCredentials,HTTPBasic
from sqlmodel import Session, select
from model import Survey, User
from db import get_session

router = APIRouter(prefix="/surveys", tags=["Surveys"])
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), database: Session = Depends(get_session)):
    user = database.query(User).filter(User.email == credentials.username).first()
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user

@router.get("/create")
def create_survey(request: Request):
    return templates.TemplateResponse("create_survey.html", {"request": request})

@router.post("/create")
async def create_survey(request: Request, title: str, description: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    survey = Survey(title=title, description=description, user_id=user.id)
    session.add(survey)
    session.commit()
    return Response(status_code=201, content="Survey created successfully")