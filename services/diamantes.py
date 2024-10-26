from models.sprint import Diamante
import pandas as pd



class DiamanteService():
    def __init__(self, db):
        self.db = db
        
        
    def get_diamantes(self, ruta):
        
        data_raw = pd.read_csv(ruta)
        
        data = (
        data_raw.drop(len(data_raw)-1)
        .drop(columns=['Unnamed: 7', 'Ganancias'])
        )
        data = data.fillna('Ocio')
        
        
        tarea = data['Tarea'].tolist()
        fecha = pd.to_datetime(data['Día'], format='%d/%m/%Y').tolist()
        inicio = pd.to_datetime(data['Día'] + data['Inicio'], format='%d/%m/%Y%H:%M').tolist()
        fin = pd.to_datetime(data['Día'] + data['Fin'], format='%d/%m/%Y%H:%M').tolist()
        duracion = pd.to_timedelta(data['Duración']+':00').apply(lambda x: x.total_seconds()/3600).tolist()
        etiqueta = data['Etiquetas'].tolist()
        
        
        
        data = list(zip(tarea, fecha, inicio, fin, duracion, etiqueta))
        
        return data
    
    def create_diamante(self, diamante : Diamante):
        self.db.add(diamante)
        self.db.commit()
        
        
    def get_diamantes_sprint(self, sprint_id):
        diamantes = self.db.query(Diamante).filter(Diamante.sprint_id == sprint_id).all()
        df = pd.DataFrame(diamantes)
        return diamantes