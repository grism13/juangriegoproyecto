import os
import platform

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