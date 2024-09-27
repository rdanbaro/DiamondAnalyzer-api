from fastapi import FastAPI
from models.user import User
from database.database import engine, Base, Session



app = FastAPI()
app.title = "DS API"

Base.metadata.create_all(engine)
