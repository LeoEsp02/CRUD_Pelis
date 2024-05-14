import tkinter as tk
from tkinter import ttk, messagebox  # Importa tkinter y sus módulos ttk y messagebox para la interfaz gráfica
import sqlite3  # Importa sqlite3 para la base de datos SQLite

# Función para crear la tabla 'peliculas' en la base de datos si no existe
def crear_tabla():
    conexion = sqlite3.connect("cine.db")  # Conecta a la base de datos 'cine.db'
    cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL
    # Ejecuta una consulta para crear la tabla si no existe, con columnas para título, director, duración, clasificación y género
    cursor.execute("CREATE TABLE IF NOT EXISTS peliculas (id INTEGER PRIMARY KEY, titulo TEXT, director TEXT, duracion INTEGER, clasificacion TEXT, genero TEXT)")
    conexion.commit()  # Guarda los cambios en la base de datos
    conexion.close()  # Cierra la conexión a la base de datos

# Función para agregar una nueva película a la base de datos
def agregar_pelicula():
    # Obtiene los valores ingresados en los campos de entrada
    titulo = entrada_titulo.get()
    director = entrada_director.get()
    duracion = entrada_duracion.get()
    clasificacion = entrada_clasificacion.get()
    genero = entrada_genero.get()

    # Verifica que todos los campos estén completos
    if titulo != "" and director != "" and duracion != "" and clasificacion != "" and genero != "":
        conexion = sqlite3.connect("cine.db")  # Conecta a la base de datos 'cine.db'
        cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL
        # Inserta una nueva fila en la tabla 'peliculas' con los valores ingresados
        cursor.execute("INSERT INTO peliculas (titulo, director, duracion, clasificacion, genero) VALUES (?, ?, ?, ?, ?)", (titulo, director, duracion, clasificacion, genero))
        conexion.commit()  # Guarda los cambios en la base de datos
        conexion.close()  # Cierra la conexión a la base de datos
        messagebox.showinfo("Éxito", "Película agregada correctamente")  # Muestra un mensaje de éxito
        limpiar_campos()  # Limpia los campos de entrada
        mostrar_peliculas()  # Actualiza la lista de películas mostrada
    else:
        messagebox.showerror("Error", "Por favor completa todos los campos")  # Muestra un mensaje de error si algún campo está vacío

# Función para mostrar todas las películas en la lista de películas
def mostrar_peliculas():
    lista_peliculas.delete(*lista_peliculas.get_children())  # Borra todas las filas actuales en la lista de películas
    conexion = sqlite3.connect("cine.db")  # Conecta a la base de datos 'cine.db'
    cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL
    cursor.execute("SELECT * FROM peliculas")  # Ejecuta una consulta para seleccionar todas las filas de la tabla 'peliculas'
    peliculas = cursor.fetchall()  # Obtiene todas las filas seleccionadas
    conexion.close()  # Cierra la conexión a la base de datos

    # Itera sobre todas las películas y las agrega a la lista de películas
    for pelicula in peliculas:
        lista_peliculas.insert("", tk.END, values=pelicula)

# Función para eliminar la película seleccionada de la base de datos
def eliminar_pelicula():
    seleccion = lista_peliculas.selection()  # Obtiene la película seleccionada en la lista de películas
    if seleccion:
        # Pregunta al usuario si está seguro de eliminar la película
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que quieres eliminar esta película?"):
            # Itera sobre todas las películas seleccionadas y las elimina de la base de datos
            for item in seleccion:
                pelicula = lista_peliculas.item(item, "values")  # Obtiene los valores de la película seleccionada
                conexion = sqlite3.connect("cine.db")  # Conecta a la base de datos 'cine.db'
                cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL
                # Ejecuta una consulta para eliminar la película con el ID correspondiente
                cursor.execute("DELETE FROM peliculas WHERE id=?", (pelicula[0],))
                conexion.commit()  # Guarda los cambios en la base de datos
                conexion.close()  # Cierra la conexión a la base de datos
            messagebox.showinfo("Éxito", "Película eliminada correctamente")  # Muestra un mensaje de éxito
            mostrar_peliculas()  # Actualiza la lista de películas mostrada
    else:
        messagebox.showerror("Error", "Por favor selecciona una película de la lista")  # Muestra un mensaje de error si no se selecciona ninguna película

