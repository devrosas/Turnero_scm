import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        """Carga la configuración desde el archivo JSON, o crea una configuración por defecto si no existe o está corrupto."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Error al leer el archivo de configuración. Se usará una configuración por defecto.")
        
        # Configuración por defecto si el archivo no existe o está corrupto
        config = {
            "ruta_galeria": "",
            "ruta_fondo": "",
            "ruta_logo": "",
            "sonido_path": "",
            "ruta_banner": ""
        }
        self.guardar_configuracion(config)
        return config

    def guardar_configuracion(self, config=None):
        """Guarda la configuración en el archivo JSON."""
        if config is None:
            config = self.config
        try:
            with open(self.config_file, "w", encoding="utf-8") as file:
                json.dump(config, file, indent=4)
        except IOError:
            print("Error al guardar el archivo de configuración.")

    def obtener_ruta_logo(self):
        return self.config.get("ruta_logo", "")

    def obtener_ruta_fondo(self):
        return self.config.get("ruta_fondo", "")

    def obtener_ruta_sonido(self):
        return self.config.get("sonido_path", "")
    
    def obtener_ruta_banner_mayoreo(self):
        return self.config.get("ruta_banner", "")

    def obtener_ruta_galeria(self):
        return self.config.get("ruta_galeria", "")
