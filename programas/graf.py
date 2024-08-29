import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

#prueba
# Variable global para almacenar los datos de múltiples archivos
datos_archivos = {}

# Lista de colores para las gráficas
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']

# Variables para el desplazamiento con el mouse
press = None
x0 = None
y0 = None

# Función para leer los datos del archivo de texto
def leer_datos(archivo):
    valores = []
    delta = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                try:
                    valor = float(linea.strip())
                    valores.append(valor)
                    pibote = valores[0]
                    temp= valor - pibote
                    delta.append(temp)
                except ValueError as e:
                    print(f"Error al convertir la línea a float: {linea.strip()} - {e}")
    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {archivo} - {e}")
    return valores

# Función para actualizar la gráfica en el intervalo seleccionado
def actualizar_grafica():
    inicio = int(entry_inicio.get())
    fin = int(entry_fin.get())
    marker = marker_var.get()
    linestyle = linestyle_var.get()
    zoom_factor = zoom_var.get()

    if not datos_archivos:
        print("No se han cargado archivos.")
        return

    ax.clear()

    lineas = []
    etiquetas = []

    # Graficar cada archivo con un color diferente
    for idx, (nombre_archivo, valores) in enumerate(datos_archivos.items()):
        if inicio < 0 or fin >= len(valores) or inicio > fin:
            print(f"Intervalo no válido para {nombre_archivo}")
            continue

        tiempos = list(range(len(valores)))
        intervalo_valores = valores[inicio:fin+1]
        color = colors[idx % len(colors)]  # Asignar un color diferente a cada gráfica
        linea, = ax.plot(tiempos[inicio:fin+1], intervalo_valores, color=color, marker=marker, linestyle=linestyle, label=nombre_archivo)
        lineas.append(linea)
        etiquetas.append(nombre_archivo)

    ax.set_title('Comparación de Series de Números respecto al Tiempo')
    ax.set_xlabel('Tiempo (índice)')
    ax.set_ylabel('Valor')
    ax.grid(True)
    ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas del eje X

    # Ajustar el zoom
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.set_xlim([xlim[0], xlim[0] + (xlim[1] - xlim[0]) / zoom_factor])
    ax.set_ylim([ylim[0], ylim[0] + (ylim[1] - ylim[0]) / zoom_factor])

    # Hacer la gráfica interactiva con mplcursors
    cursor = mplcursors.cursor(ax, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]}, {sel.target[1]:.2f})'))

    canvas.draw()

    # Actualizar la lista de leyenda
    listbox_legend.delete(0, tk.END)
    for etiqueta in etiquetas:
        listbox_legend.insert(tk.END, etiqueta)

    # Función para resaltar la línea seleccionada
    def resaltar_linea(event):
        seleccion = listbox_legend.curselection()
        if seleccion:
            idx = seleccion[0]
            for i, linea in enumerate(lineas):
                if i == idx:
                    linea.set_linewidth(4)
                    linea.set_alpha(1)
                else:
                    linea.set_linewidth(1)
                    linea.set_alpha(0.3)
            canvas.draw()

    # Vincular la función de resaltado a la selección de la lista de leyenda
    listbox_legend.bind('<<ListboxSelect>>', resaltar_linea)

# Función para cargar los archivos
def cargar_archivos():
    global datos_archivos
    archivos = filedialog.askopenfilenames()
    for archivo in archivos:
        nombre_archivo = archivo.split('/')[-1]
        valores = leer_datos(archivo)
        datos_archivos[nombre_archivo] = valores
    label_archivos.config(text=f"{len(archivos)} archivos cargados")
    actualizar_grafica()

# Función para eliminar archivos seleccionados de la gráfica
def eliminar_archivo():
    seleccion = listbox_legend.curselection()
    if seleccion:
        idx = seleccion[0]
        nombre_archivo = listbox_legend.get(idx)
        del datos_archivos[nombre_archivo]
        listbox_legend.delete(idx)
        actualizar_grafica()

# Funciones para el desplazamiento con el mouse
def on_press(event):
    global press, x0, y0
    press = True
    x0, y0 = event.xdata, event.ydata

def on_release(event):
    global press
    press = False

