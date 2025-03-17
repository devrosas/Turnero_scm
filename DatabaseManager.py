import sqlite3

class DatabaseManager:
    TABLE_NAME = "productos"
    COLUMNS = {
        "id": "id",
        "categoria": "categoria",
        "plu": "plu",
        "producto": "producto",
        "precio_publico": "precio_publico",
        "mayoreo_3kg": "mayoreo_3kg",
        "mayoreo_10kg": "mayoreo_10kg",
        "mayoreo_50kg": "mayoreo_50kg",
    }

    def __init__(self, db_name="carniceria.db"):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def create_table(self):
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    {self.COLUMNS["id"]} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {self.COLUMNS["categoria"]} TEXT NOT NULL,
                    {self.COLUMNS["plu"]} TEXT NOT NULL UNIQUE,
                    {self.COLUMNS["producto"]} TEXT NOT NULL,
                    {self.COLUMNS["precio_publico"]} REAL NOT NULL CHECK ({self.COLUMNS["precio_publico"]} >= 0),
                    {self.COLUMNS["mayoreo_3kg"]} REAL CHECK ({self.COLUMNS["mayoreo_3kg"]} >= 0),
                    {self.COLUMNS["mayoreo_10kg"]} REAL CHECK ({self.COLUMNS["mayoreo_10kg"]} >= 0),
                    {self.COLUMNS["mayoreo_50kg"]} REAL CHECK ({self.COLUMNS["mayoreo_50kg"]} >= 0)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def get_products(self):
        """Obtiene todos los productos de la base de datos."""
        try:
            self.cursor.execute(f"SELECT DISTINCT {self.COLUMNS['producto']}, {self.COLUMNS['precio_publico']} FROM {self.TABLE_NAME}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener productos: {e}")
            return []

    def get_promociones(self):
        """Obtiene los productos para promociones."""
        try:
            self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener promociones: {e}")
            return []

    def get_precios_mayoreo(self, columna: str):
        """Obtiene los precios de mayoreo según la columna especificada."""
        if columna not in self.COLUMNS.values():
            print(f"Columna '{columna}' no válida.")
            return []
        try:
            self.cursor.execute(f"SELECT {self.COLUMNS['plu']}, {self.COLUMNS['producto']}, {columna} FROM {self.TABLE_NAME}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener precios de mayoreo: {e}")
            return []

    def actualizar_precio(self, plu, nuevo_precio_publico, nuevo_mayoreo_3kg=None, nuevo_mayoreo_10kg=None, nuevo_mayoreo_50kg=None):
        """Actualiza los precios de un producto en la base de datos."""
        if not isinstance(plu, str) or not plu.strip():
            print("El código PLU debe ser una cadena no vacía.")
            return
        if not isinstance(nuevo_precio_publico, (int, float)) or nuevo_precio_publico < 0:
            print("El precio público debe ser un número positivo.")
            return

        try:
            with self.connection:
                self.connection.execute(
                    f"UPDATE {self.TABLE_NAME} SET {self.COLUMNS['precio_publico']} = ? WHERE {self.COLUMNS['plu']} = ?",
                    (nuevo_precio_publico, plu)
                )

                precios_mayoreo = {
                    self.COLUMNS["mayoreo_3kg"]: nuevo_mayoreo_3kg,
                    self.COLUMNS["mayoreo_10kg"]: nuevo_mayoreo_10kg,
                    self.COLUMNS["mayoreo_50kg"]: nuevo_mayoreo_50kg
                }

                for columna, valor in precios_mayoreo.items():
                    if valor is not None:
                        if not isinstance(valor, (int, float)) or valor < 0:
                            print(f"El precio de {columna} debe ser un número positivo.")
                            continue
                        self.connection.execute(
                            f"UPDATE {self.TABLE_NAME} SET {columna} = ? WHERE {self.COLUMNS['plu']} = ?",
                            (valor, plu)
                        )
            print("Precios actualizados correctamente.")
        except sqlite3.Error as e:
            print(f"Error al actualizar los precios: {e}")

    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada correctamente.")

    def __del__(self):
        """Destructor para asegurar el cierre de la conexión."""
        self.close()
