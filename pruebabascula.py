import socket

def enviar_datos(host, puerto, datos):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, puerto))
            s.sendall(datos)
            print(f"Datos enviados: {datos}")
    except Exception as e:
        print(f"Error al enviar datos: {e}")

if __name__ == "__main__":
    servidor_host = "192.168.0.127"  # IP fija del servidor
    servidor_puerto = 9101  # Puerto fijo del servidor
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Avanzar turno")
        print("2. Retroceder turno")
        print("3. Actualizar turno a un número específico")
        print("4. Salir")
        opcion = input("Opción: ")
        
        if opcion == "1":
            bascula_id = input("Ingrese el ID de la báscula (2 dígitos): ")
            datos = f"\x02D01850{bascula_id}01=6\x04".encode()
        elif opcion == "2":
            bascula_id = input("Ingrese el ID de la báscula (2 dígitos): ")
            datos = f"\x02D01850{bascula_id}02=7\x04".encode()
        elif opcion == "3":
            bascula_id = input("Ingrese el ID de la báscula (2 dígitos): ")
            turno = input("Ingrese el número de turno (5 dígitos): ")
            datos = f"\x02D0185030000{turno}{bascula_id}\x04".encode()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")
            continue
        
        enviar_datos(servidor_host, servidor_puerto, datos)
