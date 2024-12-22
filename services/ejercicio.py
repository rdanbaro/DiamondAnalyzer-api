from models.sprint import EntrenamientoEjercicio
import pandas as pd

class EjercicioService():
    def __init__(self, db):
        self.db = db
        
    def get_datos_ejercicios(self, ruta):
        df_ejercicios = pd.read_csv(f'{ruta}Ejercicios-Tipos.csv')

        
        # Convertir las columnas del DataFrame a listas usando to_list()
        data = (
        pd.melt(df_ejercicios, var_name='Ejercicios',
                id_vars=['Fecha', 'Ronda', 'Rutina'], 
                value_name='Repeticiones',
                value_vars=df_ejercicios.keys().tolist()[1:-1]
            )    
        )
        data = data.dropna(subset=['Repeticiones'])
        data = data.reindex(columns = ['Fecha','Ejercicios', 'Repeticiones', 'Ronda', 'Rutina'])
        data = data.sort_values(by=['Fecha','Ronda'])
        
        fecha = pd.to_datetime(data['Fecha'], format='%d/%m/%Y').dt.date.tolist()
        ejercicios = data['Ejercicios'].tolist()
        repeticiones = data['Repeticiones'].tolist()
        ronda = data['Ronda'].tolist()
        rutinas = data['Rutina'].tolist()
        
        data = list(zip(fecha, ejercicios, repeticiones, ronda, rutinas))
        return data


    
    def create_ejercicio(self, ejercicio):
        self.db.add(ejercicio)
        self.db.commit()