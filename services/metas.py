from models.sprint import Meta
import pandas as pd

class MetaService():
    def __init__(self, db):
        self.db = db
        
        
        
    def get_datos_metas(ruta):
        """
        Funcion que devuelve los datos de metas de un csv.
        Dado un csv, devuelve 4 listas: Objetivos, Requisitos, Logros y Realizados.
        Los Objetivos son los de la columna Pendientes, los Requisitos son los de la columna Requisito, los Logros son los de la columna Cumplido y los Realizados son los de la columna Realizado.
        Los valores de la columna Requisito y Cumplido se reemplazan por 1 o 0 si estan vacios.
        Los valores de la columna Realizado se reemplazan por True o False si estan vacios.

        Parameters
        ----------
        ruta: str
            Ruta del csv que se quiere leer.

        Returns
        -------
        list
            4 listas: Objetivos, Requisitos, Logros y Realizados.
        """
        datos = pd.read_csv(ruta)

        list_objs = [i.strip() for i in list(datos['Pendientes'])]
        list_requisito = list(datos['Requisito'].fillna(1))
        list_cumplido = list(datos['Cumplido'].fillna(0))
        list_realizado = [
            True if i.strip() == 'Yes' else False for i in list(datos['Realizado'])]

        return list_objs, list_requisito, list_cumplido, list_realizado
    
        
    def create_meta(self, meta):
        self.db.add(meta)
        self.db.commit()
        