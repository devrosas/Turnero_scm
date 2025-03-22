export class ConfigManager {
    constructor() {
        this.config = {}; // Inicialmente vacío, se cargará desde Python
        console.log("ConfigManager inicializado");
        this.cargarConfiguracionInicial();
        this.configurarInputs(); // Configurar los inputs de archivo
    }

    // Configurar los inputs de archivo
    configurarInputs() {
        console.log("Configurando inputs de archivo...");
    
        // Obtener referencias a los elementos del DOM
        const botonCambiarFondo = document.getElementById("cambiar-fondo");
        const inputFondo = document.getElementById("input-fondo");
        //const botonCambiarLogo = document.getElementById("cambiar-logo");//
        const inputLogo = document.getElementById("input-logo");
        const botonCambiarSonido = document.getElementById("cambiar-sonido");
        const inputSonido = document.getElementById("input-sonido");
        const botonSeleccionarGaleria = document.getElementById("seleccionar-galeria");
        const botonActualizarPrecios = document.getElementById("actualizar-precios");
        const inputExcel = document.getElementById("input-excel");
    
        // Eliminar eventos anteriores (clonar los elementos para eliminar los manejadores)
        const nuevosElementos = {
            botonCambiarFondo: botonCambiarFondo.cloneNode(true),
            inputFondo: inputFondo.cloneNode(true),
           // botonCambiarLogo: botonCambiarLogo.cloneNode(true),//
            //inputLogo: inputLogo.cloneNode(true),//
            botonCambiarSonido: botonCambiarSonido.cloneNode(true),
            inputSonido: inputSonido.cloneNode(true),
            botonSeleccionarGaleria: botonSeleccionarGaleria.cloneNode(true),
            botonActualizarPrecios: botonActualizarPrecios.cloneNode(true),
            inputExcel: inputExcel.cloneNode(true),
        };
    
        // Reemplazar los elementos antiguos con los nuevos
        botonCambiarFondo.replaceWith(nuevosElementos.botonCambiarFondo);
        inputFondo.replaceWith(nuevosElementos.inputFondo);
        //botonCambiarLogo.replaceWith(nuevosElementos.botonCambiarLogo);//
        //inputLogo.replaceWith(nuevosElementos.inputLogo);//
        botonCambiarSonido.replaceWith(nuevosElementos.botonCambiarSonido);
        inputSonido.replaceWith(nuevosElementos.inputSonido);
        botonSeleccionarGaleria.replaceWith(nuevosElementos.botonSeleccionarGaleria);
        botonActualizarPrecios.replaceWith(nuevosElementos.botonActualizarPrecios);
        inputExcel.replaceWith(nuevosElementos.inputExcel);
    
        // Registrar nuevos eventos en los elementos clonados
        nuevosElementos.botonCambiarFondo.addEventListener("click", () => {
            console.log("Click en Cambiar Fondo");
            nuevosElementos.inputFondo.click();
        });
        nuevosElementos.inputFondo.addEventListener("change", (event) => {
            console.log("Archivo de fondo seleccionado");
            this.manejarSeleccionArchivo(event, "cambiar_fondo", "Fondo cambiado correctamente");
        });
    
        /*nuevosElementos.botonCambiarLogo.addEventListener("click", () => {
            console.log("Click en Cambiar Logo");
            nuevosElementos.inputLogo.click();
        });
        nuevosElementos.inputLogo.addEventListener("change", (event) => {
            console.log("Archivo de logo seleccionado");
            this.manejarSeleccionArchivo(event, "cambiar_logo", "Logo cambiado correctamente");
        });*/
    
        nuevosElementos.botonCambiarSonido.addEventListener("click", () => {
            console.log("Click en Cambiar Sonido");
            nuevosElementos.inputSonido.click();
        });
        nuevosElementos.inputSonido.addEventListener("change", (event) => {
            console.log("Archivo de sonido seleccionado");
            this.manejarSeleccionArchivo(event, "seleccionar_sonido", "Sonido cambiado correctamente");
        });
    
        nuevosElementos.botonSeleccionarGaleria.addEventListener("click", async () => {
            console.log("Click en Seleccionar Galería");
            const rutaGaleria = await eel.seleccionar_carpeta_galeria()();
            if (rutaGaleria) {
                console.log("Carpeta seleccionada:", rutaGaleria);
                this.config = await eel.cargar_configuracion()();
                this.aplicarConfiguracion();
                alert("Galería cambiada correctamente");
            } else {
                console.error("No se seleccionó ninguna carpeta.");
            }
        });
    
        nuevosElementos.botonActualizarPrecios.addEventListener("click", () => {
            console.log("Click en Actualizar Precios");
            nuevosElementos.inputExcel.click();
        });
        nuevosElementos.inputExcel.addEventListener("change", (event) => {
            console.log("Archivo Excel seleccionado");
            this.manejarSeleccionExcel(event);
        });
    }

    // Cargar la configuración inicial desde Python
    async cargarConfiguracionInicial() {
        console.log("Cargando configuración inicial...");
        this.config = await eel.cargar_configuracion()(); // Llamar a la función de Python
        console.log("Configuración cargada:", this.config);
        this.aplicarConfiguracion();
    }

    // Aplicar la configuración cargada al HTML y CSS
    aplicarConfiguracion() {
        console.log("Aplicando configuración cargada...");
        this.actualizarFondoEnCSS(this.config.ruta_fondo);
        //this.actualizarLogoEnHTML(this.config.ruta_logo);//
        this.actualizarSonidoEnHTML(this.config.sonido_path);
    }

    // Actualizar el fondo en el CSS
    actualizarFondoEnCSS(rutaFondo) {
        console.log("Actualizando fondo con ruta:", rutaFondo);
        const body = document.body;
        body.style.backgroundImage = `url("${rutaFondo}")`;
    }

    // Actualizar el logo en el HTML
    /*actualizarLogoEnHTML(rutaLogo) {
        console.log("Actualizando logo con ruta:", rutaLogo);
        const logoElement = document.getElementById("logo");
        if (logoElement) {
            logoElement.src = rutaLogo;
        }
    }*/

    // Actualizar el sonido en el HTML
    actualizarSonidoEnHTML(rutaSonido) {
        console.log("Actualizando sonido con ruta:", rutaSonido);
        const sonidoElement = document.getElementById("sonido-turno");
        if (sonidoElement) {
            sonidoElement.src = rutaSonido;
        }
    }

    // Manejar la selección de archivos
    async manejarSeleccionArchivo(event, funcionPython, mensajeExito) {
        const archivo = event.target.files[0];
        if (archivo) {
            console.log("Archivo seleccionado:", archivo.name);
    
            try {
                // Convertir el archivo a base64
                const { base64 } = await this.archivoABase64(archivo); // Extraer solo el base64
                console.log("Archivo convertido a base64.");
    
                // Llamar a la función de Python correspondiente
                const rutaArchivo = await eel[funcionPython](archivo.name, base64)();
                console.log("Ruta del archivo guardado:", rutaArchivo);
    
                if (rutaArchivo) {
                    // Actualizar la configuración
                    this.config = await eel.cargar_configuracion()();
                    this.aplicarConfiguracion();
                    alert(mensajeExito); // Mostrar un mensaje de éxito
                } else {
                    console.error("Error: La ruta del archivo es null.");
                    alert("Error al guardar el archivo en el servidor.");
                }
            } catch (error) {
                console.error("Error al procesar el archivo:", error.message);
                alert("Error al procesar el archivo.");
            }
        } else {
            console.log("No se seleccionó ningún archivo.");
        }
    }

    // Método para manejar la selección de archivos Excel
    async manejarSeleccionExcel(event) {
        const archivo = event.target.files[0];
        if (archivo) {
            console.log("Archivo seleccionado:", archivo.name);
    
            // Convertir el archivo a base64
            const base64 = await this.archivoABase64_2(archivo);
            if (!base64) {
                console.error("Error: No se pudo convertir el archivo a base64.");
                return;
            }
    
            // Validar el archivo Excel antes de proceder
            const validacion = await eel.validar_archivo_excel(base64)();
            console.log("Resultado de la validación:", validacion);
    
            if (validacion.status === "error") {
                alert(validacion.message); // Mostrar mensaje de error al usuario
                return; // Detener el proceso si el archivo no es válido
            }
    
            // Si el archivo es válido, proceder con la actualización de precios
            const resultado = await eel.actualizar_precios_desde_excel(base64)();
            console.log("Resultado de la actualización:", resultado);
    
            // Mostrar un mensaje al usuario
            alert(resultado.message || resultado);
        } else {
            console.log("No se seleccionó ningún archivo.");
        }
    }

    // Función para convertir un archivo a base64
    archivoABase64(archivo) {
        return new Promise((resolve, reject) => {
            // Validar que el archivo no sea nulo o indefinido
            if (!archivo) {
                reject(new Error("No se proporcionó un archivo válido."));
                return;
            }
    
            // Validar que el archivo sea un objeto File o Blob
            if (!(archivo instanceof File || archivo instanceof Blob)) {
                reject(new Error("El archivo no es un objeto File o Blob válido."));
                return;
            }
    
            // Crear una instancia de FileReader
            const reader = new FileReader();
    
            // Manejar el evento de carga exitosa
            reader.onload = () => {
                try {
                    // Obtener el resultado (base64 con prefijo)
                    const result = reader.result;
    
                    // Verificar que el resultado no esté vacío
                    if (!result) {
                        reject(new Error("No se pudo leer el archivo."));
                        return;
                    }
    
                    // Separar el prefijo "data:tipo_mime;base64," del contenido base64
                    const [prefix, base64] = result.split(",");
    
                    // Verificar que el prefijo y el base64 sean válidos
                    if (!prefix || !base64) {
                        reject(new Error("El archivo no se pudo convertir a base64 correctamente."));
                        return;
                    }
    
                    // Extraer el tipo MIME del prefijo
                    const mimeType = prefix.match(/^data:(.*);base64$/)?.[1];
    
                    // Devolver un objeto con el base64 y metadatos
                    resolve({
                        base64: base64, // Contenido base64 sin prefijo
                        nombre: archivo.name, // Nombre del archivo
                        tipo: mimeType, // Tipo MIME (por ejemplo, "audio/mp3")
                        tamaño: archivo.size, // Tamaño del archivo en bytes
                    });
                } catch (error) {
                    reject(new Error(`Error al procesar el archivo: ${error.message}`));
                }
            };
    
            // Manejar errores de lectura
            reader.onerror = () => {
                reject(new Error("Error al leer el archivo."));
            };
    
            // Leer el archivo como Data URL (base64)
            reader.readAsDataURL(archivo);
        });
    }

    archivoABase64_2(archivo) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // Eliminar el prefijo "data:application/octet-stream;base64,"
                const base64 = reader.result.split(',')[1];
                resolve(base64); // Devolver solo el string base64
            };
            reader.onerror = reject;
            reader.readAsDataURL(archivo);
        });
    }
}