#gracias gemini por facilitarme un simulacro de prueba JAJAJAJAJA
import reports
import os

# --- EJECUTAR EL FLUJO ---
print("Iniciando simulación del menú principal...")

# Llamamos a la función principal del módulo reportes pasando los datos simulados
reports.iniciar_modulo_reportes()

print("\nVolvimos al menú principal simulado. Fin de la prueba.")

#Decorador para registrar en el audit.log todos los reportes generados
def registro_reporte_log(funcion):
    """Registra en audit.log cuando se genera un archivo."""
    def wrapper(*args, **kwargs):
        ruta_archivo = args[0] if args else "Desconocido"
        try:
            resultado = funcion(*args, **kwargs)
            #Si la función no lanzó excepción, registramos el éxito
            tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Genera el tiempo de creación del reporte
            mensaje = f"[{tiempo}] REPORTES: Archivo generado exitosamente: {ruta_archivo}\n"
            with open(cambios, "a", encoding='utf-8') as log: #Se registra al final del log el mensaje
                log.write(mensaje)
            return resultado
        except Exception as error: #Con esto se revisan todos los errores que están dentro de la clase de Exception
            print(f"[ERROR] Fallo al generar reporte o registrar log: {error}")
            raise #Relanzamos para que el menú lo maneje
    return wrapper