from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = "postgres"
PASSWORD = "j@Hd#pW4"
HOST = "localhost"
PORT = "5432"
DATABASE = "blog"

encoded_password = quote_plus(PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{encoded_password}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
