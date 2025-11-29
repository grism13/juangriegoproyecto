#Módulo para generar reportes según datos de módulos de: organizer.py, analyzer.py y auditor.py

#Importamos librerías y módulos
import csv
import datetime
import os
import utils

#archivos de prueba (eliminar luego en base a otros modulos)
archivo_auditoria = "audit.log"
carpeta_reportes = "reportes"

#Verificar que exista la carpeta de reportes y crear una si no existe
if not os.path.exists(carpeta_reportes):
    os.makedirs(carpeta_reportes)

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
            with open(archivo_auditoria, "a", encoding='utf-8') as log: #Se registra al final del log el mensaje
                log.write(mensaje)
            return resultado
        except Exception as error: #Con esto se revisan todos los errores que están dentro de la clase de Exception
            print(f"[ERROR] Fallo al generar reporte o registrar log: {error}")
            raise #Relanzamos para que el menú lo maneje
    return wrapper

#Funciones para generar los archivos .csv ó .txt

@registro_reporte_log #Llamamos al decorador
def generar_archivo_csv(ruta_completa, datos):
    """Genera archivos .csv usando el módulo csv"""
    if not datos:
        raise ValueError("No hay datos para generar el reporte .csv") #Si no hay datos lanza el error
        
    #Asumimos que "datos" se está manejando como una lista de diccionarios
    #Obtenemos los encabezados
    encabezados = list(datos[0].keys()) if isinstance(datos[0], dict) else []

    with open(ruta_completa, mode="w", newline="", encoding="utf-8") as archivo: #Abrimos el archivo en modo escritura
        escritor_csv = csv.DictWriter(archivo, fieldnames=encabezados) #Con esta función de la librería de csv escribimos los datos de encabezados
        escritor_csv.writeheader()
        escritor_csv.writerows(datos) #Se escriben los datos completos
    
    print(f"\nReporte guardado con éxito en /{ruta_completa}")


@registro_reporte_log #Llamamos al decorador
def generar_archivo_txt(ruta_completa, titulo, datos):
    """Genera archivos .txt"""
    if not datos:
        raise ValueError("No hay datos para generar el reporte .txt") #Si no hay datos lanza el error

    encabezados = list(datos[0].keys()) if isinstance(datos[0], dict) else []
    with open(ruta_completa, "w", encoding="utf-8") as archivo: #Abrimos el archivo en modo escritura
        archivo.write("="*50 + "\n") #Simple decoración jsjsjs
        archivo.write(f" REPORTE: {titulo.upper()}\n")
        archivo.write(f" Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n") #Tiempo en el momento
        archivo.write("="*50 + "\n") #Simple decoración jsjsjs
        
        for encabezados in datos:
                archivo.write(f"- {encabezados}\n") #Escribir los datos
             
        archivo.write("\n" + "="*50 + "\nFIN DEL REPORTE")

    print(f"\n Reporte guardado con éxito en /{ruta_completa}")

#Función para leer datos de auditor

def leer_historial_auditoria():
    """Lee el archivo audit.log y lo devuelve como lista de diccionarios para el reporte"""
    datos_log = []
    if not os.path.exists(archivo_auditoria):
        print(f"[AVISO] No existe el archivo {archivo_auditoria} todavía")
        return []
        
    try:
        with open(archivo_auditoria, 'r', encoding='utf-8') as f:
            for linea in f:
                # Limpiamos la línea y la añadimos como un diccionario simple
                datos_log.append({"Entry": linea.strip()})
    except Exception as error:
        print(f"[ERROR] Al leer auditoría: {error}")
        return []
    return datos_log

#Flujo del módulo (añadir a main)

def iniciar_modulo_reportes(datos_organizacion_temp=None, datos_analisis_temp=None): #OJO modificar luego en base a los otros modulos
    """Función principal que ejecuta el flujo del módulo. Esta recibe datos temporales de otros módulos si existen."""
    while True:
        print("\n--- MÓDULO DE REPORTES ---")
        print("¡Bienvenido al módulo de reportes!\nAcá podrás generar reportes automáticos sobre las diferentes funciones del sistema.")
        print("\n1. Resumen de organización")
        print("2. Hallazgos de análisis")
        print("3. Historial de auditoría")
        print("4. Volver al menú principal")
        print("")
        
        #Preguntar al usuario la opción
        opcion = input("Seleccione una opción: ")
        utils.limpiar_pantalla()

        #Variables dependiendo de la selección
        datos_a_reportar = []
        titulo_reporte = ""
        prefijo_archivo = ""

        #Leer datos de los logs
        if opcion == "1":
            if not datos_organizacion_temp:
                print("\n[ALERTA] No hay resultados de organización disponibles en esta sesión.")
                continue
            datos_a_reportar = datos_organizacion_temp
            titulo_reporte = "Resumen de organización de archivos"
            prefijo_archivo = "rep_organizacion" #rep significa reporte
            
        elif opcion == "2":
            if not datos_analisis_temp:
                print("\n[ALERTA] No hay resultados de análisis disponibles en esta sesión.")
                continue
            datos_a_reportar = datos_analisis_temp
            titulo_reporte = "Hallazgos de análisis de contenido"
            prefijo_archivo = "rep_analisis" #rep significa reporte

        elif opcion == "3":
            print("Leyendo archivo de logs...")
            datos_a_reportar = leer_historial_auditoria()
            if not datos_a_reportar:
                 print("\n[ALERTA] El log está vacío o no se pudo leer.")
                 continue
            titulo_reporte = "Historial completo de auditoría"
            prefijo_archivo = "rep_auditoria" #rep significa reporte
            
        elif opcion == "4": #Regresar al menú
            break
        
        else:
            print("Opción no válida.")
            continue
            
        #Preguntar formato
        print(f"\nSe van a reportar {len(datos_a_reportar)} registros. ¿Qué formato desea?")
        print("1. TXT (Texto legible en archivo .txt)")
        print("2. CSV (Archivo .csv compatible con Excel)")
        formato_opcion = input("Seleccione el formato deseado: ")
        utils.limpiar_pantalla()
        #Generar nombre de archivo único con el tiempo
        timestamp = datetime.datetime.now().strftime("%Y.%m.%d_%H%M%S")
        
        try:
            #Generar el archivo
            if formato_opcion == "1": #Archivo TXT
                nombre_archivo = f"{prefijo_archivo}_{timestamp}.txt"
                ruta_completa = os.path.join(carpeta_reportes, nombre_archivo)
                generar_archivo_txt(ruta_completa, titulo_reporte, datos_a_reportar)
                
            elif formato_opcion == "2": #Archivo CSV
                #Verificar que los datos sean compatibles con CSV (lista de diccionarios)
                if datos_a_reportar and not isinstance(datos_a_reportar[0], dict):
                     print("[ERROR] Los datos seleccionados no tienen estructura para CSV.")
                     continue
                nombre_archivo = f"{prefijo_archivo}_{timestamp}.csv" #Generar el archivo
                ruta_completa = os.path.join(carpeta_reportes, nombre_archivo)
                generar_archivo_csv(ruta_completa, datos_a_reportar)
            else:
                print("Formato no válido.")

        except Exception as error:
            print(f"\n[ERROR] No se pudo generar el reporte: {error}")