from models.sprint import Entrenamiento
from models.sprint import EntrenamientoEjercicio as EjercicioModel
from services.ejercicio import EjercicioService
import pandas as pd

class EntrenoService():
    def __init__(self, db):
        self.db = db
        
    def get_datos_entrenamiento(self, ruta):
        df_rutinas = pd.read_csv(f'{ruta}Trackeo Entrenamientos.csv')
        
        fecha = pd.to_datetime(df_rutinas['Fecha'], format='%d/%m/%Y').dt.date.tolist()
        rutina = df_rutinas['Title'].tolist()
        dificultad = df_rutinas['Dificultad'].tolist()
        musculos = df_rutinas['Músculos'].tolist()
        
        data = list(zip(rutina,fecha, dificultad, musculos))
    
        return data
    
    def create_entrenamiento(self, entreno, ruta):
        self.db.add(entreno)
        self.db.commit()
        ejercicios = EjercicioService(self.db).get_datos_ejercicios(ruta)
        
        for ejercicio in ejercicios:
            if ejercicio[0] == entreno.fecha:
                new_ejercicio = EjercicioModel(fecha = ejercicio[0], ejercicio=ejercicio[1], repeticiones=ejercicio[2], ronda=ejercicio[3], rutina=ejercicio[4], rutina_id=entreno.id)
                EjercicioService(self.db).create_ejercicio(new_ejercicio)
            else:
                print(f'fecha:{entreno.fecha}', f'ejercicio[0]:{ejercicio[0]}')    
                