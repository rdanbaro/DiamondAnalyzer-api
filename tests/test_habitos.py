import unittest
from unittest.mock import patch, MagicMock
from services.habitos import HabitoService
import pandas as pd

from models.sprint import Habito

class TestHabitoService(unittest.TestCase):
    def setUp(self):
        # Crear un objeto HabitoService con un db ficticio
        self.db = None
        self.habito_service = HabitoService(self.db)

        # Simular un sprint_id
        self.sprint_id = 1

        # Simular habitos para el sprint
        self.habitos = [
            Habito(sprint_id=self.sprint_id, habito='Habito1', date='2022-01-01', realizado=True),
            Habito(sprint_id=self.sprint_id, habito='Habito2', date='2022-01-02', realizado=False),
            Habito(sprint_id=self.sprint_id, habito='Habito3', date='2022-01-03', realizado=True),
        ]
    
    
    

    @patch('pandas.read_csv')
    def test_get_datos_habitos(self, mock_read_csv):
        

        # Simular los datos del CSV
        data = {
            'Date': ['11 de marzo de 2024 1:00', '11 de marzo de 2024 1:00', '11 de marzo de 2024 1:00'],
            'Habito1': ['Yes', 'No', 'Yes'],
            'Habito2': ['No', 'Yes', 'No'],
            'Day': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'Progress': [0, 0, 0]
        }
        mock_read_csv.return_value = pd.DataFrame(data)

        # Ruta del archivo csv de prueba
        ruta = 'ruta_de_prueba.csv'

        # Llamar a la función get_datos_habitos
        datos_habitos = self.habito_service.get_datos_habitos(ruta)

        # Verificar que la función devuelve una lista
        self.assertIsInstance(datos_habitos, list)

        # Verificar que cada elemento de la lista es un tuple con 3 elementos
        for habito in datos_habitos:
            self.assertIsInstance(habito, tuple)
            self.assertEqual(len(habito), 3)

        # Verificar que el mock se llamó correctamente
        mock_read_csv.assert_called_once_with(ruta)
        
    

    
    def test_create_habito(self):
        

        # Simular un habito
        habito = MagicMock()

        # Reemplazar el atributo db en la instancia de HabitoService
        with patch.object(self.habito_service, 'db') as mock_db:
            # Llamar a la función create_habito
            self.habito_service.create_habito(habito)

            # Verificar que el habito se agregó al db
            mock_db.add.assert_called_once_with(habito)

            # Verificar que el db se comprometió
            mock_db.commit.assert_called_once()

    def test_get_habitos_sprint(self):
    
        # Reemplazar el atributo db en la instancia de HabitoService
        with patch.object(self.habito_service, 'db') as mock_db:
            # Agregar los habitos al db
            mock_db.query.return_value.filter.return_value.all.return_value = self.habitos

            # Llamar a la función get_habitos_sprint
            habitos_sprint = self.habito_service.get_habitos_sprint(self.sprint_id)

            # Verificar que se devuelven los habitos correctos
            self.assertEqual(habitos_sprint, self.habitos)

            # Verificar que el db se consultó correctamente
            
            
            mock_db.query.assert_called_once_with(Habito)
            