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
from routers import users_router, chatgpt_router, chats_router
from dotenv import load_dotenv
import os
import requests

# 환경변수 가져오기
load_dotenv()
_VITE_NAVER_CLIENT_ID = os.environ.get("VITE_NAVER_CLIENT_ID")
_VITE_NAVER_CLIENT_SECRET = os.environ.get("VITE_NAVER_CLIENT_SECRET")
# Router
app=FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.include_router(users_router.router)
app.include_router(chatgpt_router.router)
app.include_router(chats_router.router)



# 백과사전 API 요청 URL
naver_api_url = "https://openapi.naver.com/v1/search/encyc.json"

# 백과사전 검색 기능을 제공하는 API를 호출하는 함수
def search_naver_encyclopedia(keyword):
    headers = {
        'X-Naver-Client-Id': _VITE_NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': _VITE_NAVER_CLIENT_SECRET
    }
    params = {
        'query': keyword
    }
    response = requests.get(naver_api_url, headers=headers, params=params)
    return response.json()

# 검색 API 엔드포인트
@app.get("/search")
async def search(keyword: str):
    result = search_naver_encyclopedia(keyword)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

