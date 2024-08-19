#include "som_weights.h"
#include <Servo.h>

Servo pulgar;
Servo indice;
Servo medio;
Servo anular;
Servo menique;

int angle = 0; // Ángulo inicial del servo

const int emgPin = A3; // Pin analógico donde se conecta el sensor EMG
int threshold = 20; // Umbral para detectar un pico, ajusta según sea necesario
const int bufferSize = 300; // Tamaño del buffer para almacenar los datos del pico

int emgBuffer[bufferSize];
int bufferIndex = 0;
bool isPeakDetected = false;
bool isProcessing = false;
bool movimiento = false;

int som_x = 5;
int som_y = 5;

int winner_x = -1;
int winner_y = -1;

void setup() {
  Serial.begin(9600);
  attachServos();
  moveServosToInitialPosition();
  calibrateEMGSensor();
}

void loop() {
  int emgValue = analogRead(emgPin);
  Serial.println(emgValue);
  delay(15);
  if (emgValue > threshold) {
    detectPeak(emgValue);
  } else {
    if (isPeakDetected) {
      isProcessing = true; // Marcar que estamos procesando un pico
      for (int k = 0; k < bufferSize; k++)
      {
        //emgBuffer[k] = 0;
        Serial.print(emgBuffer[k]);
        Serial.println();
      }
      processPeak();
      for (int k = 0; k < bufferSize; k++)
      {
        //emgBuffer[k] = 0;
        Serial.print(", ");
        Serial.print(emgBuffer[k]);
        Serial.println();
      }
      delay(2000);
      calibrateEMGSensor();
      Serial.print(threshold);
      isPeakDetected = false;
    }
  }

  // Asegurarse de que los servos se mantengan en la posición inicial cuando no hay un pico
  if (!isPeakDetected && !isProcessing) {
    moveServosToInitialPosition();
    if (movimiento){
      delay(1000);
      movimiento = false;
    }
    
  }

  
}

void attachServos() {
  pulgar.attach(7);
  indice.attach(5);
  medio.attach(8);
  anular.attach(11);
  menique.attach(10);
}

void moveServosToInitialPosition() {
  pulgar.write(angle);
  indice.write(angle);
  medio.write(angle);
  anular.write(angle);
  menique.write(angle);
}

void calibrateEMGSensor() {
  int calibrationValue = 0;
  for (int i = 0; i < 200; i++) {
      analogRead(emgPin);
      delay(10);
    if(i > 99){
      calibrationValue += analogRead(emgPin);
      delay(10);
    }
  }
  threshold = (calibrationValue / 100); // Ajuste del umbral
}

void detectPeak(int emgValue) {
  if (!isPeakDetected) {
    bufferIndex = 0;
    isPeakDetected = true;
  }

  if (bufferIndex < bufferSize) {
    emgBuffer[bufferIndex] = emgValue;
    bufferIndex++;
  }
}

void processPeak() {
  float maxbuffervalue = findMaxBufferValue();
  float detected_peak_height = maxbuffervalue - threshold;
  float detected_peak_width = calculatePeakWidth();

  float input[2] = {detected_peak_height, detected_peak_width};
  findWinnerNeuron(input);

  printPeakData(detected_peak_height, detected_peak_width);
  resetBuffer();

  moveServosBasedOnWinnerNeuron();

  winner_x = -1;
  winner_y = -1;
  bufferIndex = 0;
  isProcessing = false; // Marcar que hemos terminado de procesar el pico
  movimiento = true;
  //delay(1000);
}

float findMaxBufferValue() {
  float maxbuffervalue = 0.0;
  for (int i = 0; i < bufferSize; i++) {
    if (emgBuffer[i] > maxbuffervalue) {
      maxbuffervalue = emgBuffer[i];
    }
  }
  return maxbuffervalue;
}

float calculatePeakWidth() {
  float width = 0;
  for (int i = 0; i < bufferSize; i++) {
    if (emgBuffer[i] > threshold) {
      width++;
    }
  }
  return width;
}

void findWinnerNeuron(float input[2]) {
  float min_dist = 1e6;
  for (int x = 0; x < som_x; x++) {
    for (int y = 0; y < som_y; y++) {
      float dist = euclidean_distance(input, som_weights[x][y]);
      if (dist < min_dist) {
        min_dist = dist;
        winner_x = x;
        winner_y = y;
      }
    }
  }
}

void printPeakData(float height, float width) {
  Serial.print("Winner neuron: (");
  Serial.print(winner_x);
  Serial.print(", ");
  Serial.print(winner_y);
  Serial.println(")");
  Serial.print("Weights: ");
  for (int i = 0; i < 2; i++) {
    Serial.print(som_weights[winner_x][winner_y][i]);
    if (i < 1) {
      Serial.print(", ");
    }
  }
  Serial.println();
  Serial.print(height);
  Serial.print(", ");
  Serial.print(width);
  Serial.println();
}

void resetBuffer() {
  for (int i = 0 ; i < bufferSize; i++) {
    emgBuffer[i] = 0;
  }
}

void moveServosBasedOnWinnerNeuron() {
  if ((winner_x == 0 && winner_y == 0) || (winner_x == 0 && winner_y == 1) || 
      (winner_x == 0 && winner_y == 2) || (winner_x == 1 && winner_y == 1) || 
      (winner_x == 1 && winner_y == 3) || (winner_x == 1 && winner_y == 4) || 
      (winner_x == 2 && winner_y == 1) || (winner_x == 2 && winner_y == 2) || 
      (winner_x == 3 && winner_y == 1) || (winner_x == 3 && winner_y == 4) || 
      (winner_x == 4 && winner_y == 1)) {
    // Corazon
    Serial.println("corazon");
    pulgar.write(100); 
    indice.write(100);
    medio.write(angle);
    anular.write(100); 
    menique.write(100);
  } else if ((winner_x == 0 && winner_y == 3) || (winner_x == 2 && winner_y == 3) || 
             (winner_x == 4 && winner_y == 3) || (winner_x == 4 && winner_y == 4)) {
    // 4 dedos
    Serial.println("4dedos");
    pulgar.write(angle); 
    indice.write(100);
    medio.write(150);
    anular.write(100); 
    menique.write(100);
  } else if ((winner_x == 0 && winner_y == 4) || (winner_x == 2 && winner_y == 0) || 
             (winner_x == 2 && winner_y == 4) || (winner_x == 3 && winner_y == 2) || 
             (winner_x == 4 && winner_y == 2)) {
    // Deditos
    Serial.println("deditos");
    pulgar.write(angle); 
    indice.write(angle);
    medio.write(angle);
    anular.write(100); 
    menique.write(100);
  } else if ((winner_x == 1 && winner_y == 0) || (winner_x == 1 && winner_y == 2) || 
             (winner_x == 3 && winner_y == 0) || (winner_x == 3 && winner_y == 3) || 
             (winner_x == 4 && winner_y == 0)) {
    // Cerrar
    Serial.println("cerrar");
    pulgar.write(140);
    indice.write(100);
    medio.write(150);
    anular.write(100);
    menique.write(100);
  } else {
    Serial.println("nada");
    moveServosToInitialPosition();
  }
}

float euclidean_distance(float a[2], float b[2]) {
  float sum = 0;
  for (int i = 0; i < 2; i++) {
    sum += (a[i] - b[i]) * (a[i] - b[i]);
  }
  return sqrt(sum);
}
