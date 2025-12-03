import os
import datetime
import json
from utils import escribir_log

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

def generar_snapshot(carpeta,tiempo,saltar_comprobacion=False):
    """Genera un snapshot del estado actual del proyecto."""
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    respuesta = "s"
    if os.path.exists("./logs/snapshot.json") and  not saltar_comprobacion:
        escribir_log("WARNING", "El archivo snapshot.json ya existe."," " ,tiempo,"Auditor","audit")
        print("Desea sobreescribir el snapshot? (s/n)")
        respuesta = input().lower()
    if respuesta == "s":
        with open("./logs/snapshot.json", "w", encoding='utf-8') as snapshot:
            json.dump(obtener_estado_actual(carpeta), snapshot, indent=4)
        escribir_log("INFO", "Snapshot generado exitosamente.", f"Carpeta={carpeta}",tiempo,"Auditor","audit")
    else:
        escribir_log("INFO", "Snapshot no generado. Se conserva el anterior."," ",tiempo,"Auditor","audit")


def generar_reporte(carpeta,tiempo):
    """Genera un reporte de los cambios en la carpeta."""
    archivos_cambiados = 0
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    if not os.path.exists("./logs/snapshot.json"):
        escribir_log("ERROR", "No se encontro snapshot.json, Volviendo al menu principal", " ",tiempo,"Auditor","audit")
        return
    with open("./logs/snapshot.json", "r", encoding='utf-8') as snapshot:
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
            escribir_log("INFO", "Nuevo archivo", f"Archivo={archivo}",tiempo,"Auditor","cambios","cambios")
            archivos_cambiados += 1
    if eliminados:      
        for archivo in eliminados:
            escribir_log("INFO", "Archivo eliminado", f"Archivo={archivo}",tiempo,"Auditor","cambios","cambios")
            archivos_cambiados += 1
    if modificados:
        for archivo in modificados:
            if estado_actual[archivo][0] != estado_anterior[archivo][0] or estado_actual[archivo][1] != estado_anterior[archivo][1]:
                escribir_log("INFO", "Archivo modificado", f"Archivo={archivo}",tiempo,"Auditor","cambios","cambios")
                archivos_cambiados += 1
    if archivos_cambiados == 0:
        escribir_log("INFO", "No hay cambios en la carpeta.", f"Carpeta={carpeta}",tiempo,"Auditor","audit")
    else:
        escribir_log("INFO", "Se detectaron cambios en la carpeta.", f"Carpeta={carpeta}",tiempo,"Auditor","audit")
        generar_snapshot(carpeta,tiempo,saltar_comprobacion=True)