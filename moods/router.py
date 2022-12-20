from fastapi import Depends, APIRouter
from moods import schemas
from sqlalchemy.orm import Session
from config import settings
from deps import get_db
from moods import repository as mood_repository
from users import repository as user_repository

from fastapi_jwt_auth import AuthJWT

import requests


router = APIRouter(prefix="/moods")


def get_places(lat, lng):
    PLACES_API_KEY = settings.PLACES_API_KEY
    PLACES_URL = settings.PLACES_URL

    url = f"{PLACES_URL}?apiKey={PLACES_API_KEY}&at={lat},{lng}&pretty"
    desirable_places = requests.get(url)
    if len(desirable_places.json()) > 0:
        # Return the closest place to the location provided
        closest_place = desirable_places.json()
        # We could also filter the amount of data we want to store
        return {"closest_place": closest_place["results"]["items"][0]}
    return {"message": "No places found for this specific location"}


@router.get("/places")
def nearby_places(
        db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    current_user = user_repository.get_user_by_email(db, current_user)
    db_moods = mood_repository.get_specific_moods(db, "happy", current_user.id)

    results = {"items": []}
    for mood in db_moods:
        places = get_places(mood.latitude, mood.longitude)
        mood_dict = vars(mood)
        data = {"mood": mood_dict, "closest_place": places}
        results["items"].append(data)
    return results


@router.post("/", response_model=schemas.MoodResponse)
def create_mood(
    mood_create: schemas.MoodCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    current_user = user_repository.get_user_by_email(db, current_user)
    mood = schemas.MoodResponse(
        latitude=mood_create.latitude,
        longitude=mood_create.longitude,
        mood=mood_create.mood,
        user_id=current_user.id,
    )
    mood_db = mood_repository.create_mood(db, mood_schema=mood)
    return schemas.MoodResponse(
        mood=mood_db.mood,
        latitude=mood_db.latitude,
        longitude=mood_db.longitude,
        user_id=mood_db.user_id,
    )


@router.get("/frequency")
def mood_frequency(
        db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    current_user = user_repository.get_user_by_email(db, current_user)
    mood_db = mood_repository.mood_frequency(db, current_user.id)
    return mood_db
