from sqlalchemy.orm import Session

import moods.models as models, moods.schemas as schemas

def create_mood(db: Session, mood: schemas.Mood):
    db_mood = models.mood(mood=mood.mood, geolocation=mood.geolocation, \
        user_id = 1 )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return {"id": db_mood.id, "email": db_mood.email}