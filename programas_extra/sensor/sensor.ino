int emgPin = A3; // Pin analógico donde está conectado el sensor EMG

void setup() {
  Serial.begin(9600); // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  int emgValue = analogRead(emgPin); // Lee el valor del sensor EMG
  Serial.println(emgValue); // Envía el valor a través del puerto serial
  delay(15); // Pequeño retardo
}
