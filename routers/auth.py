from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.database import Session
from models.user import User as Model_User
from routers.user import User

auth_router = APIRouter()
DB = Session()


@auth_router.post("/register", tags=["autenticacion"], response_model=dict, status_code=201)
def register(user: User):
    new_user = Model_User(**user.model_dump())
    DB.add(new_user)
    DB.commit()
    return JSONResponse(status_code=201, content="Usuario creado")