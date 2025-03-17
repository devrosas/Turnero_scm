import eel
import pygame
import threading
import os

from ConfigManager import ConfigManager
from DatabaseManager import DatabaseManager
from personalizationManager import Personalizacion
from ProductsManager import Productos
from ServidorTCP import TCPManager
from TurnoManager import TurnoManager
from ExcelPriceUpdater import ExcelPriceUpdater

# Inicializar Eel
eel.init('web')

class CarniceriaApp:
    def __init__(self):
        # Inicializar módulos
        self.config_manager = ConfigManager("config.json")
        self.db_manager = DatabaseManager("carniceria.db")
        self.personalizacion = Personalizacion(self.config_manager)
        self.productos = Productos(self.db_manager, self.config_manager)
        self.turno_manager = TurnoManager(self.config_manager)
        self.tcp_manager = TCPManager(self.turno_manager)
        self.excel_price_updater = ExcelPriceUpdater(self.db_manager)
        
        # Inicializar Pygame para sonidos
        pygame.init()
        pygame.mixer.init()
        
        # Iniciar el servidor TCP en un hilo separado
        threading.Thread(target=self.tcp_manager.iniciar_servidor, daemon=True).start()

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
    

    # Funciones de Personalizacion (personalizationManager)
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

    # Funciones adicionales de configuración (velocidades)
    def actualizar_velocidad_productos(self, nueva_velocidad):
        self.config_manager.config["velocidad_productos"] = nueva_velocidad
        self.config_manager.guardar_configuracion()
    def actualizar_velocidad_promociones(self, nueva_velocidad):
        self.config_manager.config["velocidad_promociones"] = nueva_velocidad
        self.config_manager.guardar_configuracion()

# Crear instancia de la aplicación
app = CarniceriaApp()

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
def guardar_configuracion(config=None):
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

# Configuración adicional
@eel.expose
def actualizar_velocidad_productos(nueva_velocidad):
    app.actualizar_velocidad_productos(nueva_velocidad)
@eel.expose
def actualizar_velocidad_promociones(nueva_velocidad):
    app.actualizar_velocidad_promociones(nueva_velocidad)

#Ruta de la imagen
@eel.expose
def obtener_ruta_imagen(plu):
    """Obtiene la ruta de la imagen basada en el PLU."""
    try:
        ruta_galeria = "images"  # Carpeta de imágenes dentro de "web"
        posibles_nombres = [f"{plu}.png", f"{plu.zfill(6)}.png"]  # Ejemplo: "7.png" o "000007.png"

        for nombre in posibles_nombres:
            ruta_completa = f"{ruta_galeria}/{nombre}"
            if os.path.exists(os.path.join("web", ruta_completa)):
                return ruta_completa  # Ruta relativa a la carpeta "web"

        # Si no se encuentra la imagen, devolver una imagen por defecto
        return f"{ruta_galeria}/default.png"
    except Exception as e:
        print(f"Error al obtener la ruta de la imagen: {e}")
        return None
# Iniciar la aplicación Eel
eel.start('index.html', size=(1280, 720))