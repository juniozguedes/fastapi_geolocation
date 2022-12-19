from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from users import schemas, repository
from database import SessionLocal
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = repository.create_user(db, user=user)
    return schemas.UserResponse(id=user['id'], email=user['email'])
