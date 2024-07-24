from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select, Column, Integer, ForeignKey
import uuid


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    surname: str
    email: str
    password: str
    is_admin: bool = Field(default=False)
    is_banned: bool = Field(default=False)
    surveys: List['Survey'] = Relationship(back_populates="user",sa_relationship_kwargs={"cascade": "all, delete"})
    responses: List['Response'] = Relationship(back_populates="user",sa_relationship_kwargs={"cascade": "all, delete"})

class Survey(SQLModel, table=True):
    __tablename__ = 'surveys'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID = Field(foreign_key="users.id",nullable=True)
    user: Optional['User'] = Relationship(back_populates="surveys",sa_relationship_kwargs={"cascade": "all, delete"})
    questions: List['Question'] = Relationship(back_populates="survey",sa_relationship_kwargs={"cascade": "all, delete"})
    responses: List['Response'] = Relationship(back_populates="survey",sa_relationship_kwargs={"cascade": "all, delete"})

class Question(SQLModel, table=True):
    __tablename__ = 'questions'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    text: str
    type: str  # текст, выбор, рейтинг и т.д.
    survey_id: uuid.UUID = Field(foreign_key="surveys.id",nullable=True)
    survey: Optional['Survey'] = Relationship(back_populates="questions",sa_relationship_kwargs={"cascade": "all, delete"})
    answer_options: List['AnswerOption'] = Relationship(back_populates="question",sa_relationship_kwargs={"cascade": "all, delete"})
    answers: List['Answer'] = Relationship(back_populates="question",sa_relationship_kwargs={"cascade": "all, delete"})

class AnswerOption(SQLModel, table=True):
    __tablename__ = 'answer_options'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    text: str
    question_id: uuid.UUID = Field(foreign_key="questions.id",nullable=True)
    question: Optional['Question'] = Relationship(back_populates="answer_options",sa_relationship_kwargs={"cascade": "all, delete"})
    answers: List['Answer'] = Relationship(back_populates="answer_option",sa_relationship_kwargs={"cascade": "all, delete"})

class Response(SQLModel, table=True):
    __tablename__ = 'responses'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id",nullable=True)
    user: 'User' = Relationship(back_populates="responses",sa_relationship_kwargs={"cascade": "all, delete"})
    survey_id: uuid.UUID = Field(foreign_key="surveys.id",nullable=True)
    survey: 'Survey' = Relationship(back_populates="responses",sa_relationship_kwargs={"cascade": "all, delete"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    answers: List['Answer'] = Relationship(back_populates="response",sa_relationship_kwargs={"cascade": "all, delete"})

class Answer(SQLModel, table=True):
    __tablename__ = 'answers'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    response_id: uuid.UUID = Field(foreign_key="responses.id",nullable=True)
    response: 'Response' = Relationship(back_populates="answers",sa_relationship_kwargs={"cascade": "all, delete"})
    question_id: uuid.UUID = Field(foreign_key="questions.id",nullable=True)
    question: 'Question' = Relationship(back_populates="answers",sa_relationship_kwargs={"cascade": "all, delete"})
    answer_option_id: Optional[uuid.UUID] = Field(foreign_key="answer_options.id",nullable=True)
    answer_option: Optional['AnswerOption'] = Relationship(back_populates="answers",sa_relationship_kwargs={"cascade": "all, delete"})
    text: Optional[str]  # для текстовых ответов
    rating: Optional[int]  # для рейтинговых ответов


