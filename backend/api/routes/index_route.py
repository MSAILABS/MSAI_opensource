from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def root():
    return {"Message": "Welcome to MSAI LABS API."}


@router.get("/db")
async def check_db(db: Session = Depends(get_db)):
    try:
        # Get all tables present in the database
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        print(tables)
        # Perform a simple query to check if the database is working
        db.execute(text("SELECT 1"))
        return {"Message": "Database is working."}
    except Exception as e:
        return {"Error": str(e)}
