from fastapi import Depends, HTTPException, APIRouter
from moods import schemas
from sqlalchemy.orm import Session
from deps import get_db
from moods import repository as mood_repository
from users import repository as user_repository

from fastapi_jwt_auth import AuthJWT

import googlemaps
import requests
import socket
import json


router = APIRouter(prefix='/moods')

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_user_location():
    ip = get_ip()
    url = f"https://ipapi.co/{ip}/json/"
    location = requests.get(url)
    return location.json()


def get_places(lat, lng):
    API_KEY = "I AM SECRET"
    print(lat, lng)
    url = f"https://places.ls.hereapi.com/places/v1/discover/here?apiKey={API_KEY}&at={lat},{lng}&pretty"
    desirable_places = requests.get(url)
    return desirable_places.json()

    
@router.post("/", response_model=schemas.MoodResponse)
def create_mood(mood_create: schemas.MoodCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    current_user = user_repository.get_user_by_email(db, current_user)
    mood = schemas.MoodResponse(geolocation=mood_create.geolocation, mood=mood_create.mood, \
         user_id = current_user.id)
    mood_db = mood_repository.create_mood(db, mood_schema=mood)
    return schemas.MoodResponse(mood=mood_db.mood, geolocation=mood_db.geolocation, user_id=mood_db.user_id)


@router.get("/places")
def nearby_places(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    location = get_user_location()
    places = get_places(location['latitude'],location['longitude'])
    return places


@router.get("/frequency")
def mood_frequency(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    current_user = user_repository.get_user_by_email(db, current_user)
    mood_db = mood_repository.mood_frequency(db, current_user.id)
    return mood_db
