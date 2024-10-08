from models.sprint import Diamante
import pandas as pd



class DiamanteService():
    def __init__(self, db):
        self.db = db
        
        
    def get_diamantes(ruta):
        
        data_raw = pd.read_csv(ruta)
        
        data = (
        data_raw.drop(len(data_raw)-1)
        .drop(columns=['Unnamed: 7', 'Ganancias', 'Duración'])
        )
        data = data.fillna('Ocio')
        
        
        tarea = data['Tarea'].tolist()
        fecha = pd.to_datetime(data['Día'], format='%d/%m/%Y').tolist()
        inicio = pd.to_datetime(data['Día'] + data['Inicio'], format='%d/%m/%Y%H:%M').tolist()
        fin = pd.to_datetime(data['Día'] + data['Fin'], format='%d/%m/%Y%H:%M').tolist()
        #duracion = pd.to_timedelta(data['Duración']+':00').tolist()
        etiqueta = data['Etiquetas'].tolist()
        
        
        
        data = list(zip(tarea, fecha, inicio, fin, etiqueta))
        
        return data
    
    def create_diamante(self, diamante : Diamante):
        self.db.add(diamante)
        self.db.commit()
        