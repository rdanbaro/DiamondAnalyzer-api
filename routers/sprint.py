from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database.database import Session
from schema.sprint import Sprint
from services.sprint import SprintService


sprint_router = APIRouter()
DB = Session()



@sprint_router.post('/sprints/', tags=['sprints'], response_model=dict)
def create_sprint(sprint: Sprint) -> dict:
   
    new_sprint = SprintService(DB).create_sprint(sprint)
    
    
    return JSONResponse(content={'message': 'Sprint Creado'}, status_code=201) 

@sprint_router.get('/sprints/{nombre}', tags=['sprints'], response_model=Sprint)
def get_sprint(nombre: str):
    sprint = SprintService(DB).get_sprint(nombre)
    return JSONResponse(content=jsonable_encoder(sprint), status_code=200)