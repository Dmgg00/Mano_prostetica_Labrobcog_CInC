import serial
import time

# Configura el puerto serie
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto serie correcto
time.sleep(2)  # Espera a que el puerto serie se inicialice

start_time = time.time()
file_counter = 0

def create_new_file():
    print("iniciando grabacion")
    time.sleep(0.5)
    global file_counter
    file_counter += 1
    filename = f'deditos{file_counter}.txt'
    return open(filename, 'w')

# Abre el primer archivo
file = create_new_file()

try:
    while True:
        current_time = time.time()
        if current_time - start_time >= 5:
            # Cerrar el archivo actual y abrir uno nuevo
            print("finalizando grabacion")
            time.sleep(0.5)
            file.close()
            file = create_new_file()
            start_time = current_time

        if ser.in_waiting:
            emg_value = ser.readline().decode('utf-8', errors='ignore').strip()
            print(emg_value)
            file.write(emg_value + '\n')
            file.flush()  # Asegúrate de que los datos se escriban inmediatamente en el archivo

        time.sleep(0.01)  # Ajusta el retraso según tus necesidades

except KeyboardInterrupt:
    print("Finalizando la captura de datos")
finally:
    file.close()
    ser.close()
