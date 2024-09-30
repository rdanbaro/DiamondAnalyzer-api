from pydantic import BaseModel, Field
from typing import Optional



class Sprint(BaseModel):
    id: int
    nombre: str 
    tipo: str
    ruta_metas_objetivos: str
    ruta_habitos: str 
    ruta_entrenamiento: str
    ruta_diamantes: str

    class Config:
        json_schema_extra = {
            "example": {
                'id': 1,
                "nombre": "nombre de ejemplo",
                "tipo": "Tipo de ejemplo",
                "ruta_metas_objetivos": "ruta de ejemplo",
                "ruta_habitos": "ruta de ejemplo",
                "ruta_entrenamiento": "ruta de ejemplo",
                "ruta_diamantes": "ruta de ejemplo"
            }
        }
     