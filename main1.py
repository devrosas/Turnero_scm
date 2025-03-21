import eel
import pygame
import threading
import os
import atexit
from ConfigManager import ConfigManager
from DatabaseManager import DatabaseManager
from personalizationManager import Personalizacion
from ProductsManager import Productos
from ServidorTCP import TCPManager
from TurnoManager import TurnoManager
from ExcelPriceUpdater import ExcelPriceUpdater

FIREFOX_PATH = r"C:\Program Files\Firefox Developer Edition\firefox.exe"

# Inicializar Eel con la carpeta "web"
eel.init("web")

class CarniceriaApp:
    def __init__(self):
        """Inicializa los módulos y configura la aplicación."""
        try:
            print("Inicializando módulos...")
            
            # Inicializar módulos
            self.config_manager = ConfigManager("config.json")
            self.db_manager = DatabaseManager("carniceria.db")
            self.personalizacion = Personalizacion(self.config_manager)
            self.productos = Productos(self.db_manager, self.config_manager)
            # Inicializar TurnoManager con un callback para actualizar la interfaz
            self.turno_manager = TurnoManager(self.config_manager, self.actualizar_interfaz_turno)
            self.tcp_manager = TCPManager(self.turno_manager)
            self.excel_price_updater = ExcelPriceUpdater(self.db_manager)
            
            # Inicializar Pygame para sonidos
            print("Inicializando Pygame...")
            pygame.init()
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Iniciar el servidor TCP en un hilo separado
            print("Iniciando servidor TCP...")
            threading.Thread(target=self.tcp_manager.iniciar_servidor, daemon=True).start()
            
            print("Aplicación inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la aplicación: {e}")
            raise

    # Funciones de ConfigManager
    def obtener_ruta_logo(self):
        return self.config_manager.obtener_ruta_logo()

    def obtener_ruta_fondo(self):
        return self.config_manager.obtener_ruta_fondo()

    def obtener_ruta_sonido(self):
        return self.config_manager.obtener_ruta_sonido()

    def obtener_ruta_banner_mayoreo(self):
        return self.config_manager.obtener_ruta_banner_mayoreo()

    def obtener_ruta_galeria(self):
        return self.config_manager.obtener_ruta_galeria()

    def cargar_configuracion(self):
        return self.config_manager.cargar_configuracion()

    def guardar_configuracion(self, config=None):
        return self.config_manager.guardar_configuracion(config)

    # Funciones de Personalizacion
    def cambiar_logo(self, nombre_archivo, base64_data):
        return self.personalizacion.cambiar_logo(nombre_archivo, base64_data)

    def seleccionar_sonido(self, nombre_archivo, base64_data):
        return self.personalizacion.seleccionar_sonido(nombre_archivo, base64_data)

    def seleccionar_carpeta_galeria(self):
        self.personalizacion.seleccionar_carpeta_galeria()

    def cambiar_fondo(self, nombre_archivo, base64_data):
        return self.personalizacion.cambiar_fondo(nombre_archivo, base64_data)

    # Funciones de ProductsManager
    def cargar_productos(self):
        return self.productos.cargar_productos()

    def actualizar_galeria(self):
        return self.productos.actualizar_galeria()

    def obtener_producto_actual(self):
        return self.productos.obtener_producto_actual()

    def get_precio_3kg(self):
        return self.productos.get_precio_3kg()

    def get_precio_10kg(self):
        return self.productos.get_precio_10kg()

    def get_precio_50kg(self):
        return self.productos.get_precio_50kg()

    # Funciones de ExcelPriceUpdater
    def actualizar_precios_desde_excel(self, base64_data):
        return self.excel_price_updater.actualizar_precios_desde_excel(base64_data)
    def validar_archivo_excel(self, base64_data):
        """Valida que el archivo Excel tenga las columnas requeridas."""
        return self.excel_price_updater.validar_archivo_excel(base64_data)
    # Funciones de TurnoManager
    def actualizar_turno(self, incremento, bascula_id):
        self.turno_manager.actualizar_turno(incremento, bascula_id)

    def actualizar_turno_a_numero(self, numero, bascula_id):
        self.turno_manager.actualizar_turno_a_numero(numero, bascula_id)

    def obtener_turno_actual(self):
        return self.turno_manager.obtener_turno_actual()

    def reproducir_sonido_turno(self):
        self.turno_manager.reproducir_sonido()

    def mostrar_turno(self, bascula_id):
        self.turno_manager.mostrar_turno(bascula_id)
    
    def actualizar_interfaz_turno(self, turno_actual, bascula_id):
        """
        Callback para actualizar la interfaz web cuando cambia el turno.
        :param turno_actual: Número del turno actual.
        :param bascula_id: ID de la báscula.
        """
        try:
            # Mostrar el overlay en la interfaz web
            eel.actualizarTurnoDesdePython(turno_actual, bascula_id)  # Función en JavaScript
        except Exception as e:
            print(f"Error al actualizar la interfaz del turno: {e}")
    

    # Funciones adicionales de configuración (velocidades)
    def actualizar_velocidad_productos(self, nueva_velocidad):
        self.config_manager.config["velocidad_productos"] = nueva_velocidad
        self.config_manager.guardar_configuracion()

    def actualizar_velocidad_promociones(self, nueva_velocidad):
        self.config_manager.config["velocidad_promociones"] = nueva_velocidad
        self.config_manager.guardar_configuracion()

