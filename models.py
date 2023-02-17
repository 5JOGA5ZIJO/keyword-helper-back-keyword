# from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from database import Base
# import datetime
# # models는 진짜 DB의 구조여야 함.
# # schemas는 클라이언트가 서버로 보내는 요청의 모양이 맞는지 확인하는 용도임.

# class Users(Base):
#     __tablename__="users"

#     id = Column(String(255), primary_key=True)
#     nickname = Column(String(255),unique=True, nullable=False)
#     last_chat_id = Column(Integer, ForeignKey("chats.id"))
    
#     a = relationship("Chats", back_populates="B")


# class Chats(Base):
#     __tablename__="chats"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(String(255), ForeignKey("users.id"))
#     chat = Column(String(255), nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)

#     b = relationship("Users", back_populates="A")


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# class Users(Base):
#     __tablename__ = 'users'

#     id = Column(String(255), primary_key=True)
#     nickname = Column(String(255), unique=True, nullable=False)
#     last_chat_id = Column(Integer, ForeignKey('chats.id'))
#     last_chat = relationship("Chats", back_populates="users",)

# class Chats(Base):
#     __tablename__ = 'chats'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(String(255), ForeignKey('users.id'))
#     user = relationship("Users", back_populates="chats")
#     chat = Column(String(255), nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Users.chats = relationship("Chats", order_by=Chats.id, back_populates="user")
# Chats.users = relationship("Users", order_by=Users.id, back_populates="last_chat")

class Users(Base):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True)
    nickname = Column(String(255), unique=True, nullable=False)
    last_chat_id = Column(Integer)

class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    chat = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)