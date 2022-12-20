from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    authjwt_secret_key: str = "secret"
    PLACES_API_KEY: str = os.getenv("PLACES_API_KEY", "invalid_places_api_key")
    PLACES_URL: str = os.getenv(
        "PLACES_URL", "https://places.ls.hereapi.com/places/v1/discover/here"
    )

    class Config:
        env_file = ".env"


settings = Settings()
