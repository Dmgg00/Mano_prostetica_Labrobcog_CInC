import os
import numpy as np
import pandas as pd


# Función para obtener la altura y el ancho del pico más alto
def get_peak_features(file_path):
    data = np.loadtxt(file_path)

    # Estimación del nivel de ruido (valor medio de los primeros y últimos 10 valores)
    noise_level = (np.mean(data[:10]) + np.mean(data[-10:])) / 2

    # Altura del pico (diferencia entre el valor máximo y el nivel de ruido)
    peak_value = np.max(data)
    peak_height = peak_value - noise_level

    # Ancho del pico (rango de índices desde donde empieza a subir por encima del ruido hasta que baja de nuevo)
    #peak_start = np.argmax(data > noise_level + 5)
    #peak_end = len(data) - np.argmax(data[::-1] > noise_level + 5) - 1
    #peak_width = peak_end - peak_start

    print(
        f"Archivo: {file_path}, Nivel de ruido: {noise_level}, Altura del Pico: {peak_height}")
        #f"Archivo: {file_path}, Nivel de ruido: {noise_level}, Altura del Pico: {peak_height}, Ancho del Pico: {peak_width}")
    return peak_height #, peak_width


# Directorios que contienen los archivos
directories = {
    'cerrar': 'C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/datos_final/cerrar_cortados',
    'corazon': 'C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/datos_final/corazon_cortados',
    'deditos': 'C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/datos_final/deditos_cortados',
    '4dedos': 'C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/Datos por modificar/datos_final/4dedos_cortados'
}

# Lista para guardar los datos
all_data = []

# Procesamiento de cada directorio y archivo
for label, dir_path in directories.items():
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        peak_height = get_peak_features(file_path)
        #peak_height, peak_width = get_peak_features(file_path)
        all_data.append([label, peak_height])
        #all_data.append([label, peak_height, peak_width])

# Creación del DataFrame y guardado en archivo CSV
df = pd.DataFrame(all_data, columns=['label', 'peak_height'])
#df = pd.DataFrame(all_data, columns=['label', 'peak_height', 'peak_width'])
df.to_csv('emg_features.csv', index=False)
print("Extracción de características completada y guardada en emg_features.csv")
