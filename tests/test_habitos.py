import unittest
from unittest.mock import patch, MagicMock
from services.habitos import HabitoService
import pandas as pd

class TestHabitoService(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_get_datos_habitos(self, mock_read_csv):
        # Crear un objeto HabitoService con un db ficticio
        db = None
        habito_service = HabitoService(db)

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
        datos_habitos = habito_service.get_datos_habitos(ruta)

        # Verificar que la función devuelve una lista
        self.assertIsInstance(datos_habitos, list)

        # Verificar que cada elemento de la lista es un tuple con 3 elementos
        for habito in datos_habitos:
            self.assertIsInstance(habito, tuple)
            self.assertEqual(len(habito), 3)

        # Verificar que el mock se llamó correctamente
        mock_read_csv.assert_called_once_with(ruta)
        
    

    
    def test_create_habito(selfb):
        # Crear un objeto HabitoService con un db ficticio
        habito_service = HabitoService(None)

        # Simular un habito
        habito = MagicMock()

        # Reemplazar el atributo db en la instancia de HabitoService
        with patch.object(habito_service, 'db') as mock_db:
            # Llamar a la función create_habito
            habito_service.create_habito(habito)

            # Verificar que el habito se agregó al db
            mock_db.add.assert_called_once_with(habito)

            # Verificar que el db se comprometió
            mock_db.commit.assert_called_once()
