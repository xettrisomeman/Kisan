from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_database():
    Base.metadata.create_all(bind=engine)