# Crear instancia de la aplicación
try:
    print("Creando instancia de la aplicación...")
    app = CarniceriaApp()
except Exception as e:
    print(f"Error al inicializar la aplicación: {e}")
    exit(1)

# Cierre de recursos
@atexit.register
def cleanup():
    print("Cerrando recursos...")
    app.db_manager.close()
    pygame.quit()

# Exponer funciones de Python a JavaScript mediante Eel

# ConfigManager
@eel.expose
def obtener_ruta_logo():
    return app.obtener_ruta_logo()

@eel.expose
def obtener_ruta_fondo():
    return app.obtener_ruta_fondo()

@eel.expose
def obtener_ruta_sonido():
    return app.obtener_ruta_sonido()

@eel.expose
def obtener_ruta_banner_mayoreo():
    return app.obtener_ruta_banner_mayoreo()

@eel.expose
def obtener_ruta_galeria():
    return app.obtener_ruta_galeria()

@eel.expose
def cargar_configuracion():
    return app.cargar_configuracion()

@eel.expose
def guardar_configuracion(config):
    return app.guardar_configuracion(config)

# Personalizacion
@eel.expose
def cambiar_logo(nombre_archivo, base64_data):
    return app.cambiar_logo(nombre_archivo, base64_data)

@eel.expose
def seleccionar_sonido(nombre_archivo, base64_data):
    return app.seleccionar_sonido(nombre_archivo, base64_data)

@eel.expose
def seleccionar_carpeta_galeria():
    app.seleccionar_carpeta_galeria()

@eel.expose
def cambiar_fondo(nombre_archivo, base64_data):
    return app.cambiar_fondo(nombre_archivo, base64_data)

# ProductsManager
@eel.expose
def cargar_productos():
    return app.cargar_productos()

@eel.expose
def actualizar_galeria():
    return app.actualizar_galeria()

@eel.expose
def obtener_producto_actual():
    return app.obtener_producto_actual()

@eel.expose
def get_precio_3kg():
    return app.get_precio_3kg()

@eel.expose
def get_precio_10kg():
    return app.get_precio_10kg()

@eel.expose
def get_precio_50kg():
    return app.get_precio_50kg()

# ExcelPriceUpdater
@eel.expose
def actualizar_precios_desde_excel(base64_data):
    return app.actualizar_precios_desde_excel(base64_data)
@eel.expose
def validar_archivo_excel(base64_data):
    return app.validar_archivo_excel(base64_data)
# TurnoManager
@eel.expose
def actualizar_turno(incremento, bascula_id):
    app.actualizar_turno(incremento, bascula_id)

@eel.expose
def actualizar_turno_a_numero(numero, bascula_id):
    app.actualizar_turno_a_numero(numero, bascula_id)

@eel.expose
def obtener_turno_actual():
    return app.obtener_turno_actual()

@eel.expose
def reproducir_sonido_turno():
    app.reproducir_sonido_turno()

@eel.expose
def mostrar_turno(bascula_id):
    app.mostrar_turno(bascula_id)

@eel.expose
def actualizar_interfaz_turno(turno_actual, bascula_id):
    app.actualizar_interfaz_turno(turno_actual, bascula_id)

# Función para mostrar el overlay en la interfaz web
@eel.expose
def mostrar_overlay_turno(turno_actual, bascula_id):
    """
    Muestra el overlay en la interfaz web con el número de turno y el ID de la báscula.
    :param turno_actual: Número del turno actual.
    :param bascula_id: ID de la báscula.
    """
    eel.mostrarOverlay(turno_actual, bascula_id)  # Función en JavaScript
# Configuración adicional
@eel.expose
def actualizar_velocidad_productos(nueva_velocidad):
    app.actualizar_velocidad_productos(nueva_velocidad)

@eel.expose
def actualizar_velocidad_promociones(nueva_velocidad):
    app.actualizar_velocidad_promociones(nueva_velocidad)

# Ruta de la imagen
@eel.expose
def obtener_ruta_imagen(plu):
    """Obtiene la ruta de la imagen basada en el PLU."""
    try:
        ruta_galeria = os.path.join("web", "images")  # Carpeta de imágenes dentro de "web"
        posibles_nombres = [f"{plu}.png", f"{plu.zfill(6)}.png"]  # Ejemplo: "7.png" o "000007.png"

        for nombre in posibles_nombres:
            ruta_completa = os.path.join(ruta_galeria, nombre)
            if os.path.exists(ruta_completa):
                return os.path.relpath(ruta_completa, "web")  # Ruta relativa a la carpeta "web"

        # Si no se encuentra la imagen, devolver una imagen por defecto
        return os.path.join("images", "default.png")
    except Exception as e:
        print(f"Error al obtener la ruta de la imagen: {e}")
        return None


try:
    print("Iniciando interfaz gráfica...")
    eel.start('index.html', size=(1280, 720))
except Exception as e:
    print(f"Error al iniciar la aplicación Eel: {e}")