#gracias gemini por facilitarme un simulacro de prueba JAJAJAJAJA
import reports
import os

# --- SIMULACIÓN DE DATOS TEMPORALES ---
# Imaginemos que el usuario ya corrió la opción "Organizar" y "Analizar"
# y el programa principal tiene estos datos en memoria:

datos_org_simulados = [
    {"Archivo": "foto.jpg", "Accion": "Movido", "Destino": "/Imagenes"},
    {"Archivo": "tesis.doc", "Accion": "Ignorado", "Destino": "N/A"}
]

datos_ana_simulados = [
    {"Archivo": "datos.txt", "Patron": "Email", "Hallazgo": "juan@gmail.com", "Linea": 10},
    {"Archivo": "datos.txt", "Patron": "Telf", "Hallazgo": "0414-1234567", "Linea": 15}
]

# Crear un audit.log falso si no existe para probar la opción 3
if not os.path.exists("audit.log"):
    with open("audit.log", "w") as f:
        f.write("[2023-11-28 10:00:00] INICIO: Sistema arrancado.\n")
        f.write("[2023-11-28 10:05:00] ORG: Se organizaron 2 archivos.\n")

# --- EJECUTAR EL FLUJO ---
print("Iniciando simulación del menú principal...")

# Llamamos a la función principal del módulo reportes pasando los datos simulados
reports.iniciar_modulo_reportes(
    datos_organizacion_temp=datos_org_simulados,
    datos_analisis_temp=datos_ana_simulados
)

print("\nVolvimos al menú principal simulado. Fin de la prueba.")