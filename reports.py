#Módulo para generar reportes según datos de módulos de: organizer.py, analyzer.py y auditor.py

#Importamos librerías y módulos
import csv
import os
import utils
from datetime import datetime

#archivos de prueba (eliminar luego en base a otros modulos)
logs = "logs"
cambios= "cambios"
carpeta_reportes = "reportes"
modulos= ["organizer", "audit", "analyzer"]

def leer_archivos(directorio, extension=".log"):
    """Función general para leer todos los archivos con una extensión .log en un directorio dado y esta devuelve su contenido."""
    data = []
    if not os.path.exists(directorio): #Si no existe el directorio, imprime una advertencia
        print(f"Advertencia. Directorio no encontrado: {directorio}")
        return data

    for nombre_archivo in os.listdir(directorio):
        if nombre_archivo.endswith(extension): #Busca si termina en .log
            filepath = os.path.join(directorio, nombre_archivo)
            try:
                with open(filepath, 'r', encoding='utf-8') as archivo: # Almacenamos el nombre del archivo y todas sus líneas
                    data.append({
                        "origen": directorio,
                        "nombre_archivo": nombre_archivo,
                        "contenido": archivo.readlines() #Lee las lineas del archivo y se quedan como contenido
                    })
            except Exception as error: #Si hay un error devuelve el error
                print(f"Error al leer el archivo {filepath}: {error}")
    return data

def obtener_datos_logs():
    """Lee la información de la carpeta logs."""
    archivos_logs = leer_archivos(logs, extension=".log")
    registros_logs = []

    for archivo in archivos_logs:
        for linea in archivo["contenido"]:
            linea = linea.strip()
            if linea:
                try:
                    #1. Separar la marca de tiempo/milisegundos
                    #Dividimos la línea en 3 partes: [Fecha], [Hora,milisegundos], [Resto del log]
                    partes = linea.split(' ', 2)
                    
                    if len(partes) < 3:
                        raise ValueError("No se pudo obtener la fecha y hora completas.")

                    fecha = partes[0] #Ej: 2025-12-01
                    hora_milisegundos_y_nivel = partes[1]
                        
                    fecha = partes[0] #Ej: 2025-12-01
                    hora_milisegundos_y_nivel = partes[1]
                    
                    #Capturamos la hora: "HH:MM:SS"
                    hora = hora_milisegundos_y_nivel.split(',')[0].strip()
                    
                    #Reconstruimos el campo fecha_hora final (Ej: "2025-12-01 HH:MM:SS")
                    fecha_hora = f"{fecha} {hora}" 
                    
                    # El resto del log comienza en la posición 2 del split
                    resto_log_sin_fecha = partes[2]
                    
                    #2. Extraer nivel [primer corchete]
                    inicio_nivel = resto_log_sin_fecha.find('[')
                    fin_nivel = resto_log_sin_fecha.find(']', inicio_nivel)
                    nivel = resto_log_sin_fecha[inicio_nivel:fin_nivel+1].strip('[]').upper()
                        
                    #3. Extraer el segundo corchete (Módulo)
                    resto_despues_nivel = resto_log_sin_fecha[fin_nivel+1:].strip()
                    inicio_modulo = resto_despues_nivel.find('[')
                    fin_modulo = resto_despues_nivel.find(']', inicio_modulo)
                        
                    if inicio_modulo != -1 and fin_modulo != -1:
                        modulo_nombre_crudo = resto_despues_nivel[inicio_modulo:fin_modulo+1].strip('[]')
                        modulo_nombre = modulo_nombre_crudo.strip().lower() 
                            
                        descripcion = resto_despues_nivel[fin_modulo+1:].strip()

                        registros_logs.append({
                            "fecha_hora": fecha_hora,
                            "modulo": modulo_nombre, 
                            "tipo": nivel,
                            "descripcion": descripcion
                        })
                
                except Exception as error:
                    print(f"Error en línea de cambio: {error}. Línea: {linea}")

    return registros_logs

