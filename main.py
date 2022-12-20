from fastapi import FastAPI, Request

from users import models as users_models
from moods import models as moods_models
from database import engine

from users.router import router as users_router
from moods.router import router as moods_router

from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

users_models.Base.metadata.create_all(bind=engine)
moods_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(moods_router)


# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message})
