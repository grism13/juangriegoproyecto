import os
import datetime
import json

def estado_actual(carpeta)
    """Devuelve el estado actual del proyecto."""
    estado = {}
    for carpeta, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta, archivo)
            if ".snapshot.json" in archivo or "audit.log" in archivo:
                continue
            stats = os.stat(ruta_completa)
            tiempo_modificacion = stats.st_mtime
            peso = stats.st_size
            estado[ruta_completa] = (tiempo_modificacion, peso)
    return estado

def generar_snapshot(carpeta):
    """Genera un snapshot del estado actual del proyecto."""
    if not os.path.exists(".snapshot.json"):
        with open(".snapshot.json", "w") as snapshot:
            json.dump(estado_actual(carpeta), snapshot, indent=4)
        print(f"Snapshot generado exitosamente. {datetime.datetime.now()}")
    else:
        print(f"El archivo .snapshot.json ya existe. {datetime.datetime.now()}")


