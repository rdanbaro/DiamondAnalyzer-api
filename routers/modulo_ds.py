from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from database.database import Session
from services.metas import MetaService
from services.modulo_ds import DS
from services.habitos import HabitoService

import pickle
import zipfile
from io import BytesIO


moduloDs_router = APIRouter()
DB = Session()


@moduloDs_router.get('/sprint_metas/{sprint_id}', tags=['DS_services'], response_model=list[dict])
def get_metas_sprint(sprint_id: int):
    metas = MetaService(DB).get_metas_sprint(sprint_id)
    return JSONResponse(content=jsonable_encoder(metas), status_code=200)


@moduloDs_router.get('/sprint_diamantes_stats/{sprint_id}', tags=['DS_services'], response_model=list[dict])
def get_diamantes_stats_sprint(sprint_id: int):
    stats = DS(DB).get_stats_diamantes(sprint_id)
    return JSONResponse(content=jsonable_encoder(stats), status_code=200)

@moduloDs_router.get('/sprint_diamantes_graf/{sprint_id}', tags=['DS_services'], response_model=list[dict])
def get_diamantes_graf_sprint(sprint_id: int):
    fig1, fig2, fig3, fig4 = DS(DB).get_graf_diamantes(sprint_id)
    
    
    buf1 = BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    
    buf2 = BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    
    buf3 = BytesIO()
    fig3.savefig(buf3, format='png')
    buf3.seek(0)
    
    buf4 = BytesIO()
    fig4.savefig(buf4, format='png')
    buf4.seek(0)
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('figura1.png', buf1.getvalue())
        zip_file.writestr('figura2.png', buf2.getvalue())
        zip_file.writestr('figura3.png', buf3.getvalue())
        zip_file.writestr('figura4.png', buf4.getvalue())
    zip_buffer.seek(0)
    
    return StreamingResponse(zip_buffer, media_type='application/zip', status_code=200)
    
    
@moduloDs_router.get('/sprint_habitos_stats/{sprint_id}', tags=['DS_services'], response_model=list[dict])
def get_habitos_stats_sprint(sprint_id: int):
    stats = DS(DB).get_stats_habitos(sprint_id)
    return JSONResponse(content=jsonable_encoder(stats), status_code=200)


# @moduloDs_router.get('/sprint_habitos_graf/{sprint_id}', tags=['DS_services'], response_model=list[dict])
# def get_habitos_graf_sprint(sprint_id: int):
#     fig1, fig2 = DS(DB).get_graf_habitos(sprint_id)
    
    
#     buf1 = BytesIO()
#     fig1.savefig(buf1, format='png')
#     buf1.seek(0)
    
#     buf2 = BytesIO()
#     fig2.savefig(buf2, format='png')
#     buf2.seek(0)
    

    
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
#         zip_file.writestr('figura1.png', buf1.getvalue())
#         zip_file.writestr('figura2.png', buf2.getvalue())
#     zip_buffer.seek(0)
    
#     return StreamingResponse(zip_buffer, media_type='application/zip', status_code=200)
    
@moduloDs_router.get('/sprint_habitos_graf/{sprint_id}', tags=['DS_services'])
def get_habitos_graf_sprint(sprint_id: int):
    fig1, fig2 = DS(DB).get_graf_habitos(sprint_id)
    
    buf1 = BytesIO()
    pickle.dump(fig1, buf1)
    buf1.seek(0)
    
    buf2 = BytesIO()
    pickle.dump(fig2, buf2)
    buf2.seek(0)
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('figura1.pkl', buf1.getvalue())
        zip_file.writestr('figura2.pkl', buf2.getvalue())
    zip_buffer.seek(0)
    
    return StreamingResponse(zip_buffer, media_type='application/zip', status_code=200)