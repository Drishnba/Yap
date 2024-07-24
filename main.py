import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from model import User
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from webka import register as webka_register
from webka import Create_sur as webka_Create_sur
from webka import Auth as webka_auth
from db import get_session,engine
from sqlmodel import SQLModel
from router import register
from router import Auth
from router import Glavny

SQLModel.metadata.create_all(engine)

app = FastAPI()

security = HTTPBasic()

'''@app.get("/register/")
async def register_user(first_name: str, surname: str, email: EmailStr, password: str, session: Session = Depends(get_session)):
    existing_user = session.scalars(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email address is already in use")

    user = User(first_name=first_name, surname=surname, email=email, password=password)
    session.add(user)
    session.commit()
    return {"id": user.id}'''

@app.get("/user/{user_id}")
async def read_user(user_id: str,credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
def authenticate_user(username: str, password: str, session: Session) -> bool:
    user = session.exec(select(User).where(User.email == username)).first()
    if user and user.password == password:
        return True
    return False

@app.post("/admin/")
async def create_admin(first_name: str, surname: str, email: str, password: str, session: Session = Depends(get_session)):
    user = User(first_name=first_name, surname=surname, email=email, password=password, is_admin=True)
    session.add(user)
    session.commit()
    return {"id": user.id}


@app.post("/ban/{user_id}")
async def ban_user(user_id: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user:
        user.is_banned = True
        session.commit()
        return {"message": "User banned"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user:
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

'''@app.post("/surveys/{user_id}")
async def create_surveys(user_id: str, title: str, description: str,credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_banned:
        raise HTTPException(status_code=228, detail="You are banned and cannot create surveys")
    survey = Survey(title=title, description=description, user_id=user_id)
    session.add(survey)
    session.commit()
    return {"id": survey.id}

@app.get("/surveys/{surveys_id}")
def read_survey(surveys_id: str, session: Session = Depends(get_session)):
    surveys = session.exec(select(Survey).where(Survey.id == surveys_id)).first()
    return surveys


@app.post("/questions")
async def create_question(text: str, type: str, survey_id: str,credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    question = Question(text=text, type=type, survey_id=survey_id)
    session.add(question)
    session.commit()
    return {"id": question.id}

@app.get("/question/{question_id}")
def read_question(question_id: str, session: Session = Depends(get_session)):
    question = session.exec(select(Question).where(Question.id == question_id)).first()
    return question

@app.post("/answer_options")
async def create_answer_option(text: str, question_id: str,credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    answer_option = AnswerOption(text=text, question_id=question_id)
    session.add(answer_option)
    session.commit()
    return {"id": answer_option.id}

@app.get("/answer_option/{answer_option_id}")
def read_question(answer_option_id: str, session: Session = Depends(get_session)):
    answer_option = session.exec(select(AnswerOption).where(AnswerOption.id == answer_option_id)).first()
    return answer_option

@app.post("/responses")
async def create_response(user_id: str,survey_id: str,question_id: str,credentials: HTTPBasicCredentials = Depends(security),session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    response = Response(user_id=user_id,survey_id=survey_id)
    session.add(response)
    session.commit()
    return {"id": response.id}

@app.get("/response/{response_id}")
def read_response(response_id: str, session: Session = Depends(get_session)):
    response = session.exec(select(Response).where(Response.id == response_id)).first()
    return response

@app.post("/answers")
async def create_answer(response_id: str, question_id: str, answer_option_id: str, text: str,rating:int,credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    if not authenticate_user(credentials.username, credentials.password, session):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    answer = Answer(response_id=response_id, question_id=question_id, answer_option_id=answer_option_id, text=text, rating=rating)
    session.add(answer)
    session.commit()
    return {"id": answer.id}

@app.get("/answer/{answer_id}")
def read_answer(answer_id: str, session: Session = Depends(get_session)):
    answer = session.exec(select(Answer).where(Answer.id == answer_id)).first()
    return answer'''

app.include_router(webka_register.router)
app.include_router(register.router)
app.include_router(Auth.router)
app.include_router(webka_auth.router)
app.include_router(Glavny.router)
app.include_router(webka_Create_sur.router)

uvicorn.run(app, port=1337)