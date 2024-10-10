from models.sprint import Entrenamiento
import pandas as pd

class EntrenoService():
    def __init__(self, db):
        self.db = db
        
    def get_datos_entrenamiento(ruta):
        df = pd.read_csv(ruta)
        
        fecha = pd.to_datetime(df['Fecha'], format='%d/%m/%Y').tolist()
        rutina = df['Title'].tolist()
        dificultad = df['Dificultad'].tolist()
        musculos = df['Músculos'].tolist()
        
        data = list(zip(rutina,fecha, dificultad, musculos))
    
        return data
    
    def create_entrenamiento(self, entreno):
        self.db.add(entreno)
        self.db.commit()