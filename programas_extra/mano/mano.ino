#include <Servo.h>

Servo pulgar;
Servo indice;
Servo medio;
Servo anular;
Servo menique;

 // Pin al que está conectado el servo
int angle = 0;    // Ángulo inicial del servo

void setup() {
  Serial.begin(9600); // Iniciar comunicación serial
  pulgar.attach(11);
  indice.attach(7);
  medio.attach(8); // probado
  anular.attach(5); //probado
  menique.attach(10); // Adjuntar el servo al pin
  pulgar.write(angle); // Mover el servo al ángulo inicial
  indice.write(angle);
  medio.write(angle); // 50 es su 0
  anular.write(angle); // pin 5
  menique.write(angle);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Leer el comando recibido

    switch (command) {
      case 'q': // Comando cerrar
        pulgar.write(140); 
        indice.write(100);
        medio.write(150);
        anular.write(100); 
        menique.write(100);
        break;

      case 'w': // Comando 'd' para disminuir el ángulo
        pulgar.write(100); 
        indice.write(100);
        medio.write(angle);
        anular.write(100); 
        menique.write(100);
        break;

      case 'e': // Comando 'd' para disminuir el ángulo
        pulgar.write(100); 
        indice.write(100);
        medio.write(angle);
        anular.write(angle); 
        menique.write(angle);
        break;

      case 'r': // Comando 'd' para disminuir el ángulo
        pulgar.write(angle); 
        indice.write(angle);
        medio.write(angle);
        anular.write(100); 
        menique.write(100);
        break;
      
      case 't': // Comando 'd' para disminuir el ángulo
        pulgar.write(angle); 
        indice.write(angle);
        medio.write(angle);
        anular.write(angle); 
        menique.write(angle);
        break;

      default:
        // No hacer nada para otros comandos
        break;
    }
  }
}