class TurnoManager {
    constructor() {
        console.log("Inicializando TurnoManager...");
        
        // Elementos del DOM
        this.overlay = document.querySelector(".overlay-turno");
        this.numeroTurnoMaximizado = document.getElementById("numero-turno-maximizado");
        this.basculaTurnoMaximizado = document.getElementById("bascula-turno-maximizado");
        this.numeroTurnoNormal = document.getElementById("numero-turno");
        this.basculaTurnoNormal = document.getElementById("bascula-turno");
        
        console.log("Elementos del DOM obtenidos:", {
            overlay: this.overlay,
            numeroTurnoMaximizado: this.numeroTurnoMaximizado,
            basculaTurnoMaximizado: this.basculaTurnoMaximizado,
            numeroTurnoNormal: this.numeroTurnoNormal,
            basculaTurnoNormal: this.basculaTurnoNormal
        });
    }

    mostrarOverlay(turnoActual, basculaId) {
        console.log("Mostrando overlay con turnoActual:", turnoActual, "y basculaId:", basculaId);
        
        // Actualizar el contenido del overlay
        this.numeroTurnoMaximizado.textContent = turnoActual;
        this.basculaTurnoMaximizado.textContent = `Báscula: ${basculaId}`;

        // Mostrar el overlay
        this.overlay.style.display = "flex";

        console.log("Overlay mostrado");

        // Ocultar el overlay después de 3 segundos
        setTimeout(() => {
            console.log("Ocultando overlay después de 3 segundos");
            this.ocultarOverlay();
        }, 3000);
    }

    ocultarOverlay() {
        console.log("Ocultando overlay...");
        this.overlay.style.display = "none";
    }

    actualizarInterfaz(turnoActual, basculaId) {
        console.log("Actualizando interfaz con turnoActual:", turnoActual, "y basculaId:", basculaId);
        
        this.numeroTurnoNormal.textContent = `${turnoActual}`;
        this.basculaTurnoNormal.textContent = `BASCULA: ${basculaId}`;
        
        console.log("Interfaz actualizada");
    }
}

// Exportar una instancia de TurnoManager
export const turnoManager = new TurnoManager();
