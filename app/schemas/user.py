from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    phone: str
    password: str