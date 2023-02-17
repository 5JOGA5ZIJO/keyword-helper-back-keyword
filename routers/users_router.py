from fastapi import APIRouter
from fastapi import FastAPI, Depends
import models, schemas
from datetime import datetime, timedelta
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re


router = APIRouter(
    prefix="/users",
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/", tags=["users"])
async def get_all_users(db:Session=Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/filter_by_id", tags=["users"])
async def get_user_by_id(user_id: str, db:Session=Depends(get_db)):
    login_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    return login_user.last_chat_id

@router.get("/get_nickname_by_id", tags=["users"])
async def get_user_by_id(user_id: str, db:Session=Depends(get_db)):
    login_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    return login_user.nickname

@router.post("/create", tags=['users'])
async def create_user(request:schemas.Users,db:Session=Depends(get_db)):
    new_user = models.Chats(id=request.id, nickname=request.nickname,chat=request.chat,last_chat_id=request.last_chat_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user