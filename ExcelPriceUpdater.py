import base64
import tempfile
import os
import pandas as pd

class ExcelPriceUpdater:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _validar_precio(self, precio):
        """
        Valida que el precio sea un número positivo.
        :param precio: Valor a validar.
        :return: Precio validado (float).
        :raises ValueError: Si el precio no es válido.
        """
        try:
            precio = float(precio)  # Convertir a float
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            return precio
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido.")

    def actualizar_precios_desde_excel(self, base64_data):
        try:
            # Decodificar el archivo Base64
            file_data = base64.b64decode(base64_data)

            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name

            try:
                # Leer el archivo Excel
                df = pd.read_excel(temp_file_path)

                # Definir columnas requeridas
                columnas_requeridas = {"PLU", "PRECIO_PUBLICO", "MAYOREO_3KG", "MAYOREO_10KG", "MAYOREO_50KG"}
                
                # Verificar columnas requeridas
                if not columnas_requeridas.issubset(df.columns):
                    return {
                        "status": "error",
                        "message": f"El archivo Excel debe contener las columnas: {', '.join(columnas_requeridas)}."
                    }

                productos_actualizados = []
                errores = []

                # Procesar cada fila del archivo Excel
                for index, fila in df.iterrows():
                    try:
                        # Validar y obtener el PLU
                        plu = str(fila["PLU"]).strip()  # Asegurar que PLU es string
                        if not plu:
                            raise ValueError("PLU vacío.")

                        # Validar y convertir precios
                        precios = {
                            "precio_publico": self._validar_precio(fila["PRECIO_PUBLICO"]),
                            "mayoreo_3kg": self._validar_precio(fila["MAYOREO_3KG"]),
                            "mayoreo_10kg": self._validar_precio(fila["MAYOREO_10KG"]),
                            "mayoreo_50kg": self._validar_precio(fila["MAYOREO_50KG"])
                        }

                        # Actualizar la base de datos
                        self.db_manager.actualizar_precio(
                            plu=plu,
                            nuevo_precio_publico=precios["precio_publico"],
                            nuevo_mayoreo_3kg=precios["mayoreo_3kg"],
                            nuevo_mayoreo_10kg=precios["mayoreo_10kg"],
                            nuevo_mayoreo_50kg=precios["mayoreo_50kg"]
                        )

                        productos_actualizados.append((plu, precios["precio_publico"]))

                    except Exception as e:
                        errores.append(f"Fila {index + 2}: {e}")  # +2 porque Excel comienza en 1 y la fila 1 es el encabezado

                # Retornar resultado con productos actualizados y errores (si los hay)
                mensaje = "Los precios se actualizaron correctamente."
                if errores:
                    mensaje += f" Errores encontrados: {', '.join(errores)}"

                return {
                    "status": "success",
                    "message": mensaje,
                    "productos": productos_actualizados,
                    "errores": errores
                }

            finally:
                # Asegurar eliminación del archivo temporal
                os.remove(temp_file_path)

        except Exception as e:
            return {"status": "error", "message": f"No se pudo actualizar los precios: {e}"}

    def validar_archivo_excel(self, base64_data):
        """Valida que el archivo Excel tenga las columnas requeridas."""
        try:
            # Decodificar el archivo Base64
            file_data = base64.b64decode(base64_data)

            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name

            try:
                # Leer el archivo Excel
                df = pd.read_excel(temp_file_path)

                # Definir columnas requeridas
                columnas_requeridas = {"PLU", "PRECIO_PUBLICO", "MAYOREO_3KG", "MAYOREO_10KG", "MAYOREO_50KG"}
                
                # Verificar columnas requeridas
                if not columnas_requeridas.issubset(df.columns):
                    return {
                        "status": "error",
                        "message": f"El archivo Excel debe contener las columnas: {', '.join(columnas_requeridas)}."
                    }

                return {
                    "status": "success",
                    "message": "El archivo Excel es válido."
                }

            finally:
                # Asegurar eliminación del archivo temporal
                os.remove(temp_file_path)

        except Exception as e:
            return {"status": "error", "message": f"No se pudo validar el archivo Excel: {e}"}