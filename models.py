from sqlalchemy import Boolean, Column, Integer, String
from database import Base
# models는 진짜 DB의 구조여야 함.
# schemas는 클라이언트가 서버로 보내는 요청의 모양이 맞는지 확인하는 용도임.
class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)