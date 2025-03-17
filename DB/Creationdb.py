import sqlite3

# Nombre de la base de datos
DB_NAME = "carniceria.db"

# Conexión a la base de datos (se crea si no existe)
def crear_base_de_datos():
    try:
        # Conectar a la base de datos (o crearla si no existe)
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        # Crear la tabla productos con las nuevas columnas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                plu TEXT NOT NULL,
                producto TEXT NOT NULL,
                precio_publico REAL NOT NULL,
                super_precio_50kg REAL NOT NULL,
                mayoreo_3kg REAL NOT NULL,
                mayoreo_10kg REAL NOT NULL,
                mayoreo_50kg REAL NOT NULL
            )
        ''')

        # Insertar los productos con los nuevos precios inventados
        productos = [
            ('LO MÁS VENDIDO', '3', 'BIRRIA', 92.00, 88.00, 85.00, 82.00, 80.00),
            ('LO MÁS VENDIDO', '6', 'BISTEC PICADO M', 92.00, 88.00, 85.00, 82.00, 80.00),
            ('LO MÁS VENDIDO', '0', 'BISTEC REBANADO M', 96.00, 92.00, 89.00, 86.00, 84.00),
            ('LO MÁS VENDIDO', '22', 'PIERNA DE CDO S/HUESO (ENTERA)', 94.00, 90.00, 87.00, 84.00, 82.00),
            ('LO MÁS VENDIDO', '113', 'PIERNA DE CDO S/HUESO EN BISTEC', 94.00, 90.00, 87.00, 84.00, 82.00),
            ('CHORIZOS', '328', 'CHISTORRA', 88.00, 84.00, 81.00, 78.00, 76.00),
            ('CHORIZOS', '327', 'CHORIZO ARGENTINO', 80.00, 76.00, 73.00, 70.00, 68.00),
            ('CHORIZOS', '27', 'CHORIZO ASADERO', 80.00, 76.00, 73.00, 70.00, 68.00),
            ('CHORIZOS', '326', 'CHORIZO PARRILLERO', 80.00, 76.00, 73.00, 70.00, 68.00),
            ('CHORIZOS', '28', 'LONGANIZA', 74.00, 72.00, 70.00, 68.00, 66.00),
            ('CHORIZOS', '98', 'LONGANIZA CAMPESTRE', 80.00, 76.00, 73.00, 70.00, 68.00),
            ('ASADOS', '123', 'ASADO NORTEÑO', 172.00, 170.00, 168.00, 165.00, 162.00),
            ('ASADOS', '126', 'BISTEC DE RES', 158.00, 156.00, 154.00, 152.00, 150.00),
            ('ASADOS', '322', 'DIEZMILLO C/ HUESO', 172.00, 170.00, 168.00, 165.00, 162.00),
            ('ASADOS', '2', 'MARINADA', 100.00, 92.00, 90.00, 88.00, 86.00),
            ('ASADOS', '565', 'PICAÑA MARINADA', 100.00, 92.00, 90.00, 88.00, 86.00),
            ('ASADOS', '215', 'RIB-EYE C/H', 172.00, 170.00, 168.00, 165.00, 162.00),
            ('ASADOS', '216', 'T-BONE', 172.00, 170.00, 168.00, 165.00, 162.00),
            ('ASADOS', '226', 'TUETANO DE RES', 90.00, 86.00, 84.00, 82.00, 80.00),
            ('RES', '317', 'BIRRIA C/HUESO', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('RES', '9', 'COCIDO RES', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('RES', '30', 'HUESO DE RES', 22.00, 20.00, 18.00, 16.00, 14.00),
            ('RES', '10', 'MOLIDA DE RES', 92.00, 88.00, 86.00, 84.00, 82.00),
            ('VÍSCERAS', '51', 'BUCHE DE LINEA', 66.00, 66.00, 64.00, 62.00, 60.00),
            ('VÍSCERAS', '34', 'HIGADO DE RES', 38.00, 36.00, 34.00, 32.00, 30.00),
            ('VÍSCERAS', '44', 'LABIO DE RES', 134.00, 130.00, 128.00, 126.00, 124.00),
            ('VÍSCERAS', '42', 'LENGUA DE CERDO', 70.00, 66.00, 64.00, 62.00, 60.00),
            ('VÍSCERAS', '46', 'MENUDO DE RES', 64.00, 60.00, 58.00, 56.00, 54.00),
            ('VÍSCERAS', '47', 'PATA DE RES', 62.00, 58.00, 56.00, 54.00, 52.00),
            ('VÍSCERAS', '40', 'TRIPA TELECO', 50.00, 46.00, 44.00, 42.00, 40.00),
            ('COCINA FÁCIL', '335', 'BISTEC TAQUERO', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('COCINA FÁCIL', '12', 'CARNE ADOBADA', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('COCINA FÁCIL', '13', 'CARNE AL PASTOR', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('COCINA FÁCIL', '23', 'CHULETA AHUMADA REBANADA', 88.00, 84.00, 82.00, 80.00, 78.00),
            ('COCINA FÁCIL', '134', 'TOCINETA', 102.00, 98.00, 96.00, 94.00, 92.00),
            ('COCINA FÁCIL', '315', 'TROMPO', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('COCINA FÁCIL POLLO', '143', 'ALITAS ADOBADAS', 72.00, 68.00, 66.00, 64.00, 62.00),
            ('COCINA FÁCIL POLLO', '323', 'ARRACHERA DE POLLO', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('COCINA FÁCIL POLLO', '49', 'PECHUGA EMPANIZADA', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('COCINA FÁCIL POLLO', '337', 'PECHUGA A LA MOSTAZA', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('POLLO', '342', 'ALITAS NATURALES', 72.00, 68.00, 66.00, 64.00, 62.00),
            ('POLLO', '324', 'MILANESA DE POLLO', 104.00, 100.00, 98.00, 96.00, 94.00),
            ('POLLO', '48', 'PECHUGA ENTERA', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('POLLO', '566', 'PIERNA DE POLLO', 38.00, 38.00, 36.00, 34.00, 32.00),
            ('POLLO', '596', 'PIERNA Y MUSLO A', 38.00, 38.00, 36.00, 34.00, 32.00),
            ('POLLO', '50', 'PIERNA Y MUSLO DE POLLO', 30.00, 30.00, 28.00, 26.00, 24.00),
            ('PESCADO', '158', 'BASA', 72.00, 68.00, 66.00, 64.00, 62.00),
            ('PESCADO', '159', 'TILAPIA', 116.00, 112.00, 110.00, 108.00, 106.00),
            ('CERDO', '41', 'CABEZA DE CDO', 34.00, 34.00, 32.00, 30.00, 28.00),
            ('CERDO', '17', 'CHAMORRO DE CDO', 56.00, 52.00, 50.00, 48.00, 46.00),
            ('CERDO', '065', 'CHEMIS', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('CERDO', '18', 'COSTILLA DE CDO', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('CERDO', '7', 'CUERO DE CDO', 24.00, 24.00, 22.00, 20.00, 18.00),
            ('CERDO', '19', 'ESPINAZO', 62.00, 58.00, 56.00, 54.00, 52.00),
            ('CERDO', '29', 'HUESO DE CDO', 18.00, 16.00, 14.00, 12.00, 10.00),
            ('CERDO', '21', 'LOMO DE CDO', 98.00, 94.00, 92.00, 90.00, 88.00),
            ('CERDO', '43', 'MANITAS DE CDO', 68.00, 64.00, 62.00, 60.00, 58.00),
            ('CERDO', '11', 'MOLIDA DE CERDO', 94.00, 90.00, 88.00, 86.00, 84.00),
            ('DOÑA CHICHA', '26', 'CHICHARRON PRENSADO', 136.00, 132.00, 130.00, 128.00, 126.00),
            ('DOÑA CHICHA', '60', 'MANTECA CUBETA CH', 140.00, 140.00, 138.00, 136.00, 134.00),
            ('DOÑA CHICHA', '62', 'MANTECA CUBETA GDE', 500.00, 500.00, 480.00, 460.00, 440.00),
            ('DOÑA CHICHA', '402', 'MANTECA GRANEL', 44.00, 44.00, 42.00, 40.00, 38.00),
            ('SOBRE PEDIDO', '072', 'CABEZA DE RES', 68.00, 68.00, 66.00, 64.00, 62.00),
            ('SOBRE PEDIDO', '591', 'PERNIL DE CDO', 62.00, 62.00, 60.00, 58.00, 56.00),
        ]

        # Insertar los productos en la tabla
        cursor.executemany('''
            INSERT INTO productos (categoria, plu, producto, precio_publico, super_precio_50kg, mayoreo_3kg, mayoreo_10kg, mayoreo_50kg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', productos)

        # Guardar los cambios
        conexion.commit()
        print("Base de datos creada y productos insertados correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        # Cerrar la conexión
        if conexion:
            conexion.close()
            print("Conexión a la base de datos cerrada.")


# Ejecutar la función para crear la base de datos
if __name__ == "__main__":
    crear_base_de_datos()