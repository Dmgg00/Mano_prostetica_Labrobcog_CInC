import os
import numpy as np

# Definir la carpeta de entrada y la carpeta de salida
# input_folder = ('C:/Users/emili/OneDrive/Escritorio/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/nuevos_datos/corazon')
# output_folder = ('C:/Users/emili/OneDrive/Escritorio/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/nuevos_datos/corazon_cut')

input_folder = ('C:/Users/Lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/nuevos_datos/deditos_nuevos')
output_folder = ('C:/Users/Lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/nuevos_datos/deditos_nuevos_cut')

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Obtener la lista de archivos en la carpeta de entrada
file_names = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for file_name in file_names:
    input_file_path = os.path.join(input_folder, file_name)

    # Leer el archivo y convertir a una lista de números enteros
    with open(input_file_path, 'r') as file:
        data = [int(line.strip()) for line in file if line.strip().isdigit()]

    # Encontrar el índice del valor máximo
    max_index = np.argmax(data)

    # Obtener los 40 valores anteriores y 40 posteriores
    start_index = max(0, max_index - 40)
    end_index = min(len(data), max_index + 41)  # 41 porque el índice final es exclusivo

    selected_data = data[start_index:end_index]

    # Guardar los valores en un nuevo archivo en la carpeta de salida
    output_file_path = os.path.join(output_folder, f'cut_{file_name}')
    with open(output_file_path, 'w') as file:
        for value in selected_data:
            file.write(f"{value}\n")

    print(f"Los valores cercanos al pico del archivo {file_name} se han guardado en: {output_file_path}")

print("Proceso completado.")
