from sqlalchemy.orm import Session

from moods.models import Mood
from moods.schemas import MoodResponse


def create_mood(db: Session, mood_schema: MoodResponse):
    db_mood = Mood(mood=mood_schema.mood, geolocation=mood_schema.geolocation, \
        user_id = mood_schema.user_id )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return db_mood
