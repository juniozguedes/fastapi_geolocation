from fastapi import  FastAPI

from users import models as users_models
from moods import models as moods_models
from database import engine

from users.router import router as users_router
from moods.router import router as moods_router

users_models.Base.metadata.create_all(bind=engine)
moods_models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(users_router)
app.include_router(moods_router)



