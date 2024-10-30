from models.sprint import Habito
from services.utiles import convertir_fecha_a_datetime
import pandas as pd


class HabitoService():
    def __init__(self, db):
        self.db = db
        
        
    def get_datos_habitos(self, ruta):
        
        data_raw = pd.read_csv(ruta)
        
        
        data_raw = data_raw.drop(columns=['Day', 'Progress']).set_index('Date')

        data = (
            pd.melt(data_raw, var_name='Habito', value_name='Realizado', ignore_index=False)    
            .reset_index()
        )


        data = data.set_index('Habito')
        data.index.name = 'Habito'
        data = data.sort_values(by='Date')
        data = data.reset_index()
        data.rename(columns = {'Date': 'Fecha'}, inplace = True)
        
        data['Fecha'] = data['Fecha'].apply(convertir_fecha_a_datetime)
        
        habito_list = data['Habito'].tolist()
        fecha_list = data['Fecha'].tolist()
        realizado_list = [True if i == 'Yes' else False for i in list(data['Realizado'])]
        
        data = list(zip(habito_list, fecha_list, realizado_list))
        
        
        return data
        
        
    def create_habito(self, habito):
        self.db.add(habito)
        self.db.commit()
        
    
    def get_habitos_sprint(self, sprint_id):
        habitos = self.db.query(Habito).filter(Habito.sprint_id == sprint_id).all()
        return habitos
