import os
import base64
from tkinter import Tk
from tkinter.filedialog import askdirectory
from ConfigManager import ConfigManager  # Importamos ConfigManager

class Personalizacion:
    def __init__(self, config_manager):
        """
        Inicializa la clase Personalizacion con una instancia de ConfigManager.
        """
        self.config_manager = config_manager
        self.sonido_path = self.config_manager.obtener_ruta_sonido()

    def _guardar_archivo(self, carpeta, nombre_archivo, base64_data):
        """Método interno para guardar archivos de imagen/sonido de forma segura."""
        try:
            # Verificar que los datos base64 no estén vacíos
            if not base64_data:
                print("Error: Los datos base64 están vacíos.")
                return None

            # Crear carpeta si no existe
            os.makedirs(carpeta, exist_ok=True)

            # Eliminar prefijo "data:tipo/...;base64," si está presente
            if "," in base64_data:
                base64_data = base64_data.split(",")[1]

            # Decodificar datos Base64
            try:
                bytes_archivo = base64.b64decode(base64_data.strip())
            except Exception as e:
                print(f"Error al decodificar datos base64: {e}")
                return None

            # Verificar que el nombre del archivo sea válido
            if not nombre_archivo or not isinstance(nombre_archivo, str):
                print("Error: El nombre del archivo no es válido.")
                return None

            # Guardar el archivo
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            with open(ruta_archivo, "wb") as f:
                f.write(bytes_archivo)

            print(f"Archivo guardado correctamente en: {ruta_archivo}")
            return ruta_archivo
        except Exception as e:
            print(f"Error al guardar archivo {nombre_archivo}: {e}")
            return None

    def cambiar_logo(self, nombre_archivo, base64_data):
        """Guarda un nuevo logo y actualiza la configuración."""
        print("Cambiando logo...")  # Depuración
        if not nombre_archivo or not base64_data:
            return None

        ruta_logo = self._guardar_archivo("web/images", nombre_archivo, base64_data)
        if ruta_logo:
            self.config_manager.config["ruta_logo"] = f"images/{nombre_archivo}"
            self.config_manager.guardar_configuracion()
            print(f"Logo guardado en: {ruta_logo}")  # Depuración
            return f"images/{nombre_archivo}"
        return None

    def seleccionar_sonido(self, nombre_archivo, base64_data):
        """Guarda un nuevo sonido y actualiza la configuración."""
        print("Cambiando sonido...")  # Depuración
        if not nombre_archivo or not base64_data:
            print("Error: Nombre del archivo o datos base64 no proporcionados.")
            return None

        # Guardar el archivo en la carpeta "web/sounds"
        ruta_sonido = self._guardar_archivo("web/sounds", nombre_archivo, base64_data)
        if ruta_sonido:
            # Obtener la ruta relativa y reemplazar las barras invertidas por barras normales
            ruta_relativa = os.path.relpath(ruta_sonido, "web").replace("\\", "/")
            
            # Actualizar la configuración con la ruta relativa
            self.config_manager.config["sonido_path"] = ruta_relativa
            self.config_manager.guardar_configuracion()
            print(f"Sonido guardado en: {ruta_sonido}")  # Depuración
            return ruta_relativa
        else:
            print("Error: No se pudo guardar el archivo de sonido.")
            return None

    def seleccionar_carpeta_galeria(self):
        """Abre un diálogo para seleccionar una carpeta y guarda la ruta en el JSON de configuración."""
        try:
            # Abrir el diálogo de selección de carpeta
            Tk().withdraw()  # Oculta la ventana principal de tkinter
            ruta_galeria = askdirectory()  # Abre el diálogo de selección de carpeta

            if ruta_galeria:
                print(f"Carpeta seleccionada: {ruta_galeria}")

                # Guardar la ruta en el archivo JSON de configuración
                config = self.config_manager.config
                config["ruta_galeria"] = ruta_galeria  # Actualizar la ruta de la galería
                self.config_manager.guardar_configuracion()

                print("Ruta de galería guardada en config.json.")
                return ruta_galeria
            else:
                print("No se seleccionó ninguna carpeta.")
                return None
        except Exception as e:
            print(f"Error al seleccionar la carpeta de galería: {e}")
            return None

    def cambiar_fondo(self, nombre_archivo, base64_data):
        """Guarda una nueva imagen de fondo y actualiza la configuración."""
        print(" Cambiando fondo...")  # Depuración
        if not nombre_archivo or not base64_data:
            return None

        ruta_fondo = self._guardar_archivo("web/images", nombre_archivo, base64_data)
        if ruta_fondo:
            self.config_manager.config["ruta_fondo"] = f"images/{nombre_archivo}"
            self.config_manager.guardar_configuracion()
            print(f"Fondo guardado en: {ruta_fondo}")  # Depuración
            return f"images/{nombre_archivo}"
        return None
