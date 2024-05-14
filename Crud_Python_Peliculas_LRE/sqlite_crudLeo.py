# Importa el módulo sqlite3 para interactuar con la base de datos SQLite
import sqlite3

# Definición de la función para mostrar todos los registros de la tabla 'peliculas' en la base de datos
def mostrar_registros():
    # Conecta a la base de datos 'cine.db'
    conexion = sqlite3.connect("cine.db")
    # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor = conexion.cursor()
    # Ejecuta una consulta para seleccionar todos los registros de la tabla 'peliculas'
    cursor.execute("SELECT * FROM peliculas")
    # Obtiene todos los registros seleccionados
    registros = cursor.fetchall()
    # Cierra la conexión a la base de datos
    conexion.close()

    # Verifica si hay registros para mostrar
    if registros:
        # Si hay registros, itera sobre cada uno e imprímelo
        for registro in registros:
            print(registro)
    else:
        # Si no hay registros, imprime un mensaje indicando que no hay registros en la tabla 'peliculas'
        print("No hay registros en la tabla 'peliculas'")

# Llama a la función 'mostrar_registros' para mostrar los registros de la tabla 'peliculas'
mostrar_registros()