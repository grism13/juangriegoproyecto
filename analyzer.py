import re
import os
import utils

def menu_analizador():
   
    carpeta = input("Ingresa la ruta de la carpeta (Enter para actual): ").strip()
    if not carpeta: carpeta = "./test_samples"
    
    if not os.path.exists(carpeta):
        print("Esa carpeta no existe.")
        return

    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    if not archivos:
        print("Carpeta vacía.")
        return

    utils.mostrar_encabezado("Selecciona un archivo")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    seleccion = input("\nElige el número del archivo: ")
    if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(archivos):
        print("Opción inválida.")
        return
    
    
    archivo_a_analizar = os.path.join(carpeta, archivos[int(seleccion)-1])

   
    while True:
        utils.mostrar_encabezado(f"Analizando: {os.path.basename(archivo_a_analizar)}")
        
        print("¿Qué quieres extraer?")
        patrones = obtener_patrones() 
        for clave, valor in patrones.items():
            print(f"{clave}. {valor['nombre']}")
        
        opcion = input("\nElige una opción (1-4): ")
        
        
        resultados = analizador_archivos(archivo_a_analizar, opcion)
        
        # --- MOSTRAR RESULTADOS Y RESUMEN ---
        if resultados:
            print(f"\n--- Resultados Encontrados ({len(resultados)}) ---")
            
            # Mostrar detalle (limitado a 10)
            for i, item in enumerate(resultados):
                if i < 10:
                    print(f"Línea {item['linea']}: {item['valor']}")
                else:
                    print(f"... y {len(resultados) - 10} más.")
                    break
            
            # Generar Estadísticas
            conteo = {}
            for item in resultados:
                valor = item['valor']
                conteo[valor] = conteo.get(valor, 0) + 1 # Forma corta de contar
            
            print("\n--- Resumen de Frecuencias (Top 5) ---")
            mas_comunes = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for valor, cantidad in mas_comunes:
                print(f"'{valor}' aparece {cantidad} veces.")
                
        else:
            print("No se encontraron coincidencias.")
        
        # PREGUNTA CLAVE
        continuar = input("\n¿Quieres buscar OTRO patrón en este MISMO archivo? (s/n): ").strip().lower()
        if continuar != 's':
            break # Sale del bucle y vuelve al menú principal


def obtener_patrones():
    return {
        "1": {
            "nombre": "Correos Electrónicos",
            "regex": r"[\w\.-]+@[\w\.-]+\.\w+"
        },
        "2": {
            "nombre": "Teléfonos (Ej. 0414-1234567)",
            "regex": r"\d{4}-\d{7}" 
        },
        "3": {
            "nombre": "Fechas (dd/mm/aaaa)",
            "regex": r"\d{2}/\d{2}/\d{4}"
        }, 
        "4": {
            "nombre": "Palabra ''",
            "regex": r"\b\b"
        }
    }
    


#GENERADOR
def leer_archivo_eficiente(ruta_archivo):
    try:
        # Abrimos el archivo
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as archivo:
            for linea in archivo:
                yield linea  # <--- Esto entrega la línea y pausa (Generador)
    except FileNotFoundError:
        print(f" Error: No se encontró el archivo: {ruta_archivo}")
    except Exception as e:
        print(f" Error leyendo el archivo: {e}")

#FUNCIÓN PRINCIPAL DEL ANALIZADOR
def analizador_archivos(ruta_archivo, opcion):
    patrones = obtener_patrones()
    
    if opcion not in patrones:
        print("Esa opción no está disponible")
        return []

    regex_seleccionado = patrones[opcion]["regex"]
    nombre_patron = patrones[opcion]["nombre"]
    
    print(f"Analizando '{os.path.basename(ruta_archivo)}' buscando {nombre_patron}...")
    
    resultados = []

    
  
    generador = leer_archivo_eficiente(ruta_archivo)
    
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