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
    prefix="/chats",
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", tags=['chats'])
async def get_all_chats(db:Session=Depends(get_db)):
    return db.query(models.Chats).all()

@router.post("/create", tags=['chats'])
async def create_chat(request:schemas.Chats,db:Session=Depends(get_db)):
    new_chat = models.Chats(id=request.id, user_id=request.user_id,chat=request.chat,created_at=request.created_at)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat

@router.get("/filter_by_keyword", tags=['chats'])
async def get_chats_by_keyword(keyword:str, db:Session=Depends(get_db)):
    chat_messages = db.query(models.Chats.chat).filter(models.Chats.chat.contains(keyword)).all()
    chats_list = [chat[0] for chat in chat_messages]
    return chats_list

# @router.get("/getdb/filter_by_id", tags=['chats'])
# async def get_db_chats_filter_by_id(start_id: int, db:Session=Depends(get_db)):
#     return db.query(models.Chats).filter(models.Chats.id > start_id).all()

# @router.get("/getdb/filter_by_timestamp", tags=['chats'])
# async def get_db_chats_filter_by_timestamp(db:Session=Depends(get_db)):
#     thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
#     chat_messages = db.query(models.Chats.chat).filter(models.Chats.created_at > thirty_minutes_ago).all()
#     chats_list = [chat[0] for chat in chat_messages]
#     chats = ', '.join(chats_list)

#     return chats