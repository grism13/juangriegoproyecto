import re
import os
import utils


def menu_analizador() :
    utils.mostrar_encabezado("¿Qué quieres buscar?")
    
    carpeta = input("Donde vamos a buscar hoy? :")
    
# Verificamos si existe (usando os)
    if not os.path.isfile(carpeta):
        print("¡Epa! Ese archivo no existe, chamo. Revisa bien.")
        return []

   
    print("\n¿Qué quieres extraer hoy?")
    patrones = obtener_patrones() 
    
    for clave, valor in patrones.items():
        
        print(f"{clave}. {valor['nombre']}")
    
    # Pedir la opción
    opcion = input("Elige una opción (1-4): ")
    
    
    # Aquí llamamos a tu función principal
    resultados = analizador_archivos(carpeta, opcion)
    
    # Mostrar Resultados
    print(f"\n--- Resultados Encontrados ({len(resultados)}) ---")
    for item in resultados:
        print(f"Línea {item['linea']}: {item['valor']}")





def obtener_patrones():
    return {
        "1": {
            "nombre": "Correos Electrónicos",
            # patron correo electronico
            "regex": r"[\w\.-]+@[\w\.-]+\.\w+"
        },
        "2": {
            "nombre": "Teléfonos (Ej. 0414-1234567)",
            #patron numero de telefono
            "regex": r"\d{4}-\d{7}" 
        },
        "3": {
            "nombre": "Fechas (dd/mm/aaaa)",
            # fecha de archivo
            "regex": r"\d{2}/\d{2}/\d{4}"
        }, 
        "4": {
            "nombre": "Palabra Clave (Prueba)",
            # palabra importante que de el usuario
            "regex": r"\bIMPORTANTE\b"
        }
    }
    
    
def analizador_archivos(carpeta , opcion) :
    patrones = obtener_patrones()
    
    if opcion not in patrones :
        print("Esa opcion no esta disponible")
        return []

    regex_seleccionado = patrones[opcion]["regex"]
    
    nombre_patron = patrones[opcion]["nombre"]
    
    print(f"\n--- Analizando '{carpeta}' buscando {nombre_patron} ---")
    
    resultados = []
    
    try :
        with open(carpeta , 'r', encoding='utf-8') as archivo :
            
            numero_linea = 0
            
            for linea in archivo :
                
                numero_linea += 1
                
                encontrados = re.findall(regex_seleccionado, linea)
                
                if encontrados:
                    for hallazgo in encontrados:
                       
                        resultados.append({
                            "linea": numero_linea,
                            "valor": hallazgo,
                            "tipo": nombre_patron
                        })
    
    except FileNotFoundError:
        
        print(f"Chamo El archivo '{carpeta}' no existe.")
        return []
    
    except Exception as e:
        
        print(f"Error raro leyendo el archivo: {e}")
        return []

    return resultados
    
    
    