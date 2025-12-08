#Modulo de organizar mediante carpetas
import os
import shutil
import time
import utils

@utils.medir_tiempo
def mover_archivo(ruta_origen, carpeta_destino_nombre, carpeta_raiz,tiempo):

    # Calculamos la ruta completa de la carpeta destino
    ruta_destino_carpeta = os.path.join(carpeta_raiz, carpeta_destino_nombre)
    
    # Obtenemos solo el nombre del archivo (ej. "foto.jpg")
    nombre_archivo = os.path.basename(ruta_origen)
    
    # Calculamos la ruta final donde quedará el archivo
    ruta_final = os.path.join(ruta_destino_carpeta, nombre_archivo)

    try:
        # 1. Crear carpeta si no existe 
        if not os.path.exists(ruta_destino_carpeta):
            os.makedirs(ruta_destino_carpeta)
            utils.escribir_log("INFO",f" Carpeta creada: {carpeta_destino_nombre}"," ",tiempo,"Organizer","organizer")
        
        # 2. Mover archivo
        shutil.move(ruta_origen, ruta_final)
        utils.escribir_log("INFO",f"Movido: {nombre_archivo} -> {carpeta_destino_nombre}"," ",tiempo,"Organizer","organizer")
        
    except Exception as e:
        utils.escribir_log("ERROR",f"Error moviendo {nombre_archivo}: {e}"," ",tiempo,"Organizer","organizer")

def generar_vista_previa(ruta_origen, carpeta_destino_nombre, carpeta_raiz,nombre_archivo):
    ruta_destino_carpeta = os.path.join(carpeta_raiz, carpeta_destino_nombre,nombre_archivo)
    print(f"{utils.colores["rojo"]}{ruta_origen} {utils.colores["normal"]}-----> {utils.colores["verde"]}{ruta_destino_carpeta}{utils.colores["normal"]}")
    

def organizar_archivos_por_extension(ruta_de_carpeta,tiempo):
    
    #Obtener lista de los archivos
    contenido = os.listdir(ruta_de_carpeta)
    while True:
        utils.limpiar_pantalla()
        print(f"""
---------------------------------------------------------------------------------------------------
 Analizando carpeta: {ruta_de_carpeta}
---------------------------------------------------------------------------------------------------
""")
        archivos_a_cambiar = set()
        print("Archivos a organizar:")
        for archivo in contenido:
            ruta_completa = os.path.join(ruta_de_carpeta, archivo)

            #Se verifica que es un archivo y no carpeta
            if os.path.isfile(ruta_completa):
                nombre, tipo = os.path.splitext(archivo)
                #Se elimina el puto de la extension
                tipo = tipo[1:]
                tipo = tipo.upper()
                if not tipo:
                    tipo = "Otros"

                archivos_a_cambiar.add((ruta_completa,tipo))
                generar_vista_previa(ruta_completa, tipo, ruta_de_carpeta, archivo)
        
        opcion = input("Acepta estos cambios(s/n) : ").lower()
        if opcion == "s":
            break
        elif opcion == "n":
            break
        else:
            input("Opción no válida, Press enter para continuar..")
    if opcion == "s":
        for ruta_completa,tipo in archivos_a_cambiar:
            mover_archivo(ruta_completa, tipo, ruta_de_carpeta,tiempo)
        input("Se movieron los archivos. Press enter para continuar")
    else:
        input("No se movieron los archivos. Press enter para continuar")

def organizar_archivos_por_espacio(ruta_de_carpeta,tiempo):
    contenido = os.listdir(ruta_de_carpeta)
    while True:
        utils.limpiar_pantalla()
        print(f"""
---------------------------------------------------------------------------------------------------
 Analizando carpeta: {ruta_de_carpeta}
---------------------------------------------------------------------------------------------------
""")
        print("Archivos a organizar:")
        archivos_a_cambiar = set()
        for archivo in contenido:
            ruta_completa = os.path.join(ruta_de_carpeta, archivo)

            if os.path.isfile(ruta_completa):
                tamano_mb = os.path.getsize(ruta_completa) / (1024 * 1024)
                nombre_carpeta = "VARIOS"

                if tamano_mb < 1:
                    nombre_carpeta = "PEQUEÑOS"
                elif tamano_mb < 500:
                    nombre_carpeta = "MEDIANOS"
                else:
                    nombre_carpeta = "GRANDES"
                archivos_a_cambiar.add((ruta_completa,nombre_carpeta))
                generar_vista_previa(ruta_completa, nombre_carpeta, ruta_de_carpeta, archivo)
        opcion = input("Acepta estos cambios(s/n) : ").lower()
        if opcion == "s":
            break
        elif opcion == "n":
            break
        else:
            input("Opción no válida, Press enter para continuar..")
    if opcion == "s":
        for ruta_completa, nombre_carpeta in archivos_a_cambiar:
            mover_archivo(ruta_completa, nombre_carpeta, ruta_de_carpeta,tiempo)
        input("Se movieron los archivos. Press enter para continuar")
    else:
        input("No se movieron los archivos. Press enter para continuar")

def organizar_archivos_por_fecha(ruta_de_carpeta,tiempo):
    contenido = os.listdir(ruta_de_carpeta)
    while True:
        utils.limpiar_pantalla()
        print(f"""
---------------------------------------------------------------------------------------------------
 Analizando carpeta: {ruta_de_carpeta}
---------------------------------------------------------------------------------------------------
""")
        print("Archivos a organizar:")
        archivos_a_cambiar = set()
        for archivo in contenido:
            ruta_completa = os.path.join(ruta_de_carpeta, archivo)
            
            if os.path.isfile(ruta_completa):
                timestamp = os.path.getmtime(ruta_completa)
                fecha = time.localtime(timestamp)
                dia_mes_año = f"{fecha.tm_mday}-{fecha.tm_mon}-{fecha.tm_year}"
                
                archivos_a_cambiar.add((ruta_completa,dia_mes_año))
                generar_vista_previa(ruta_completa, dia_mes_año, ruta_de_carpeta, archivo)            
        opcion = input("Acepta estos cambios(s/n) : ").lower()
        if opcion == "s":
            break
        elif opcion == "n":
            break
        else:
            input("Opción no válida, Press enter para continuar..")
    if opcion == "s":
        for ruta_completa, dia_mes_año in archivos_a_cambiar:
            mover_archivo(ruta_completa, dia_mes_año, ruta_de_carpeta,tiempo)
        input("Se movieron los archivos. Press enter para continuar")
    else:
        input("No se movieron los archivos. Press enter para continuar")
            
            