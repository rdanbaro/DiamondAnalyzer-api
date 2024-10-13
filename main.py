from fastapi import FastAPI
from models.user import User
from database.database import engine, Base, Session
from routers.user import user_router
from routers.auth import auth_router
from routers.sprint import sprint_router
from routers.modulo_ds import moduloDs_router


app = FastAPI()
app.title = "DS API"

Base.metadata.create_all(engine)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(sprint_router)
app.include_router(moduloDs_router)