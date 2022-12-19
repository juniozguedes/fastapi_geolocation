from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from users import schemas, repository
from database import SessionLocal

from fastapi_jwt_auth import AuthJWT
from settings import Settings


router = APIRouter()

@AuthJWT.load_config
def get_config():
    return Settings()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/login')
def login(user: schemas.UserCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = repository.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=401,detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.email)
    return {"access_token": access_token}


@router.get('/current')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = repository.create_user(db, user=user)

    token = Authorize.create_access_token(subject=user['email'])
    return schemas.UserResponse(id=user['id'], email=user['email'], token=token)
