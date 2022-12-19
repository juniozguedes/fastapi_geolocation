from fastapi import Depends, HTTPException, APIRouter
from moods import schemas
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/moods")
def create_item_for_user():
    return True