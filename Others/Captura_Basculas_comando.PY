import socket

def procesar_comando(datos):
    """
    Procesa los datos recibidos y devuelve la acción, el valor (si corresponde) y el identificador de la báscula.
    """
    try:
        # Eliminar los caracteres de inicio (\x02) y fin (\x04)
        datos_limpios = datos[1:-1].decode()
        
        # Extraer el tipo de comando
        tipo_comando = datos_limpios[5:7]  # Los caracteres 6 y 7
        
        # Extraer el identificador de la báscula (por ejemplo, "01", "02", "03")
        bascula_id = datos_limpios[7:9]  # Los caracteres 8 y 9
        
        if tipo_comando == "01":
            return "ARRIBA", None, bascula_id
        elif tipo_comando == "02":
            return "ABAJO", None, bascula_id
        elif tipo_comando == "03":
            # Extraer el valor del turno (los 6 dígitos después del tipo de comando)
            valor_turno = int(datos_limpios[9:15])
            return "ACTUALIZAR", valor_turno, bascula_id
        else:
            return "DESCONOCIDO", None, None
    except Exception as e:
        print(f"Error al procesar comando: {e}")
        return "ERROR", None, None

def servidor_prueba():
    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Enlazar el socket a la dirección y puerto
    server_address = ('0.0.0.0', 9101)  # Escuchar en todas las interfaces, puerto 9101
    print(f"Iniciando servidor en {server_address[0]}:{server_address[1]}...")
    server_socket.bind(server_address)
    
    # Escuchar conexiones entrantes (máximo 5 clientes en espera)
    server_socket.listen(5)
    print("Servidor listo para recibir conexiones...")

    while True:
        # Esperar una conexión
        print("Esperando una conexión...")
        connection, client_address = server_socket.accept()
        try:
            print(f"Conexión establecida con {client_address}")

            # Recibir datos en pequeños bloques
            while True:
                data = connection.recv(1024)  # Recibir hasta 1024 bytes
                if not data:
                    # Si no hay más datos, cerrar la conexión
                    print("No se recibieron más datos. Cerrando conexión.")
                    break

                # Imprimir los datos recibidos en bruto y decodificados
                print(f"Datos recibidos (bytes): {data}")
                try:
                    print(f"Datos recibidos (texto): {data.decode()}")
                except UnicodeDecodeError:
                    print("Los datos no se pueden decodificar como texto. Podrían ser binarios.")

                # Procesar el comando
                accion, valor, bascula_id = procesar_comando(data)
                if accion == "ARRIBA":
                    print(f"Comando: Avanzar turno (Báscula: {bascula_id})")
                elif accion == "ABAJO":
                    print(f"Comando: Retroceder turno (Báscula: {bascula_id})")
                elif accion == "ACTUALIZAR":
                    print(f"Comando: Actualizar turno a {valor} (Báscula: {bascula_id})")
                elif accion == "DESCONOCIDO":
                    print("Comando no reconocido")
                elif accion == "ERROR":
                    print("Error al procesar el comando")

        finally:
            # Cerrar la conexión
            connection.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    servidor_prueba()