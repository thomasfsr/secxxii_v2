import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Numeric
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
dbname = os.getenv('POSTGRES_DB')

DATABASE_URL = f'postgresql://{user}:{password}@localhost:5432/{dbname}'

def db_session(url:str=DATABASE_URL):
    engine = create_engine(url=url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal