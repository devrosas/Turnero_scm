import unittest
from ServidorTCP import TCPManager
class TestTCPManager(unittest.TestCase):
    def setUp(self):
        # Simulamos un turno_manager (puede ser un mock si es necesario)
        class MockTurnoManager:
            def actualizar_turno(self, delta, bascula_id):
                pass

            def actualizar_turno_a_numero(self, valor, bascula_id):
                pass

        self.tcp_manager = TCPManager(MockTurnoManager())

    def test_procesar_comando_actualizar_turno(self):
        # Caso 1: Actualizar turno (comando "03")
        data = b'\x02D0185030002540200\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ACTUALIZAR")
        self.assertEqual(valor, 254)
        self.assertEqual(bascula_id, "02")

        # Caso 2: Actualizar turno (comando "03")
        data = b'\x02D0185030000520200\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ACTUALIZAR")
        self.assertEqual(valor, 52)
        self.assertEqual(bascula_id, "02")

    def test_procesar_comando_avanzar_turno(self):
        # Caso 1: Avanzar turno (comando "01")
        data = b'\x02D01850101=6\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ARRIBA")
        self.assertIsNone(valor)
        self.assertEqual(bascula_id, "01")

        # Caso 2: Avanzar turno (comando "01")
        data = b'\x02D01850102=6\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ARRIBA")
        self.assertIsNone(valor)
        self.assertEqual(bascula_id, "02")

    def test_procesar_comando_retroceder_turno(self):
        # Caso 1: Retroceder turno (comando "02")
        data = b'\x02D01850201=7\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ABAJO")
        self.assertIsNone(valor)
        self.assertEqual(bascula_id, "01")

        # Caso 2: Retroceder turno (comando "02")
        data = b'\x02D01850202=7\x04'
        accion, valor, bascula_id = self.tcp_manager.procesar_comando(data)
        self.assertEqual(accion, "ABAJO")
        self.assertIsNone(valor)
        self.assertEqual(bascula_id, "02")

if __name__ == "__main__":
    unittest.main()