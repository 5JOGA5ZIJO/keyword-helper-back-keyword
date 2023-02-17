from fastapi import APIRouter
from fastapi import FastAPI, Depends
import models, schemas
from datetime import datetime, timedelta
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chatgpt
from chatgpt import chatGPT
import re
from fastapi import Query

router = APIRouter(
    prefix="/chatgpt",
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.post('/login', tags=['chatgpt'])
async def summary_by_user_id(user_id : str, db:Session=Depends(get_db)):
    login_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    start_id = login_user.last_chat_id
    chat_messages = db.query(models.Chats.chat).filter(models.Chats.id > start_id).all()
    # chat_messages = db.query(models.Chats.chat).filter(models.Chats.id < 11).all()

    chats_list = [chat[0] for chat in chat_messages]
    chats = ', '.join(chats_list)
    prompt = 'return python list type which includes three main keywords of following conversateion. \n' + chats
    # prompt = '다음 대화의 핵심 키워드 3개와, 각각의 키워드와 가장 관련 있는 대화 1개를 json 코드로 출력해줘. ' + chats
    text = chatGPT(prompt).strip()
    pattern = r'\[.*?\]'
    match = re.search(pattern, text)
    if match:
        lst_str = match.group()
        lst = eval(lst_str)
        return lst
    else:
        return "다시 버튼을 눌러주세요"

@router.post('/time', tags=['chatgpt'])
async def summary_by_time(minutes:int=Query(30,gt=0) ,db:Session=Depends(get_db)):
    thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
    chat_messages = db.query(models.Chats.chat).filter(models.Chats.created_at > thirty_minutes_ago).all()
    chats_list = [chat[0] for chat in chat_messages]
    chats = ', '.join(chats_list)

    prompt = 'return python list type which includes three main keywords of following conversateion. \n' + chats
    text = chatGPT(prompt).strip()
    pattern = r'\[.*?\]'
    match = re.search(pattern, text)
    if match:
        lst_str = match.group()
        lst = eval(lst_str)
        return lst
    else:
        return "다시 버튼을 눌러주세요"