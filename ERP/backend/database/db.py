from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
import os


url="sqlite:///database3.db"
engine = create_engine(url,connect_args={"check_same_thread":False})
sessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
base = declarative_base()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

