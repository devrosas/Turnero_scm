import unittest
from unittest.mock import MagicMock
from TurnoManager import TurnoManager

class TestTurnoManager(unittest.TestCase):
    def setUp(self):
        # Crear un mock para el callback de actualización de interfaz
        self.callback_mock = MagicMock()
        self.turno_manager = TurnoManager(callback_actualizar_interfaz=self.callback_mock)

    def test_actualizar_turno_incremento(self):
        # Incrementar el turno
        self.turno_manager.actualizar_turno(1, "02")
        self.assertEqual(self.turno_manager.obtener_turno_actual(), 2)
        self.callback_mock.assert_called_once_with(2, "02")

    def test_actualizar_turno_decremento(self):
        # Decrementar el turno
        self.turno_manager.actualizar_turno(-1, "02")
        self.assertEqual(self.turno_manager.obtener_turno_actual(), 1)
        self.callback_mock.assert_called_once_with(1, "02")

    def test_actualizar_turno_a_numero(self):
        # Actualizar el turno a un número específico
        self.turno_manager.actualizar_turno_a_numero(5, "02")
        self.assertEqual(self.turno_manager.obtener_turno_actual(), 5)
        self.callback_mock.assert_called_once_with(5, "02")

    def test_actualizar_turno_a_numero_invalido(self):
        # Intentar actualizar el turno con un número inválido
        with self.assertRaises(ValueError):
            self.turno_manager.actualizar_turno_a_numero("no_es_un_numero", "02")

if __name__ == "__main__":
    unittest.main()