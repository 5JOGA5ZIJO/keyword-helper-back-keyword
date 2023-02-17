from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chatgpt
from chatgpt import chatGPT

app=FastAPI()

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

@app.get("/getdb")
async def get_db(db:Session=Depends(get_db)):
    return db.query(models.Test).all()

@app.get('/')
async def hello():
    return 'dd'

@app.post('/chatgpt')
async def get_summary(prompt : str):
    prompt = '다음 대화를 키워드 3개로 요약해줘' + prompt
    return chatGPT(prompt).strip()



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)