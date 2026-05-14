from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.REMOTE_DATABASE_URL)
SessionRemote = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_remote_db():
    db = SessionRemote()
    try:
        yield db
    finally:
        db.close()
