import unittest
from unittest.mock import patch, MagicMock
from services.diamantes import DiamanteService
from models.sprint import Diamante
import pandas as pd

class TestDiamanteService(unittest.TestCase):
    
    def setUp(self):
        # Crear un objeto db ficticio
        self.db = MagicMock()

        # Crear un objeto DiamanteService con el db ficticio
        self.diamante_service = DiamanteService(self.db)

        # Simular un sprint_id
        self.sprint_id = 1

        # Simular una lista de diamantes para el sprint
        self.diamantes = [
            MagicMock(sprint_id=self.sprint_id),
            MagicMock(sprint_id=self.sprint_id),
            MagicMock(sprint_id=self.sprint_id)
        ]

    def test_get_diamantes(self):
        
        # Ruta del archivo csv de prueba
        ruta = 'ruta_de_prueba.csv'

        # Simular los datos del CSV
        data = {
            'Tarea': ['Tarea1', 'Tarea2', 'Tarea3'],
            'Día': ['11/03/2024', '12/03/2024', '13/03/2024'],
            'Inicio': ['08:00', '09:00', '10:00'],
            'Fin': ['10:00', '11:00', '12:00'],
            'Duración': ['2:00', '2:00', '2:00'],
            'Etiquetas': ['Etiqueta1', 'Etiqueta2', 'Etiqueta3'],
            'Unnamed: 7': ['Valor1', 'Valor2', 'Valor3'],
            'Ganancias': ['Valor4', 'Valor5', 'Valor6']
        }

        # Crear un DataFrame con los datos del CSV
        df = pd.DataFrame(data)

        # Simular la lectura del CSV
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = df

            # Llamar a la función get_diamantes
            diamantes = self.diamante_service.get_diamantes(ruta)

            # Verificar que la función devuelve una lista
            self.assertIsInstance(diamantes, list)

            # Verificar que cada elemento de la lista es un tuple con 6 elementos
            for diamante in diamantes:
                self.assertIsInstance(diamante, tuple)
                self.assertEqual(len(diamante), 6)

            # Verificar que el mock se llamó correctamente
            mock_read_csv.assert_called_once_with(ruta)
            
            
    def test_create_diamante(self):
        

        # Crear un objeto Diamante ficticio
        diamante = MagicMock()

        # Llamar a la función create_diamante
        self.diamante_service.create_diamante(diamante)

        # Verificar que el diamante se agregó al db
        self.db.add.assert_called_once_with(diamante)

        # Verificar que el db se comprometió
        self.db.commit.assert_called_once()
        
        
    def test_get_diamantes_sprint(self):
        

        # Simular la consulta a la base de datos
        self.db.query.return_value.filter.return_value.all.return_value = self.diamantes

        # Llamar a la función get_diamantes_sprint
        diamantes_sprint = self.diamante_service.get_diamantes_sprint(self.sprint_id)

        # Verificar que la función devuelve la lista de diamantes para el sprint
        self.assertEqual(diamantes_sprint, self.diamantes)

        # Verificar que la consulta a la base de datos se realizó correctamente
        self.db.query.assert_called_once_with(Diamante)
        self.db.query.return_value.filter.return_value.all.assert_called_once()