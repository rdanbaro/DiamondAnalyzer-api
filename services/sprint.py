from models.sprint import Sprint as SprintModel
from models.sprint import Meta as MetaModel
from models.sprint import Habito as HabitoModel
from models.sprint import Diamante as DiamanteModel
from models.sprint import Entrenamiento as EntrenamientoModel

from services.habitos import HabitoService
from services.metas import MetaService
from services.diamantes import DiamanteService
from services.entreno import EntrenoService

import pandas as pd


class SprintService:
    def __init__(self, db):
        self.db = db

    def get_sprints(self):
        sprints = self.db.query(SprintModel).all()
        return sprints
    
    def create_sprint(self, sprint):
        new_sprint = SprintModel(**sprint.model_dump())
        self.db.add(new_sprint)
        self.db.commit()
        
        
        #Metas
        ruta_metas = sprint.ruta_metas_objetivos
        metas = MetaService(self.db).get_datos_metas(ruta_metas)
        
        for meta in metas:
            new_meta = MetaModel(obj=meta[0], requisito=meta[1], cumplido=meta[2], realizado=meta[3], sprint_id=new_sprint.id)
            MetaService(self.db).create_meta(new_meta)
        
        #Habitos
        ruta_habitos = sprint.ruta_habitos
        habitos = HabitoService(self.db).get_datos_habitos(ruta_habitos)
        
        for habito in habitos:
            new_habito = HabitoModel(habito=habito[0],date=habito[1], realizado=habito[2], sprint_id=new_sprint.id)
            HabitoService(self.db).create_habito(new_habito)
        
        #Diamantes
        ruta_diamantes = sprint.ruta_diamantes
        diamantes = DiamanteService(self.db).get_diamantes(ruta_diamantes)
        
        for diamante in diamantes:
            new_diamante = DiamanteModel(actividad=diamante[0], fecha=diamante[1], inicio=diamante[2], fin=diamante[3], duracion=diamante[4], etiqueta=diamante[5], sprint_id=new_sprint.id)
            DiamanteService(self.db).create_diamante(new_diamante)
        
        #Entrenamientos
        ruta_entrenamiento = sprint.ruta_entrenamiento
        rutinas = EntrenoService(self.db).get_datos_entrenamiento(ruta_entrenamiento)
        
        for rutina in rutinas:
            new_entrenamiento = EntrenamientoModel(rutina=rutina[0], fecha=rutina[1], dificultad=rutina[2], musculos=rutina[3], sprint_id=new_sprint.id)
            EntrenoService(self.db).create_entrenamiento(new_entrenamiento)
        
        return new_sprint
    
    def get_sprint(self, nombre):
        sprint = self.db.query(SprintModel).filter(SprintModel.nombre == nombre).first()
        return sprint