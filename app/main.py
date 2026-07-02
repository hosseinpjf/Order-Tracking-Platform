from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .db.database import engine
from .db.base import Base
from .middleware.exception_handler import http_exception_handler, general_exception_handler, validation_exception_handler

# from .models.user import User
from .routers.users import router as router_users
from .routers.device_tracking import router as router_device_tracking

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router_users)
app.include_router(router_device_tracking)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)