import unittest
from unittest.mock import Mock, patch
from models.sprint import Entrenamiento, EntrenamientoEjercicio
from services.ejercicio import EjercicioService
from services.entreno import EntrenoService
import pandas as pd
from datetime import date

class TestEntrenamientoService(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.sprint_id = 1
        self.entreno_service = EntrenoService(self.db)
        self.ruta = "C:\\Users\\User\\Downloads\\Datos de Entreno Notion\\"

    def test_get_datos_entrenamiento(self):
        data = {
            'Fecha': ['11/03/2024', '12/03/2024'],
            'Title': ['Rutina1', 'Rutina2'],
            'Dificultad': ['Alta', 'Media'],
            'Músculos': ['Pierna', 'Brazo']
        }
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame(data)
            resultado = self.entreno_service.get_datos_entrenamiento(self.ruta)
            
            self.assertIsInstance(resultado, list)
            self.assertEqual(len(resultado), 2)
            self.assertEqual(len(resultado[0]), 4)

    def test_create_entrenamiento(self):
        entreno_mock = Mock(spec=Entrenamiento, id=1, fecha=date(2024, 3, 11))
        ejercicios_data = [(date(2024, 3, 11), 'Ejercicio1', 10, 1, 'Rutina1')]
        
        with patch('services.ejercicio.EjercicioService') as ejercicio_service_mock:
            ejercicio_service_mock.return_value.get_datos_ejercicios.return_value = ejercicios_data
            
            self.entreno_service.create_entrenamiento(entreno_mock, self.ruta)
            
            self.db.add.assert_called_once_with(entreno_mock)
            self.db.commit.assert_called_once()
            
    def test_get_entrenamientos_sprint(self):
    # Mock de entrenamientos
        entrenamientos_mock = [
            Mock(spec=Entrenamiento, id=1),
            Mock(spec=Entrenamiento, id=2),
            Mock(spec=Entrenamiento, id=3)
        ]
        
        # Mock de ejercicios
        ejercicios_mock = [
            Mock(spec=EntrenamientoEjercicio, rutina_id=1, ejercicio="Sentadillas", repeticiones=10),
            Mock(spec=EntrenamientoEjercicio, rutina_id=1, ejercicio="Peso Muerto", repeticiones=8),
            Mock(spec=EntrenamientoEjercicio, rutina_id=2, ejercicio="Flexiones", repeticiones=15),
            Mock(spec=EntrenamientoEjercicio, rutina_id=2, ejercicio="Dominadas", repeticiones=12),
            Mock(spec=EntrenamientoEjercicio, rutina_id=3, ejercicio="Press Banca", repeticiones=10),
            Mock(spec=EntrenamientoEjercicio, rutina_id=3, ejercicio="Remo", repeticiones=12)
        ]
        
        # Configurar mock de base de datos
        self.db.query.return_value.filter.return_value.all.return_value = entrenamientos_mock
        
        # Mock del EjercicioService
        mock_ejercicio_service = Mock()
        mock_ejercicio_service.get_ejercicios_rutina = Mock(return_value=ejercicios_mock)
        
        # Patch del constructor de EjercicioService
        with patch('services.entreno.EjercicioService', return_value=mock_ejercicio_service):
            entrenamientos, ejercicios = self.entreno_service.get_entrenamientos_sprint(self.sprint_id)
            
            self.assertEqual(len(entrenamientos), 3)
            self.assertEqual(len(ejercicios), 6)
