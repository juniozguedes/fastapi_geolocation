from typing import  Union
from pydantic import BaseModel

class MoodCreate(BaseModel):
    mood: str
    geolocation: str

class MoodResponse(MoodCreate):
    mood: str
    geolocation: str
    user_id: int
