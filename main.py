import secrets

from fastapi import FastAPI, Depends
from typing import List, Optional

from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from Database.database import engine, SessionLocal
from Models import models, schemas

models.Base.metadata.create_all(bind=engine)


origins = [
    "*"
]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"Hello": "World!"}


@app.post("/user/register", response_model=schemas.UserToken)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_model = models.User(
        username=user.username,
        password=user.password
    )

    user_token = models.UserToken(
        token=secrets.token_hex(16)
    )

    db.add(user_token)
    db.add(user_model)

    try:
        db.commit()
    except Exception:
        return {"error": "yes"}

    return user_token


@app.post("/user/login", response_model=schemas.UserToken)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.username == user.username).first()
    if found_user is None:
        return {"error": "yes"}

    if found_user.password != user.password:
        return {"error": "yes"}

    token = db.query(models.UserToken).filter(models.UserToken.user_id == found_user.id).first()

    return token
