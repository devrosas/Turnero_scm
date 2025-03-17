# TurnoManager.py
import os
import pygame
import logging
from ConfigManager import ConfigManager
from ServidorTCP import TCPManager

class TurnoManager:
    def __init__(self, config_manager, callback_actualizar_interfaz=None):
        """
        Inicializa el TurnoManager.

        :param config_manager: Instancia de ConfigManager para obtener la ruta del sonido.
        :param callback_actualizar_interfaz: Función para actualizar la interfaz.
        """
        self.turno_actual = 1
        self.callback_actualizar_interfaz = callback_actualizar_interfaz
        self.config_manager = config_manager  # Guardar la instancia de ConfigManager
        self.logger = logging.getLogger(__name__)

        # Inicializar pygame para reproducir sonidos
        pygame.mixer.init()

    def actualizar_turno(self, incremento, bascula_id):
        """
        Actualiza el turno actual.

        :param incremento: Incremento (o decremento) para el turno actual.
        :param bascula_id: Identificador de la báscula.
        """
        try:
            self.turno_actual = max(1, self.turno_actual + incremento)
            self.mostrar_turno(bascula_id)
            self.reproducir_sonido()  # Reproducir sonido al actualizar el turno

            # Notificar a JavaScript que el turno ha cambiado
            if self.callback_actualizar_interfaz:
                self.callback_actualizar_interfaz(self.turno_actual, bascula_id)
        except Exception as e:
            self.logger.error(f"Error al actualizar el turno: {e}")

    def actualizar_turno_a_numero(self, numero, bascula_id):
        """
        Actualiza el turno a un número específico.

        :param numero: Número al que se actualizará el turno.
        :param bascula_id: Identificador de la báscula.
        """
        try:
            self.turno_actual = max(1, int(numero))
            self.mostrar_turno(bascula_id)
            self.reproducir_sonido()  # Reproducir sonido al actualizar el turno

            # Notificar a JavaScript que el turno ha cambiado
            if self.callback_actualizar_interfaz:
                self.callback_actualizar_interfaz(self.turno_actual, bascula_id)
        except (ValueError, TypeError) as e:
            self.logger.error(f"Error al actualizar el turno a un número: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")

    def mostrar_turno(self, bascula_id):
        """
        Devuelve el ID de la báscula y el número de turno actual.

        :param bascula_id: Identificador de la báscula.
        :return: Diccionario con el número de turno y el ID de la báscula.
        """
        return {"turno": self.turno_actual, "bascula_id": bascula_id}

    def obtener_turno_actual(self):
        """
        Devuelve el valor actual del turno.

        :return: Número del turno actual.
        """
        return self.turno_actual

    def reproducir_sonido(self):
        """
        Reproduce un sonido si la ruta al archivo de sonido es válida.
        """
        try:
            # Obtener la ruta del sonido desde ConfigManager
            sonido_path = self.config_manager.obtener_ruta_sonido()

            if not sonido_path:
                self.logger.warning("La ruta del sonido no está configurada.")
                return

            # Asegurarse de que la ruta sea absoluta y esté correctamente formateada
            if not os.path.isabs(sonido_path):
                # Si la ruta es relativa, convertirla a absoluta basada en la carpeta "web"
                sonido_path = os.path.join("web", sonido_path)

            # Verificar si el archivo existe
            if os.path.exists(sonido_path):
                # Cargar y reproducir el sonido
                pygame.mixer.music.load(sonido_path)
                pygame.mixer.music.play()
                self.logger.info(f"Reproduciendo sonido: {sonido_path}")
            else:
                self.logger.warning(f"Archivo de sonido no encontrado: {sonido_path}")
        except Exception as e:
            self.logger.error(f"Error al reproducir el sonido: {e}")