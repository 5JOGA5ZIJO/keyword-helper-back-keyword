from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)