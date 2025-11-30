import sys
import utils  # Importamos tus herramientas
import datetime
import auditor
import organizer

# Estos imports darán error hasta que tus compañeros creen sus funciones.
# Por ahora los dejaremos comentados o simularemos que funcionan.
# import organizer
# import analyzer

# import reports

def mostrar_menu_principal():
    """Despliega las opciones del sistema."""
    utils.mostrar_encabezado("KIT DE AUTOMATIZACIÓN DE ARCHIVOS (v1.0)")
    print("1. [Organizador]  Clasificar y ordenar archivos")
    print("2. [Analizador]   Buscar patrones y contenido")
    print("3. [Auditor]      Detectar cambios en carpetas")
    print("4. [Reportes]     Generar informes (CSV/TXT)")
    print("5. Salir")
    print("-" * 60)

def mostrar_menu_auditor():
    """Despliega las opciones del sistema."""
    utils.mostrar_encabezado("KIT DE AUDITORIA (v1.0)")
    print("1. Generar snapshot")
    print("2. Generar reporte")
    print("3. Salir")
    print("-" * 60)

def main():
    tiempo_inicio = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
    while True:
        mostrar_menu_principal()
        opcion = input(">> Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            print("Iniciando Modulo Organizador...")
            #Se obtiene ruta y opcion de organizacion
            carpeta = organizer.pedir_ruta()
            opcion = organizer.pedir_opcion()

            if opcion == "1":
                organizer.organizar_archivos_por_espacio(carpeta)

            elif opcion == "2":
                organizer.organizar_archivos_por_extension(carpeta)
            
            elif opcion == "3":
                organizer.organizar_archivos_por_fecha(carpeta)

            else:
                print("Hubo un error en el sistema...")

            input("Presione ENTER para volver al inicio...")
            
        elif opcion == "2":
            # Aquí llamaremos a: analyzer.iniciar()
            print("\n🚧 Módulo del Analizador (Roand) en construcción...")
            input("Presiona Enter para volver...")

        elif opcion == "3":
            while True:
                mostrar_menu_auditor()
                opcion = input(">> Selecciona una opción (1-5): ").strip()
                if opcion == "1":
                    auditor.generar_snapshot("./test_samples",tiempo_inicio)
                    input("Presiona Enter para volver...")
                elif opcion == "2":
                    auditor.generar_reporte("./test_samples",tiempo_inicio)
                    input("Presiona Enter para volver...")
                elif opcion == "3":
                    break
                else:
                    print("\n❌ Error: Opción no válida.")
                    input("Presiona Enter para intentar de nuevo...")
            input("Presiona Enter para volver...")

        elif opcion == "4":
            # Aquí llamaremos a: reports.iniciar()
            print("\n🚧 Módulo de Reportes (Juan) en construcción...")
            input("Presiona Enter para volver...")

        elif opcion == "5":
            print("\n¡Hasta luego! Cerrando sistema...")
            break
        
        else:
            print("\n❌ Error: Opción no válida.")
            input("Presiona Enter para intentar de nuevo...")

