from fastapi import FastAPI, Depends
import models, schemas
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

@app.get('/')
async def hello():
    return 'dd'

@app.get("/getdb")
async def get_db(db:Session=Depends(get_db)):
    return db.query(models.Test).all()

@app.post('/chatgpt')
async def get_summary(prompt : str):
    prompt = '다음 대화를 키워드 3개로 요약하고 리스트 형식으로 출력해줘' + prompt
    return chatGPT(prompt).strip()

@app.post("/adddb")
async def add_db(request:schemas.Test, db:Session=Depends(get_db)):
    new_user = models.Test(name=request.name, age=request.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @app.post("/points")
# async def create_point(request:schemas.Test, db:Session=Depends(get_db)):
#     new_user = models.Test(id=request.id, name=request.name, age=request.age)
#     db.add(new_user)

#     db.commit()
#     db.refresh(new_user)
#     return new_user

@app.post("/points")
async def create_point(request:schemas.Test, db:Session=Depends(get_db)):
    new_user = models.Test(id=request.id, name=request.name, age=request.age)
    db.add(new_user)

    db.commit()
    db.refresh(new_user)
    return new_user

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# from enum import Enum

# app = FastAPI()

# # 기초 Model 사용법
# class Item(BaseModel):
#     name:str
#     price:float
#     is_offer : Union[bool, None] = None

# @app.get("/")
# def read_root():
#     return {"Hello" : "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id : int, q : Union[str, None] = None):
#     return {"item_id":item_id, "q":q}

# @app.put("/items/{item_id}")
# def update_item(item_id:int, item:Item):
#     return {"item_name" : item.name, "item_id":item_id}


# # 심화 Model 사용법
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/models/{model_name}")
# async def get_model(model_name : ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name" : model_name, "msg" : "알렉스넷이다"}
#     if model_name.value == "lenet":
#         return {"model_name" : model_name, "msg" : "르넷이다"}
#     return {"model_name" : model_name, "msg" : "나머지다"}


# # pagination
# fake_items_db = [{"item_name" : "Foo"},{"item_name" : "Bar"},{"item_name" : "Baz"}]
# @app.get("/animals")
# def readt_animals(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:skip + limit]


# # request body(PUT/POST) + path 
# class AA(BaseModel):
#     name: str = Field(default="name", title="name title", max_length=300)
#     desc : Union[str, None] = None
#     price : float
#     tax : Union[float, None] = None

# @app.put("/aa/{item_id}")
# def create_item(item_id:int, item:AA):
#     return {"item_id" : item_id, **item.dict()}
# @app.post("/aa")
# def create_item(item:AA):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax" : price_with_tax})
#     return item_dict



# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)