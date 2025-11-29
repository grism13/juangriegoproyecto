import sys
import utils  # Importamos tus herramientas

# Estos imports darán error hasta que tus compañeros creen sus funciones.
# Por ahora los dejaremos comentados o simularemos que funcionan.
# import organizer
# import analyzer
# import auditor
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

def main():
    while True:
        mostrar_menu_principal()
        opcion = input(">> Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            # Aquí llamaremos a: organizer.iniciar()
            print("\n🚧 Módulo del Organizador (Eliezer) en construcción...")
            input("Presiona Enter para volver...")

        elif opcion == "2":
            # Aquí llamaremos a: analyzer.iniciar()
            print("\n🚧 Módulo del Analizador (Roand) en construcción...")
            input("Presiona Enter para volver...")

        elif opcion == "3":
            # Aquí llamaremos a: auditor.iniciar()
            print("\n🚧 Módulo del Auditor (Gabriel) en construcción...")
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

if __name__ == "__main__":
    main()