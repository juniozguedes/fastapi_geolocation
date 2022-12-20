from sqlalchemy.orm import Session

import users.models as models, users.schemas as schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    query = models.User(email=user.email, password=user.password)
    db.add(query)
    db.commit()
    db.refresh(query)
    return {"id": query.id, "email": query.email}
