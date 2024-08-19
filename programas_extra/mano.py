import serial
import time

# Configurar la conexión serial (ajusta el puerto según sea necesario)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def send_command(command):
    arduino.write(bytes(command, 'utf-8'))
    time.sleep(0.05)  # Esperar un poco para que el comando se procese
    data = arduino.readline()
    return data

while True:
    command = input("q(cerrar), w(corazon), e(meñique), r(ok), t(restablecer), z (quit) ")
    if command == 'z':
        break
    response = send_command(command)
    print(response.decode('utf-8'))  # Decodificar la respuesta para imprimirla correctamente