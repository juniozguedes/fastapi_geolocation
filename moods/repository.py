from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from moods.models import Mood
from moods.schemas import MoodResponse


def create_mood(db: Session, mood_schema: MoodResponse):
    query = Mood(mood=mood_schema.mood, latitude=mood_schema.latitude, \
        longitude=mood_schema.longitude, user_id = mood_schema.user_id )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def mood_frequency(db: Session, user_id: int):
    subquery = (
        db.query(Mood.user_id, Mood.mood, func.count(Mood.mood))
        .group_by(Mood.user_id, Mood.mood)
        .subquery()
    )

    query = (
        db.query(subquery.c.user_id, subquery.c.mood, subquery.c.count.label("frequency:"))
        .all()
    )

    return query

def get_specific_moods(db: Session, mood_type: str, user_id: int):
    query = db.query(Mood).filter(Mood.user_id == user_id, Mood.mood == mood_type).all()
    return query