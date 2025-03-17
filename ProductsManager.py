import os
import random
from DatabaseManager import DatabaseManager  # Importamos DatabaseManager
from ConfigManager import ConfigManager  # Importamos ConfigManager

class Productos:
    def __init__(self, db_manager, config_manager):
        """
        Inicializa la clase Productos.

        :param db_manager: Instancia de DatabaseManager para obtener productos y promociones.
        :param config_manager: Instancia de ConfigManager para obtener la ruta de la galería.
        """
        self.db_manager = db_manager
        self.config_manager = config_manager
        self.ruta_galeria = os.path.normpath(self.config_manager.obtener_ruta_galeria())  # Normalizar la ruta
        self.pagina_actual = 0  # Para manejar la paginación de productos

    # En tu archivo productosManager.py

    def obtener_producto_actual(self):
        """Obtiene un producto aleatorio con sus detalles."""
        try:
            productos = self.db_manager.get_promociones()
            if not productos:
                return None


            # Seleccionar un producto aleatorio
            producto = random.choice(productos)

            # Devolver los detalles del producto formateados
            return {
                "categoria": str(producto[1]).upper(),  # Convertir a cadena y luego a mayúsculas
                "plu": producto[2],  # PLU (código del producto)
                "producto": str(producto[3]).upper(),  # Nombre del producto en mayúsculas
                "precio_publico": f"${float(producto[4]):.2f}",  # Precio público formateado
                "mayoreo_3kg": f"${float(producto[5]):.2f}",  # Precio mayoreo 3kg formateado
                "mayoreo_10kg": f"${float(producto[6]):.2f}",  # Precio mayoreo 10kg formateado
                "mayoreo_50kg": f"${float(producto[7]):.2f}"   # Precio mayoreo 50kg formateado
            }
        except IndexError:
            return None
        except ValueError as ve:
            return None
        except Exception as e:
            return None
        
    def get_precio(self, tipo_mayoreo):
        """Obtiene el precio de mayoreo para 3kg, 10kg o 50kg."""
        producto_actual = self.obtener_producto_actual()
        return producto_actual.get(tipo_mayoreo, "$0.00") if producto_actual else "$0.00"

    def actualizar_galeria(self):
        """Muestra la imagen del producto junto con sus detalles."""
        try:
            producto_actual = self.obtener_producto_actual()
            if not producto_actual:
                return self._producto_default()

            # Construir la ruta de la imagen usando el PLU
            nombre_imagen = f"{str(producto_actual['plu']).zfill(6)}.png"
            ruta_imagen = os.path.join(self.ruta_galeria, nombre_imagen)

            if not os.path.isfile(ruta_imagen):
                nombre_imagen = "sin-imagen.png"

            return {
                "imagen": f"/images/{nombre_imagen}",
                "nombre_producto": producto_actual["nombre_producto"],
                "precio_publico": producto_actual["precio_publico"],
                "mayoreo_3kg": producto_actual["mayoreo_3kg"],
                "mayoreo_10kg": producto_actual["mayoreo_10kg"],
                "mayoreo_50kg": producto_actual["mayoreo_50kg"]
            }

        except Exception as e:
            return self._producto_default()

    def cargar_productos(self):
        """Carga productos para mostrar en una tabla con paginación."""
        try:
            productos = self.db_manager.get_products()
            productos_ordenados = sorted(productos, key=lambda x: x[0].lower())
            
            productos_por_pagina = 8
            total_paginas = max(1, (len(productos_ordenados) + productos_por_pagina - 1) // productos_por_pagina)

            inicio = self.pagina_actual * productos_por_pagina
            fin = inicio + productos_por_pagina

            self.pagina_actual = (self.pagina_actual + 1) % total_paginas
            return productos_ordenados[inicio:fin]

        except Exception as e:
            return []

    def _producto_default(self):
        """Retorna un producto por defecto en caso de error."""
        return {
            "imagen": "/images/sin-imagen.png",
            "nombre_producto": "SIN PRODUCTO",
            "precio_publico": "$0.00",
            "mayoreo_3kg": "$0.00",
            "mayoreo_10kg": "$0.00",
            "mayoreo_50kg": "$0.00"
        }
