import os
import numpy as np
import pandas as pd

# Función para obtener la amplitud y altura del pico más alto
def get_peak_features(file_path):
    data = np.loadtxt(file_path)
    peak_amplitude = np.max(data)
    peak_height = np.argmax(data)
    print(f"Archivo: {file_path}, Amplitud del Pico: {peak_amplitude}, Altura del Pico: {peak_height}")
    return peak_amplitude, peak_height

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
        peak_amplitude, peak_height = get_peak_features(file_path)
        all_data.append([label, peak_amplitude, peak_height])

# Creación del DataFrame y guardado en archivo CSV
df = pd.DataFrame(all_data, columns=['label', 'peak_amplitude', 'peak_height'])
df.to_csv('emg_features.csv', index=False)
print("Extracción de características completada y guardada en emg_features.csv")
