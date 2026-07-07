from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DB_URL = "mysql+pymysql://root:Ngmai2804@localhost/bai1_session11_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
