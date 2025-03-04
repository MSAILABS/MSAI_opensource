from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_file = "db/database.db"

SQLALCHEMY_DATABASE_URL = "sqlite:///" + db_file
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# These two functions allow the userprofile and other data to be stored in separate databases by region
def get_base_login_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


get_db = get_base_login_db
