from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os
from dotenv import load_dotenv

# 환경변수 가져오기
load_dotenv()
_user = os.environ.get("user")
_password = os.environ.get("password")
_host = os.environ.get("host")
_port = os.environ.get("port")
_database = os.environ.get("database")

# print(__file__) #이 파일의 상대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #이 파일의 절대경로
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]

# DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8"
DB_URL = f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_database}?charset=utf8"

engine = create_engine(
    DB_URL, encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
