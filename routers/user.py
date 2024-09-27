from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.user import User as Model_User
from pydantic import BaseModel
from database.database import Session


user_router = APIRouter()

class User(BaseModel):
    username: str
    password: str
    
DB = Session()
    
@user_router.get('/users', tags=['users'], response_model=list[User])
def get_users() -> list[User]:
    usuarios = DB.query(Model_User).all()
    return JSONResponse(content=jsonable_encoder(usuarios), status_code=200)