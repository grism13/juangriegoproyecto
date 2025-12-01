import sys
import utils  # Importamos tus herramientas
import datetime
import auditor
import organizer
import analyzer
import reports
import os


# Por ahora los dejaremos comentados o simularemos que funcionan.

carpeta = "./test_samples" #carpeta de ejemplo

def mostrar_menu_principal():
    """Despliega las opciones del sistema."""
    utils.mostrar_encabezado("KIT DE AUTOMATIZACIÓN DE ARCHIVOS (v1.0)")
    print("Hola! Soy Capitán Folder y estoy aquí para ayudare a combatir contra el desorden, dime que opción deseas y empezamos")
    print(f"Carpeta=  {carpeta}")
    print("1. [ORGANIZADOR] :  Clasificar y ordenar archivos")
    print("2. [ANALIZADOR] :  Buscar patrones y contenido")
    print("3. [AUDITOR]  :    Detectar cambios en carpetas")
    print("4. [REPORTES]  :   Generar informes (CSV/TXT)")
    print("5. CAMBIAR CARPETA")
    print("6. Salir")
    print("-" * 60)

def mostrar_menu_auditor():
    """Despliega las opciones del sistema."""
    utils.mostrar_encabezado("KIT DE AUDITORIA (v1.0)")
    print("1. Generar snapshot")
    print("2. Generar reporte")
    print("3. Salir")
    print("-" * 60)

def mostrar_menu_seleccion_carpeta():
    """Despliga el menu de carpetas"""
    utils.mostrar_encabezado("SELECCIONADOR DE CARPETAS (v1.0)")
    print(f"Carpeta actual: {carpeta}")
    print("1. Cambiar carpeta")
    print("2. Salir")
    print("-" * 60)

def main():
    global carpeta
    # Capturamos el tiempo de inicio UNA sola vez para pasar el mismo timestamp a todos
    tiempo_inicio = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    while True:
        mostrar_menu_principal()
        opcion = input(">> Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            # --- ORGANIZADOR ---
            print("\n--- MÓDULO ORGANIZADOR ---")
            # Ya no pedimos ruta aquí, usamos la variable 'carpeta' global
            print(f"Trabajando en: {carpeta}")
            
            opcion_org = organizer.pedir_opcion() # Eliezer debe asegurarse que esta función retorne "1", "2" o "3"

            if opcion_org == "1":
                organizer.organizar_archivos_por_espacio(carpeta)
            elif opcion_org == "2":
                organizer.organizar_archivos_por_extension(carpeta)
            elif opcion_org == "3":
                organizer.organizar_archivos_por_fecha(carpeta)
            else:
                print("Opción no válida en organizador.")

            # Registrar acción en auditoría (Opcional pero recomendado)
            auditor.escribir_log("INFO", "Ejecutado Organizador", f"Opción={opcion_org}", tiempo_inicio)
            input("Presione ENTER para continuar...")
            
        elif opcion == "2":
            # --- ANALIZADOR ---
            # Si Roand tiene su función lista:
            # analyzer.iniciar_analizador(carpeta)
            print("\n🚧 Módulo del Analizador (Roand) en construcción...")
            input("Presiona Enter para volver...")

        elif opcion == "3":
            # --- AUDITOR ---
            while True:
                mostrar_menu_auditor()
                op_aud = input(">> Selecciona una opción (1-3): ").strip()
                
                if op_aud == "1":
                    auditor.generar_snapshot(carpeta, tiempo_inicio)
                    input("Snapshot generado. Enter para continuar...")
                elif op_aud == "2":
                    auditor.generar_reporte(carpeta, tiempo_inicio)
                    input("Reporte de cambios generado. Enter para continuar...")
                elif op_aud == "3":
                    break
                else:
                    print("Opción no válida.")

        elif opcion == "4":
            # --- REPORTES ---
            # Llamamos a la función principal de Juan
            # Le pasamos None por ahora porque no estamos guardando datos en memoria
            # Pero su módulo sabe leer el audit.log
            reports.iniciar_modulo_reportes() 
            input("Presiona Enter para volver...")

        elif opcion == "5":
            #Menu para cambiar la carpeta
            while True:
                mostrar_menu_seleccion_carpeta()
                opcion = input(">> Selecciona una opción (1-2): ").strip()
                if opcion == "1":
                    while True:
                        utils.limpiar_pantalla()
                        ruta = input("Introduzca la ruta de la carpeta:")
                        if os.path.exists(ruta) and ruta not in ["./","./logs","./env"]:
                            carpeta = ruta 
                            break
                        else:
                            input("Opción no Valida , presione enter para continuar...")
                            continue
                elif opcion == "2":
                    input("Saliendo, press enter para continuar...")
                    break
                else:
                    print("\n❌ Error: Opción no válida.")
                    input("Presiona Enter para intentar de nuevo...")
                    
                    


        elif opcion == "6":
            print("\n¡Hasta luego! Cerrando sistema...")
            break
        
        else:
            print("\n❌ Error: Opción no válida.")
            input("Presiona Enter para intentar de nuevo...")

if __name__ == "__main__":
    main()