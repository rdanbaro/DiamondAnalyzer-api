from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database.database import Session
from services.metas import MetaService


moduloDs_router = APIRouter()
DB = Session()



@moduloDs_router.get('/sprint_metas/{sprint_id}', tags=['DS_services'], response_model=list[dict])
def get_metas_sprint(sprint_id: int):
    metas = MetaService(DB).get_metas_sprint(sprint_id)
    return JSONResponse(content=jsonable_encoder(metas), status_code=200)