def on_motion(event):
    global press, x0, y0
    if press:
        dx = event.xdata - x0
        dy = event.ydata - y0
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
        canvas.draw()

# Función para mover las gráficas a un punto en el eje Y
def mover_a_y():
    try:
        nuevo_y = float(entry_mover_y.get())
        for nombre_archivo, valores in datos_archivos.items():
            diferencia = nuevo_y - valores[0]  # Calcular la diferencia para desplazar los valores
            datos_archivos[nombre_archivo] = [v + diferencia for v in valores]
        actualizar_grafica()
    except ValueError:
        print("Por favor, introduce un valor numérico válido.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Graficar Intervalo de Tiempo")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_archivos = ttk.Label(frame, text="No se han cargado archivos")
label_archivos.grid(row=0, column=0, columnspan=3, pady=(0, 10))

btn_cargar = ttk.Button(frame, text="Cargar Archivos", command=cargar_archivos)
btn_cargar.grid(row=1, column=0, pady=(0, 10))

label_inicio = ttk.Label(frame, text="Inicio:")
label_inicio.grid(row=2, column=0, pady=(0, 10))

entry_inicio = ttk.Entry(frame, width=10)
entry_inicio.grid(row=2, column=1, pady=(0, 10))

label_fin = ttk.Label(frame, text="Fin:")
label_fin.grid(row=3, column=0, pady=(0, 10))

entry_fin = ttk.Entry(frame, width=10)
entry_fin.grid(row=3, column=1, pady=(0, 10))

# Opciones de marker y linestyle
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', '+', 'x', '|', '_', ' ']
linestyles = ['-', '--', '-.', ':']

marker_var = tk.StringVar(value=markers[0])
linestyle_var = tk.StringVar(value=linestyles[0])

label_marker = ttk.Label(frame, text="Marker:")
label_marker.grid(row=4, column=0, pady=(0, 10))

combo_marker = ttk.Combobox(frame, textvariable=marker_var, values=markers)
combo_marker.grid(row=4, column=1, pady=(0, 10))

label_linestyle = ttk.Label(frame, text="Linestyle:")
label_linestyle.grid(row=5, column=0, pady=(0, 10))

combo_linestyle = ttk.Combobox(frame, textvariable=linestyle_var, values=linestyles)
combo_linestyle.grid(row=5, column=1, pady=(0, 10))

btn_actualizar = ttk.Button(frame, text="Actualizar Gráfica", command=actualizar_grafica)
btn_actualizar.grid(row=6, column=0, columnspan=2, pady=(10, 0))

btn_eliminar = ttk.Button(frame, text="Eliminar Archivo", command=eliminar_archivo)
btn_eliminar.grid(row=6, column=2, pady=(10, 0))

# Barra de zoom
label_zoom = ttk.Label(frame, text="Zoom:")
label_zoom.grid(row=7, column=0, pady=(0, 10))

zoom_var = tk.DoubleVar(value=1.0)
scale_zoom = ttk.Scale(frame, variable=zoom_var, from_=1, to_=10, orient=tk.HORIZONTAL, command=lambda x: actualizar_grafica())
scale_zoom.grid(row=7, column=1, pady=(0, 10))

# Entrada y botón para mover las gráficas a un punto en el eje Y
label_mover_y = ttk.Label(frame, text="Mover a Y:")
label_mover_y.grid(row=8, column=0, pady=(0, 10))

entry_mover_y = ttk.Entry(frame, width=10)
entry_mover_y.grid(row=8, column=1, pady=(0, 10))

btn_mover_y = ttk.Button(frame, text="Mover", command=mover_a_y)
btn_mover_y.grid(row=8, column=2, pady=(0, 10))

# Crear la figura de matplotlib y el canvas
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=9, column=0, columnspan=3, padx=10, pady=10)

# Conectar los eventos de mouse para el desplazamiento
canvas.mpl_connect('button_press_event', on_press)
canvas.mpl_connect('button_release_event', on_release)
canvas.mpl_connect('motion_notify_event', on_motion)

# Crear la lista de leyenda
listbox_legend = tk.Listbox(root, height=10)
listbox_legend.grid(row=9, column=3, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()