# Función para limpiar los campos de entrada
def limpiar_campos():
    entrada_titulo.delete(0, tk.END)
    entrada_director.delete(0, tk.END)
    entrada_duracion.delete(0, tk.END)
    entrada_clasificacion.delete(0, tk.END)
    entrada_genero.delete(0, tk.END)

# Función para editar la película seleccionada
def editar_pelicula():
    seleccion = lista_peliculas.selection()  # Obtiene la película seleccionada en la lista de películas
    if seleccion:
        pelicula_seleccionada = lista_peliculas.item(seleccion, "values")  # Obtiene los valores de la película seleccionada
        ventana_editar = tk.Toplevel()  # Crea una nueva ventana para editar la película
        ventana_editar.title("Editar Película")  # Establece el título de la ventana
        ventana_editar.geometry("300x200")  # Establece las dimensiones de la ventana
        ventana_editar.configure(bg="#F5F5F5")  # Establece el color de fondo de la ventana

        # Crea etiquetas y campos de entrada para cada atributo de la película seleccionada
        ttk.Label(ventana_editar, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entrada_titulo_editar = ttk.Entry(ventana_editar)
        entrada_titulo_editar.grid(row=0, column=1, padx=5, pady=5)
        entrada_titulo_editar.insert(0, pelicula_seleccionada[1])

        ttk.Label(ventana_editar, text="Director:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entrada_director_editar = ttk.Entry(ventana_editar)
        entrada_director_editar.grid(row=1, column=1, padx=5, pady=5)
        entrada_director_editar.insert(0, pelicula_seleccionada[2])

        ttk.Label(ventana_editar, text="Duración (horas):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entrada_duracion_editar = ttk.Entry(ventana_editar)
        entrada_duracion_editar.grid(row=2, column=1, padx=5, pady=5)
        entrada_duracion_editar.insert(0, pelicula_seleccionada[3])

        ttk.Label(ventana_editar, text="Clasificación:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entrada_clasificacion_editar = ttk.Entry(ventana_editar)
        entrada_clasificacion_editar.grid(row=3, column=1, padx=5, pady=5)
        entrada_clasificacion_editar.insert(0, pelicula_seleccionada[4])

        ttk.Label(ventana_editar, text="Género:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        entrada_genero_editar = ttk.Entry(ventana_editar)
        entrada_genero_editar.grid(row=4, column=1, padx=5, pady=5)
        entrada_genero_editar.insert(0, pelicula_seleccionada[5])

        boton_guardar = ttk.Button(ventana_editar, text="Guardar Cambios", command=lambda: guardar_cambios(pelicula_seleccionada[0], entrada_titulo_editar.get(), entrada_director_editar.get(), entrada_duracion_editar.get(), entrada_clasificacion_editar.get(), entrada_genero_editar.get()))
        boton_guardar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    else:
        messagebox.showerror("Error", "Por favor selecciona una película de la lista")  # Muestra un mensaje de error si no se selecciona ninguna película

# Función para guardar los cambios realizados en la película
def guardar_cambios(id_pelicula, titulo, director, duracion, clasificacion, genero):
    if titulo != "" and director != "" and duracion != "" and clasificacion != "" and genero != "":
        conexion = sqlite3.connect("cine.db")  # Conecta a la base de datos 'cine.db'
        cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL
        # Ejecuta una consulta para actualizar los valores de la película con el ID correspondiente
        cursor.execute("UPDATE peliculas SET titulo=?, director=?, duracion=?, clasificacion=?, genero=? WHERE id=?", (titulo, director, duracion, clasificacion, genero, id_pelicula))
        conexion.commit()  # Guarda los cambios en la base de datos
        conexion.close()  # Cierra la conexión a la base de datos
        messagebox.showinfo("Éxito", "Cambios guardados correctamente")  # Muestra un mensaje de éxito
        mostrar_peliculas()  # Actualiza la lista de películas mostrada
    else:
        messagebox.showerror("Error", "Por favor completa todos los campos")  # Muestra un mensaje de error si algún campo está vacío

# Función para cerrar la aplicación
def salir():
    ventana.destroy()  # Cierra la ventana principal

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Catalogo de Movies: El Cinefilito Baneado")  # Establece el título de la ventana

# Establece el estilo para la ventana principal
ventana.configure(bg="#F5F5F5")

# Establece el estilo para la tabla de películas
estilo_tabla = ttk.Style()
estilo_tabla.theme_use("clam")
estilo_tabla.configure("Treeview", background="#F5F5F5", foreground="black", fieldbackground="#F5F5F5")
estilo_tabla.configure("Treeview.Heading", background="#B0E0E6", foreground="black", font=("Helvetica", 10, "bold"))

# Establece el estilo para los botones
estilo_botones = ttk.Style()
estilo_botones.theme_use("clam")
estilo_botones.configure("TButton", background="#FFA07A", foreground="black")

# Crear los widgets
formulario = ttk.Frame(ventana)
formulario.pack(padx=10, pady=10)

# Etiquetas y campos de entrada para cada atributo de la película
etiqueta_titulo = ttk.Label(formulario, text="Título:", background="#F5F5F5")
etiqueta_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entrada_titulo = ttk.Entry(formulario)
entrada_titulo.grid(row=0, column=1, padx=5, pady=5)

etiqueta_director = ttk.Label(formulario, text="Director:", background="#F5F5F5")
etiqueta_director.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entrada_director = ttk.Entry(formulario)
entrada_director.grid(row=1, column=1, padx=5, pady=5)

etiqueta_duracion = ttk.Label(formulario, text="Duración (horas):", background="#F5F5F5")
etiqueta_duracion.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entrada_duracion = ttk.Entry(formulario)
entrada_duracion.grid(row=2, column=1, padx=5, pady=5)

etiqueta_clasificacion = ttk.Label(formulario, text="Clasificación:", background="#F5F5F5")
etiqueta_clasificacion.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entrada_clasificacion = ttk.Entry(formulario)
entrada_clasificacion.grid(row=3, column=1, padx=5, pady=5)

etiqueta_genero = ttk.Label(formulario, text="Género:", background="#F5F5F5")
etiqueta_genero.grid(row=4, column=0, padx=5, pady=5, sticky="w")
entrada_genero = ttk.Entry(formulario)
entrada_genero.grid(row=4, column=1, padx=5, pady=5)

# Botones para agregar, eliminar, editar, limpiar y salir
boton_agregar = ttk.Button(formulario, text="Agregar Película", command=agregar_pelicula, style="TButton")
boton_agregar.grid(row=5, column=0, padx=5, pady=5, sticky="we")

boton_eliminar = ttk.Button(formulario, text="Eliminar Película", command=eliminar_pelicula, style="TButton")
boton_eliminar.grid(row=5, column=1, padx=5, pady=5, sticky="we")

boton_editar = ttk.Button(formulario, text="Editar Película", command=editar_pelicula, style="TButton")
boton_editar.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

boton_limpiar = ttk.Button(formulario, text="Limpiar Campos", command=limpiar_campos, style="TButton")
boton_limpiar.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

boton_salir = ttk.Button(ventana, text="Salir", command=salir, style="TButton")
boton_salir.pack(padx=10, pady=5, ipadx=5, ipady=5, fill="x")

# Lista de películas
lista_peliculas = ttk.Treeview(ventana, columns=("ID", "Título", "Director", "Duración (Horas)", "Clasificación", "Género"), show="headings")
lista_peliculas.pack(padx=10, pady=10, fill="both", expand=True)

# Encabezados de la lista de películas
lista_peliculas.heading("ID", text="ID")
lista_peliculas.heading("Título", text="Título")
lista_peliculas.heading("Director", text="Director")
lista_peliculas.heading("Duración (Horas)", text="Duración (Horas)")
lista_peliculas.heading("Clasificación", text="Clasificación")
lista_peliculas.heading("Género", text="Género")

# Crear la base de datos y mostrar las películas existentes
crear_tabla()
mostrar_peliculas()

# Ejecutar la aplicación
ventana.mainloop()
