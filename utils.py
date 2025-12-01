import os
import platform
import datetime

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_encabezado(titulo):
    """Muestra un título decorado y centra el texto."""
    limpiar_pantalla()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60)
    print("\n")
    
def escribir_log(nivel, mensaje, detalles,tiempo,host,nombre_log,carpeta="logs"):
    """Escribe un log con el nivel, mensaje y detalles ."""
    # 1. Fecha con milisegundos (mmm)
    ahora = datetime.datetime.now()
    fecha_fmt = ahora.strftime("%Y-%m-%d %H:%M:%S")
    milisegundos = int(ahora.microsecond / 1000)
    tiempo_completo = f"{fecha_fmt},{milisegundos:03d}" # :03d asegura 3 dígitos (ej. 005)
    
    # 2. Construir la línea
    # Formato: YYYY-MM-DD HH:MM:SS,mmm [LEVEL] [Module] Message... Key=Value
    linea_log = f"{tiempo_completo} [{nivel}] [{host}] {mensaje} {detalles}\n"
    
    # 3. Escribir y mostrar en consola
    print(linea_log)
    with open(f"./{carpeta}/{nombre_log}_{tiempo}.log", "a") as log:
        log.write(linea_log)