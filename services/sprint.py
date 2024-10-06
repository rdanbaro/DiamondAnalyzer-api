from models.sprint import Sprint as SprintModel
from models.sprint import Meta as MetaModel
from models.sprint import Habito as HabitoModel

from services.habitos import HabitoService
from services.metas import MetaService

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
        
        ruta_metas = sprint.ruta_metas_objetivos
        objs, reqs, cumplidos, realizados = MetaService.get_datos_metas(ruta_metas)
        
        for i in range(len(objs)):
            new_meta = MetaModel(obj=objs[i], requisito=reqs[i], cumplido=cumplidos[i], realizado=realizados[i], sprint_id=new_sprint.id)
            self.db.add(new_meta)
            self.db.commit()
        
        
        ruta_habitos = sprint.ruta_habitos
        habitos = HabitoService.get_datos_habitos(ruta_habitos)
        
        for habito in habitos:
            new_habito = HabitoModel(habito=habito[0],date=habito[1], realizado=habito[2], sprint_id=new_sprint.id)
            self.db.add(new_habito)
            self.db.commit()
        
        return new_sprint