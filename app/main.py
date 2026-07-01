from fastapi import FastAPI
from .db.database import engine
from .db.base import Base

from app.models.user import User
from app.routers.users import router as router_users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router_users)