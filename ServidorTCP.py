import socket
import threading
import logging

class TCPManager:
    def __init__(self, turno_manager):
        self.turno_manager = turno_manager
        self.logger = logging.getLogger(__name__)

    def iniciar_servidor(self):
        """Inicia el servidor TCP en un hilo separado."""
        def manejar_cliente(conn, addr):
            print(f"Conexión establecida con {addr}")
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.procesar_datos(data)
            except (socket.error, ValueError) as e:
                print(f"Error: {e}")
            finally:
                print(f"Conexión cerrada con {addr}")
                conn.close()

        def servidor():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("0.0.0.0", 9101))
            server_socket.listen(5)
            print("Servidor TCP iniciado en el puerto 9101...")
            while True:
                conn, addr = server_socket.accept()
                threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

        threading.Thread(target=servidor, daemon=True).start()

    def procesar_comando(self, datos):
        try:
            # Eliminar STX (\x02) y ETX (\x04)
            datos_limpios = datos[1:-1].decode()

            # Extraer tipo de comando (posiciones 5-6)
            tipo_comando = datos_limpios[5:7]

            if tipo_comando == "03":  # Actualizar turno
                # Extraer valor del turno (posiciones 7-12)
                valor_turno = int(datos_limpios[7:13].lstrip('0') or '0')
                # Extraer ID de la báscula (posiciones 13-14)
                bascula_id = datos_limpios[13:15]
                return "ACTUALIZAR", valor_turno, bascula_id

            elif tipo_comando in ("01", "02"):  # Avanzar o retroceder turno
                # Extraer ID de la báscula (posiciones 7-8)
                bascula_id = datos_limpios[7:9]
                if tipo_comando == "01":
                    return "ARRIBA", None, bascula_id
                else:
                    return "ABAJO", None, bascula_id

            else:
                return "DESCONOCIDO", None, None

        except (ValueError, IndexError, UnicodeDecodeError) as e:
            self.logger.error(f"Error al procesar comando: {e}")
            return "ERROR", None, None

    def procesar_datos(self, data):
        """Procesa los datos recibidos desde el cliente TCP."""
        try:
            if data.startswith(b'\x02') and data.endswith(b'\x04'):
                accion, valor, bascula_id = self.procesar_comando(data)

                if accion == "ARRIBA":
                    print(f"Comando: Avanzar turno (Báscula: {bascula_id})")
                    self.turno_manager.actualizar_turno(1, bascula_id)

                elif accion == "ABAJO":
                    print(f"Comando: Retroceder turno (Báscula: {bascula_id})")
                    self.turno_manager.actualizar_turno(-1, bascula_id)

                elif accion == "ACTUALIZAR":
                    print(f"Comando: Actualizar turno a {valor} (Báscula: {bascula_id})")
                    self.turno_manager.actualizar_turno_a_numero(valor, bascula_id)

                elif accion == "DESCONOCIDO":
                    self.logger.warning("Tipo de comando no reconocido.")

                elif accion == "ERROR":
                    self.logger.error("Error al procesar el comando.")

            else:
                self.logger.warning("Formato de datos no reconocido.")

        except Exception as e:
            self.logger.error(f"Error inesperado al procesar datos: {e}")
