import re
import os
import utils

def menu_analizador(carpeta,tiempo):
   
    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    if not archivos:
        utils.escribir_log("WARM","Carpeta vacía.",f"Carpeta ={carpeta}",tiempo,"Analyzer","analyzer")
        return
    while True:
        utils.mostrar_encabezado("Selecciona un archivo")
        for i, archivo in enumerate(archivos, 1):
            print(f"{i}. {archivo}")
        print(f"{i+1}. Salir")
        
        seleccion = input("\nElige el número del archivo: ")
        if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(archivos) + 1:
            input("Opción inválida. Press enter para continuar..")
            continue 
        elif int(seleccion) == len(archivos)+1:
            input("Saliendo. Press enter para continuar...")
            return
        else:
            break
    
    
    archivo_a_analizar = os.path.join(carpeta, archivos[int(seleccion)-1])

   
    while True:
        utils.mostrar_encabezado(f"Analizando: {os.path.basename(archivo_a_analizar)}")
        
        print("¿Qué quieres extraer?")
        patrones = obtener_patrones() 
        for clave, valor in patrones.items():
            print(f"{clave}. {valor['nombre']}")
        
        opcion = input("\nElige una opción (1-8): ")
        
        
        resultados = analizador_archivos(archivo_a_analizar, opcion,tiempo)
        
        # --- MOSTRAR RESULTADOS Y RESUMEN ---
        if resultados:
            print(f"\n--- Resultados Encontrados ({len(resultados)}) ---")
            
            # Mostrar detalle (limitado a 10)
            for i, item in enumerate(resultados):
                i += 1
                if i < 10:
                    utils.escribir_log("INFO",f"Resultado encontrado en{archivo_a_analizar}",f"Línea {item['linea']}: {item['valor']}",tiempo,"Analyzer","analyzer")
                else:
                    utils.escribir_log("INFO",f"Resultado encontrado en{archivo_a_analizar}",f"... y {len(resultados) - 10} más.",tiempo,"Analyzer","analyzer")
                    break
            
            # Generar Estadísticas
            conteo = {}
            for item in resultados:
                valor = item['valor']
                conteo[valor] = conteo.get(valor, 0) + 1 # Forma corta de contar
            
            print("\n--- Resumen de Frecuencias (Top 5) ---")
            mas_comunes = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for valor, cantidad in mas_comunes:
                utils.escribir_log("INFO","Frecuencia",f"'{valor}' aparece {str(cantidad) + " vez" if cantidad == 1 else str(cantidad) + " veces" } en {archivo_a_analizar}",tiempo,"Analyzer","analyzer")
                
        else:
            utils.escribir_log("WARM",f"No se encontraron coincidencias en {archivo_a_analizar}"," ",tiempo,"Analyzer","analyzer")
        
        # PREGUNTA CLAVE
        continuar = input("\n¿Quieres buscar OTRO patrón en este MISMO archivo? (s/n): ").strip().lower()
        if continuar != 's':
            break # Sale del bucle y vuelve al menú principal


def obtener_patrones():
    return {
        "1": {
            "nombre": "Correos Electrónicos 'hola@email.com'",
            "regex": r"[\w\.-]+@[\w\.-]+\.\w+"
        },
        "2": {
            "nombre": "Teléfonos '0414-1234567'",
            "regex": r"\d{4}-\d{7}" 
        },
        "3": {
            "nombre": "Fechas 'dd/mm/aaaa'",
            "regex": r"\d{2}/\d{2}/\d{4}"
        }, 
        "4": {
            "nombre": "Hastags '#programacion'",
            "regex": r"#[a-zA-Z0-9_]+"
        },
        "5" : {
            "nombre": "URls 'https://www.google.com/'",
            "regex" : r"(?:https?://|www\.)[\w.-]+\.[a-zA-Z]{2,}(?:/[\w\-._~:/?#[\]@!$&\'()*+,;=%]*)?"
        },
        "6" : {
            "nombre": "Precios '$1,500.00, 200 EUR, 50 dolares, Bs 500,00'",
            "regex" : r"(?:(?:US\$|C\$|\$|€|£|¥|Bs\.?|S/)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?\s?(?:\$|€|£|¥|Bs\.?|USD|EUR|VES|MXN|dólares|dolares|euros|bolívares|bolivares|pesos)\b)"
        },
        "7" :{
            "nombre": "Ips '8.8.8.8'",
            "regex" : r"\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"           
        },
        "8" : {
            "nombre": "Palabra personalizada 'hola'",
            "regex" : None
        }
    }
    


#GENERADOR
def leer_archivo_eficiente(ruta_archivo,tiempo):
    try:
        # Abrimos el archivo
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
            for linea in archivo:
                yield linea  # <--- Esto entrega la línea y pausa (Generador)
    except FileNotFoundError:
        utils.escribir_log("ERROR",f"Error archivo no encontrado en: {ruta_archivo}",f"No se encontró el archivo: {ruta_archivo}",tiempo,"Analyzer","analyzer")
    except Exception as e:
        utils.escribir_log("ERROR",f" Error leyendo el archivo en: {ruta_archivo}",f"Error : {e}",tiempo,"Analyzer","analyzer")

#FUNCIÓN PRINCIPAL DEL ANALIZADOR
def analizador_archivos(ruta_archivo, opcion,tiempo):
    patrones = obtener_patrones()
    
    if opcion not in patrones:
        print("Esa opción no está disponible")
        return []
    if opcion == "8":
        palabra = input("Ingrese la palabra a buscar:")
        regex_seleccionado = fr"\b{re.escape(palabra)}\b"
        nombre_patron = f"Palabra {palabra}"
    else:    
        regex_seleccionado = patrones[opcion]["regex"]
        nombre_patron = patrones[opcion]["nombre"]
    
    print(f"Analizando '{os.path.basename(ruta_archivo)}' buscando {nombre_patron}...")
    
    resultados = []

    
  
    generador = leer_archivo_eficiente(ruta_archivo,tiempo)
    
    # Recorremos el generador línea por línea
    for numero_linea, linea in enumerate(generador, 1):
        
        # Buscamos coincidencias en esa línea específica
        encontrados = re.findall(regex_seleccionado, linea)
        
        if encontrados:
            for hallazgo in encontrados:
                resultados.append({
                    "linea": numero_linea,
                    "valor": hallazgo,
                    "tipo": nombre_patron
                })

    return resultados