def obtener_datos_cambios():
    """Lee la información de la carpeta cambios."""
    archivos_cambios = leer_archivos(cambios, extension=".log")
    registros_cambios = []
    
    for archivo in archivos_cambios:
        for linea in archivo["contenido"]:
            linea = linea.strip()
            if linea:
                try:
                    #1. Separar la marca de tiempo/milisegundos
                    partes = linea.split(' ', 2)
                    
                    if len(partes) < 3:
                        raise ValueError("No se pudo obtener la fecha y hora completas.")
                        
                    fecha = partes[0] # Ej: 2025-12-01
                    hora_milisegundos_y_nivel = partes[1]
                    
                    #Capturamos la hora: "HH:MM:SS" (cortando en la coma y limpiando)
                    hora = hora_milisegundos_y_nivel.split(',')[0].strip()
                    
                    #Reconstruimos el campo fecha_hora final (Ej: "2025-12-01 HH:MM:SS")
                    fecha_hora = f"{fecha} {hora}"
                    
                    #El resto del log comienza en la posición 2 del split
                    resto_log_sin_fecha = partes[2]
                    
                    #2. Extraer nivel [primer corchete]
                    inicio_nivel = resto_log_sin_fecha.find('[')
                    fin_nivel = resto_log_sin_fecha.find(']', inicio_nivel)
                    nivel = resto_log_sin_fecha[inicio_nivel:fin_nivel+1].strip('[]').upper()
                        
                    #3. Extraer el segundo corchete y la descripción
                    resto_despues_nivel = resto_log_sin_fecha[fin_nivel+1:].strip()
                    inicio_modulo = resto_despues_nivel.find('[')
                    fin_modulo = resto_despues_nivel.find(']', inicio_modulo)
                        
                    if inicio_modulo != -1 and fin_modulo != -1:
                        #Extraemos el módulo en el log, pero lo ignoramos para la etiqueta final
                        
                        descripcion = resto_despues_nivel[fin_modulo+1:].strip()

                        registros_cambios.append({
                            "fecha_hora": fecha_hora,
                            "modulo": "cambios",
                            "tipo": nivel,
                            "descripcion": descripcion
                        })

                except Exception as error:
                    print(f"Error en línea de cambio: {error}. Línea: {linea}")

    return registros_cambios

#Verificar que exista la carpeta de reportes y crear una si no existe
if not os.path.exists(carpeta_reportes):
    os.makedirs(carpeta_reportes)

#Funciones para generar los reportes y archivos .csv ó .txt

def generar_reporte(formato='txt', modulo_filtro=None, prefijo= "general"):
    """
    Función principal que compila todos los datos, filtra por módulo (opcional)
    y genera el reporte.
    :param formato: 'txt' o 'csv'
    :param modulo_filtro: Nombre del módulo a filtrar ('organizer', 'auditor', 'analyzer', 'cambios') o None para todos.
    """
    
    #Normalizar el filtro a minúsculas
    filtro_normalizado = modulo_filtro.lower() if modulo_filtro else None

    #Obtener todos los datos
    print("Obteniendo todos los datos disponibles...")
    registros_cambios = obtener_datos_cambios()
    registros_logs = obtener_datos_logs()
    
    todos_los_registros = registros_cambios + registros_logs

    #Aplicar el filtro por módulo
    registros_finales = []
    
    if filtro_normalizado and filtro_normalizado != 'todos':
    # Filtramos la lista de registros
        registros_finales = [
            registro for registro in todos_los_registros 
            if registro["modulo"].strip().lower() == filtro_normalizado
        ]
    else:
        #Si no hay filtro o se pide 'todos', se incluyen todos
        print("Generando reporte para TODOS los módulos.")
        registros_finales = todos_los_registros

    if not registros_finales:
        print(f"No se encontraron registros para el módulo/filtro '{modulo_filtro if modulo_filtro else 'todos'}'.")
        return

    #Generar el nombre del archivo de salida
    timestamp_reporte = datetime.now().strftime("%Y.%m.%d_%H-%M")
    nombre_archivo_salida = f"{prefijo}_{timestamp_reporte}.{formato.lower()}"
    
    #Construir la ruta completa del archivo
    ruta_completa_archivo = os.path.join(carpeta_reportes, nombre_archivo_salida)

    #Escribir el reporte según el tipo de archivo deseado
    if formato.lower() == "csv":
        escribir_reporte_csv(ruta_completa_archivo, registros_finales)
    elif formato.lower() == "txt":
        escribir_reporte_txt(ruta_completa_archivo, registros_finales)
    else:
        print(f"Error: Formato de reporte no soportado: {formato}")
        return

    print(f"\nReporte generado exitosamente: {ruta_completa_archivo}")

