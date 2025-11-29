import os
import datetime
import json

def escribir_log(nivel, mensaje, detalles,tiempo):
    """Escribe un log con el nivel, mensaje y detalles para el auditor."""
    # 1. Fecha con milisegundos (mmm)
    ahora = datetime.datetime.now()
    fecha_fmt = ahora.strftime("%Y-%m-%d %H:%M:%S")
    milisegundos = int(ahora.microsecond / 1000)
    tiempo_completo = f"{fecha_fmt},{milisegundos:03d}" # :03d asegura 3 dígitos (ej. 005)
    
    # 2. Construir la línea
    # Formato: YYYY-MM-DD HH:MM:SS,mmm [LEVEL] [Module] Message... Key=Value
    linea_log = f"{tiempo_completo} [{nivel}] [Auditor] {mensaje} {detalles}\n"
    
    # 3. Escribir y mostrar en consola
    print(linea_log)
    with open(f"./logs/audit_{tiempo}.log", "a") as log:
        log.write(linea_log)

def escribir_log_cambios(nivel, mensaje, detalles,tiempo):
    """Escribe un log con el nivel, mensaje y detalles para los cambios."""
    # 1. Fecha con milisegundos (mmm)
    ahora = datetime.datetime.now()
    fecha_fmt = ahora.strftime("%Y-%m-%d %H:%M:%S")
    milisegundos = int(ahora.microsecond / 1000)
    tiempo_completo = f"{fecha_fmt},{milisegundos:03d}" # :03d asegura 3 dígitos (ej. 005)
    
    # 2. Construir la línea
    # Formato: YYYY-MM-DD HH:MM:SS,mmm [LEVEL] [Module] Message... Key=Value
    linea_log = f"{tiempo_completo} [{nivel}] [Auditor] {mensaje} {detalles}\n"
    
    # 3. Escribir y mostrar en consola
    print(linea_log)
    with open(f"./cambios/cambios_{tiempo}.log", "a") as log:
        log.write(linea_log)

def obtener_estado_actual(carpeta):
    """Devuelve el estado actual del proyecto."""
    estado = {}
    for carpeta, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            if "snapshot.json" in archivo or "audit.log" in archivo:
                continue
            stats = os.stat(ruta_completa)
            tiempo_modificacion = stats.st_mtime
            peso = stats.st_size
            estado[ruta_completa] = (tiempo_modificacion, peso)
    return estado

def generar_snapshot(carpeta,tiempo):
    """Genera un snapshot del estado actual del proyecto."""
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    respuesta = "s"
    if os.path.exists("./logs/snapshot.json"):
        escribir_log("WARNING", "El archivo snapshot.json ya existe."," " ,tiempo)
        print("Desea sobreescribir el snapshot? (s/n)")
        respuesta = input().lower()
    if respuesta == "s":
        with open("./logs/snapshot.json", "w") as snapshot:
            json.dump(obtener_estado_actual(carpeta), snapshot, indent=4)
        escribir_log("INFO", "Snapshot generado exitosamente.", f"Carpeta={carpeta}",tiempo)
    else:
        escribir_log("INFO", "Snapshot no generado. Se conserva el anterior."," ",tiempo)


def generar_reporte(carpeta,tiempo):
    """Genera un reporte de los cambios en la carpeta."""
    archivos_cambiados = 0
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    if not os.path.exists("./logs/snapshot.json"):
        escribir_log("ERROR", "No se encontro snapshot.json, Volviendo al menu principal", " ",tiempo)
        return
    with open("./logs/snapshot.json", "r") as snapshot:
        estado_anterior = json.load(snapshot)
    estado_actual = obtener_estado_actual(carpeta)
    
    set_anterior = set(estado_anterior.keys())
    set_actual = set(estado_actual.keys())
    
    nuevos = set_actual - set_anterior
    eliminados = set_anterior - set_actual
    modificados = set_actual & set_anterior
    if not os.path.exists("./cambios"):
        os.makedirs("./cambios")
    if nuevos:
        for archivo in nuevos:  
            escribir_log_cambios("INFO", "Nuevo archivo", f"Archivo={archivo}",tiempo)
            archivos_cambiados += 1
    if eliminados:      
        for archivo in eliminados:
            escribir_log_cambios("INFO", "Archivo eliminado", f"Archivo={archivo}",tiempo)
            archivos_cambiados += 1
    if modificados:
        for archivo in modificados:
            if estado_actual[archivo][0] != estado_anterior[archivo][0] or estado_actual[archivo][1] != estado_anterior[archivo][1]:
                escribir_log_cambios("INFO", "Archivo modificado", f"Archivo={archivo}",tiempo)
                archivos_cambiados += 1
    if archivos_cambiados == 0:
        escribir_log("INFO", "No hay cambios en la carpeta.", f"Carpeta={carpeta}",tiempo)
    else:
        escribir_log("INFO", "Se detectaron cambios en la carpeta.", f"Carpeta={carpeta}",tiempo)