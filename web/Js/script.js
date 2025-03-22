import { ConfigManager } from './modules/ConfigManager.js';
import { ProductosManager } from './modules/ProductosManager.js';
import {turnoManager} from './modules/turnomanager.js'

// Inicializar los módulos
const configManager = new ConfigManager();
const productosManager = new ProductosManager();
// Función para inicializar la aplicación
function inicializarAplicacion() {
    console.log("Inicializando aplicación...");

    // Cargar la configuración inicial (fondo, logo, sonido, etc.)
    configManager.cargarConfiguracionInicial();

    // Cargar productos y promociones
    productosManager.cargarProductos();
    productosManager.cargarPromociones();

    // Configurar eventos de la interfaz
    configurarEventos();
}
// Función para manejar la actualización del turno desde Python
function actualizarTurnoDesdePython(turnoActual, basculaId) {
    console.log(`Turno actualizado: ${turnoActual}, Báscula: ${basculaId}`);
    
    // Actualizar la interfaz normal
    turnoManager.actualizarInterfaz(turnoActual, basculaId);
    
    // Mostrar el overlay
    turnoManager.mostrarOverlay(turnoActual, basculaId);
}

// Exponer la función a Eel
eel.expose(actualizarTurnoDesdePython); // <-- ¡Esta línea es clave!
// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", inicializarAplicacion);

document.getElementById("actualizar-pagina").addEventListener("click", function () {
    location.reload(); // Recarga la página
});

function enterFullScreen() {
    let elem = document.documentElement; // Toda la página
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { // Firefox
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { // Chrome, Safari y Edge
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { // IE/Edge
        elem.msRequestFullscreen();
    }
}

// Ejecutar pantalla completa después de que cargue la página
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(enterFullScreen, 1000); // Esperar 1 seg para evitar bloqueos
});