def escribir_reporte_txt(ruta_completa_archivo, registros):
    """Escribe los registros en formato .txt"""
    with open(ruta_completa_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write("--- REPORTE DE ACTIVIDAD DEL SISTEMA ---\n")
        archivo.write(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write("-" * 80 + "\n")
        
        archivo.write(f"{'FECHA/HORA':<20} | {'MÓDULO':<15} | {'TIPO':<8} | DESCRIPCIÓN\n")
        archivo.write("-" * 80 + "\n")

        for reg in registros:
            linea = (
                f"{reg['fecha_hora']:<20} | "
                f"{reg['modulo'].upper():<15} | "
                f"{reg['tipo']:<8} | "
                f"{reg['descripcion']}\n"
            )
            archivo.write(linea)
        archivo.write("-" * 80 + "\n")
        archivo.write(f"Total de registros: {len(registros)}\n")

def escribir_reporte_csv(ruta_completa_archivo, registros):
    """Escribe los registros en formato .CSV."""
    campos = ['fecha_hora', 'modulo', 'tipo', 'descripcion']
    try:
        with open(ruta_completa_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=campos, delimiter=',') 
            writer.writeheader()
            writer.writerows(registros)
    except Exception as error:
        print(f"Error al escribir el archivo CSV: {error}")

#Flujo del módulo (añadir a main)

def iniciar_modulo_reportes(): 
    """Función principal que ejecuta el flujo del módulo reports.py"""
    while True:
        print("\n--- MÓDULO DE REPORTES ---")
        print("¡Bienvenido al módulo de reportes!\nAcá podrás generar reportes sobre el historial de logs y cambios del sistema.")
        print("\n--- Opciones de Reporte de Historial ---")
        print("1. Historial de Auditoría (Todos los logs y cambios)")
        print("2. Resumen de organización")
        print("3. Historial de auditoría")
        print("4. Hallazgos de análisis")
        print("5. Volver al menú principal")
        print("")
        
        opcion = input("Seleccione una opción: ")
        utils.limpiar_pantalla()
        
        #Variable para el filtro y el prefijo
        modulo_a_filtrar = None
        prefijo_archivo = None
        
        if opcion == "1":
            #Historial completo (sin filtro)
            modulo_a_filtrar = None  #None significa "todos"
            prefijo_archivo = "rep_auditoria_completa"
            
        elif opcion == "2":
            #Historial Filtrado: Organizer
            modulo_a_filtrar = "organizer"
            prefijo_archivo = "rep_organizer"
            
        elif opcion == "3":
            #Historial Filtrado: Auditor
            modulo_a_filtrar = "auditor"
            prefijo_archivo = "rep_auditor"
            
        elif opcion == "4":
            #Historial Filtrado: Analyzer
            modulo_a_filtrar = "analyzer"
            prefijo_archivo = "rep_analyzer"

        elif opcion == "5":
            break
        
        else:
            print("Opción no válida.")
            continue
            
        #Generación de reporte según selección de usuario
        print("\n--- FORMATO DE REPORTE ---")
        print("¿Qué formato desea?")
        print("1. TXT (texto legible en archivo .txt)")
        print("2. CSV (archivo .csv compatible con Excel)")
        formato_opcion = input("Seleccione el formato deseado: ")
        utils.limpiar_pantalla()

        formato = None
        if formato_opcion == "1": #.txt
            formato = 'txt'
        elif formato_opcion == "2": #.csv
            formato = 'csv'
        else:
            print("Formato no válido.")
            continue

        try:
            generar_reporte(formato=formato, modulo_filtro=modulo_a_filtrar, prefijo=prefijo_archivo)
            
        except Exception as error:
            print(f"\n[ERROR] No se pudo generar el reporte: {error}")