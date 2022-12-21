from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auth_handler import hash_password
from users import schemas, repository

from fastapi_jwt_auth import AuthJWT
from config import Settings

from deps import get_db


router = APIRouter(prefix="/users")


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/login")
def login(
    user: schemas.UserCreate,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    db_user = repository.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.email)
    return {"access_token": access_token}


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user_create: schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    db_user = repository.get_user_by_email(db, email=user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_create.password = hash_password(user_create.password)
    user = repository.create_user(db, user=user_create)

    token = Authorize.create_access_token(subject=user["email"])
    return schemas.UserResponse(
        id=user["id"], email=user["email"], token=token)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = repository.get_user(db, user_id)    
    if user is None:
        return HTTPException(status_code=404, detail="User not found")
    
    return repository.delete_user(db, user_id)