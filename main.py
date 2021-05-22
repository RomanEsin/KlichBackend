import secrets

from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional

from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from Database.database import engine, SessionLocal
from Models import models, schemas

models.Base.metadata.create_all(bind=engine)

origins = [
    "*"
]

app = FastAPI()
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
        password=user.password,
        user_type=user.user_type
    )

    db.add(user_model)

    try:
        db.commit()
        db.flush()
    except Exception:
        raise HTTPException(detail="Account already exists", status_code=400)

    db.refresh(user_model)

    user_token = models.UserToken(
        token=secrets.token_hex(16),
        user_id=user_model.id,
        user_type=user_model.user_type
    )

    user_profile = models.UserProfile(
        user_id=user_model.id,
        username=user_model.username
    )

    db.add(user_profile)
    db.add(user_token)
    db.commit()

    return user_token


@app.post("/user/login", response_model=schemas.UserToken)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.username == user.username).first()
    if found_user is None:
        raise HTTPException(detail="Invalid Username or Password", status_code=400)

    if found_user.password != user.password:
        raise HTTPException(detail="Invalid Username or Password", status_code=400)

    token = db.query(models.UserToken).filter(models.UserToken.user_id == found_user.id).first()

    return token


@app.get("/user/profile", response_model=schemas.OrgProfile)
def get_user_profile(user_token: str, db: Session = Depends(get_db)):
    user_token = db.query(models.UserToken).filter(models.UserToken.token == user_token).first()

    if user_token is None:
        raise HTTPException(detail="Invalid Username or Password", status_code=400)

    if user_token.user_type == 0:
        user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_token.user_id).first()
    else:
        user_profile = db.query(models.OrgProfile).filter(models.OrgProfile.user_id == user_token.user_id).first()

    return user_profile


@app.post("/user/edit", response_model=schemas.OrgProfile)
def update_user(user_token: str, user_profile_edited: schemas.UserProfile, db: Session = Depends(get_db)):
    user_token = db.query(models.UserToken).filter(models.UserToken.token == user_token).first()

    if user_token is None:
        raise HTTPException(detail="Invalid Username or Password", status_code=400)

    if user_token.user_type == 0:
        user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_token.user_id).first()

        user_profile.full_name = user_profile_edited.full_name
        user_profile.about = user_profile_edited.about
    else:
        user_profile = db.query(models.OrgProfile).filter(models.OrgProfile.user_id == user_token.user_id).first()

        user_profile.full_name = user_profile_edited.full_name
        user_profile.about = user_profile_edited.about

    db.commit()
    return user_profile


# @app.get("/categories/available")
# def available_categories(user_token: str, db: Session = Depends(get_db)):
#     # categories = db.query(models.Category).filter(mode)


@app.get("/categories/my", response_model=List[schemas.Category])
def my_categories(user_token: str, db: Session = Depends(get_db)):
    user_token: models.UserToken = db.query(models.UserToken).filter(models.UserToken.token == user_token).first()

    if user_token is None:
        raise HTTPException(detail="Invalid Username or Password", status_code=400)

    user = user_token.user
    cats = db.query(models.Category)

    for category in user.categories:
        cats.append(db.query(models.Category).filter(models.Category.id == category).first())

    return cats
