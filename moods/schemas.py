from typing import  Union
from pydantic import BaseModel, validator

class MoodCreate(BaseModel):
    mood: str
    latitude: float
    longitude: float

    @validator("latitude")
    def validate_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError("Invalid latitude")
        return value

    @validator("longitude")
    def validate_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError("Invalid longitude")
        return value


class MoodResponse(MoodCreate):
    user_id: int