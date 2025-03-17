// js/modules/ProductosManager.js
import { ConfigManager } from './ConfigManager.js';

export class ProductosManager {
    constructor() {
        this.productos = []; // Lista de productos
        this.promociones = []; // Lista de promociones
        this.indiceProductoActual = 0; // Índice del producto actual en la tabla
        this.indicePromocionActual = 0; // Índice de la promoción actual
        this.configManager = new ConfigManager("config.json"); // Instancia de ConfigManager
        this.iniciarActualizacionProductos();
        this.iniciarActualizacionPromociones();
    }

    // Cargar productos desde Python
    async cargarProductos() {
        try {
            console.log("Cargando productos desde Python..."); // Depuración
            this.productos = await eel.cargar_productos()();
            console.log("Productos cargados:", this.productos); // Depuración
            this.actualizarTablaProductos();
        } catch (error) {
            console.error("Error al cargar productos:", error);
        }
    }

    // Cargar promociones desde Python
    async cargarPromociones() {
        try {
            console.log("Cargando promoción desde Python..."); // Depuración
            const promocion = await eel.obtener_producto_actual()();
            console.log("Promoción recibida:", promocion); // Depuración

            if (promocion) {
                this.promociones = [promocion]; // Guardar la promoción en una lista
                this.actualizarPromocion();
            } else {
                console.error("No se pudo cargar la promoción.");
            }
        } catch (error) {
            console.error("Error al cargar promociones:", error);
        }
    }

    // Actualizar la tabla de productos cada 10 segundos
    iniciarActualizacionProductos() {
        setInterval(async () => {
            console.log("Actualizando tabla de productos..."); // Depuración
            await this.cargarProductos();
            this.indiceProductoActual = (this.indiceProductoActual + 1) % this.productos.length;
            this.actualizarTablaProductos();
        }, 10000); // 10 segundos
    }

    // Actualizar la promoción cada 5 segundos
    iniciarActualizacionPromociones() {
        setInterval(async () => {
            console.log("Actualizando promoción..."); // Depuración
            await this.cargarPromociones();
            this.indicePromocionActual = (this.indicePromocionActual + 1) % this.promociones.length;
            this.actualizarPromocion();
        }, 5000); // 5 segundos
    }

     // Actualizar la tabla de productos en el HTML
     actualizarTablaProductos() {
        const tablaProductos = document.getElementById("tabla-productos");
        if (tablaProductos) {
            tablaProductos.innerHTML = ""; // Limpiar la tabla

            // Ordenar los productos alfabéticamente por nombre
            const productosOrdenados = this.productos.slice().sort((a, b) => a[0].localeCompare(b[0]));

            // Mostrar los productos en dos columnas
            for (let i = 0; i < productosOrdenados.length; i++) {
                const producto = productosOrdenados[i];

                // Crear una celda para el producto
                const celda = document.createElement("div");
                celda.className = "celda";

                // Nombre del producto
                const nombreProducto = document.createElement("div");
                nombreProducto.className = "nombre-producto";
                nombreProducto.textContent = producto[0]; // Nombre del producto

                // Precio del producto
                const precioProducto = document.createElement("div");
                precioProducto.className = "precio-producto";
                precioProducto.textContent = `$${producto[1].toFixed(2)}`; // Precio formateado

                // Agregar nombre y precio a la celda
                celda.appendChild(nombreProducto);
                celda.appendChild(precioProducto);

                // Agregar la celda a la tabla
                tablaProductos.appendChild(celda);
            }
        }
    }

    // Crear una celda de producto
    crearCeldaProducto(producto) {
        const celda = document.createElement("div");
        celda.className = "celda";

        // Nombre del producto
        const nombreProducto = document.createElement("div");
        nombreProducto.className = "nombre-producto";
        nombreProducto.textContent = producto[0]; // Nombre del producto

        // Precio del producto
        const precioProducto = document.createElement("div");
        precioProducto.className = "precio-producto";
        precioProducto.textContent = `$${producto[1].toFixed(2)}`; // Precio formateado

        // Agregar nombre y precio a la celda
        celda.appendChild(nombreProducto);
        celda.appendChild(precioProducto);

        return celda;
    }

    // Actualizar la promoción en el HTML
    async actualizarPromocion() {
        const promocion = this.promociones[this.indicePromocionActual];
        if (!promocion) {
            console.error("No hay promoción disponible.");
            return;
        }

        console.log("Actualizando promoción en la interfaz:", promocion); // Depuración

        // Actualizar el nombre del producto
        const tituloPromocion = document.getElementById("titulo-promocion");
        if (tituloPromocion) {
            tituloPromocion.textContent = promocion.producto; // Cambiado de nombre_producto a producto
        }

        // Actualizar la imagen del producto
        const imagenProducto = document.getElementById("imagen-producto");
        if (imagenProducto) {
            // Obtener la ruta de la imagen desde Python
            const rutaImagen = await eel.obtener_ruta_imagen(promocion.plu)();
            if (rutaImagen) {
                imagenProducto.src = rutaImagen; // Ruta relativa servida por Eel
            } else {
                console.error("No se pudo obtener la ruta de la imagen.");
            }
        }

        // Actualizar los precios
        const precioPublico = document.getElementById("precio-entero");
        const precioDecimal = document.getElementById("precio-decimal");
        if (precioPublico && precioDecimal) {
            const [entero, decimal] = promocion.precio_publico.split(".");
            precioPublico.textContent = entero.replace("$", "");
            precioDecimal.textContent = decimal;
        }

        // Actualizar precios de mayoreo
        const precio3kg = document.getElementById("precio-mayoreo-1");
        const precio10kg = document.getElementById("precio-mayoreo-2");
        const precio50kg = document.getElementById("precio-mayoreo-3");
        if (precio3kg && precio10kg && precio50kg) {
            precio3kg.textContent = promocion.mayoreo_3kg.replace("$", "").split(".")[0];
            precio10kg.textContent = promocion.mayoreo_10kg.replace("$", "").split(".")[0];
            precio50kg.textContent = promocion.mayoreo_50kg.replace("$", "").split(".")[0];
        }
    }


    // Verificar si una imagen existe en el servidor
    async verificarExistenciaImagen(ruta) {
        try {
            const response = await fetch(ruta, { method: "HEAD" });
            return response.ok;
        } catch (error) {
            console.error("Error al verificar la existencia de la imagen:", error);
            return false;
        }
    }
}
