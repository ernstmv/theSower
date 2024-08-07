const int pinServo = 11; // Pin de salida del servomotor
int angulo = 0; // Ángulo deseado del servomotor
int pulsoMinimo = 1000; // Pulso mínimo para -90 grados en microsegundos
int pulsoMaximo = 2000; // Pulso máximo para 90 grados en microsegundos
int pulsoAncho; // Ancho del pulso en microsegundos

void setup() {
  pinMode(pinServo, OUTPUT); // Configura el pin del servomotor como salida
  Serial.begin(9600); // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  if (Serial.available() > 0) {
    angulo = Serial.parseInt(); // Lee el ángulo desde el puerto serie
    if (angulo >= -90 && angulo <= 90) {
      pulsoAncho = map(angulo, -90, 90, pulsoMinimo, pulsoMaximo); // Mapea el ángulo al ancho del pulso
      generarPulso(pulsoAncho); // Genera el pulso de ancho variable
      Serial.print("Moviendo el servomotor a: ");
      Serial.println(angulo);
      Serial.println(pulsoAncho);
    } else {
      Serial.println("Ángulo fuera de rango. Introduzca un valor entre -90 y 90.");
    }
  }
  delay(15); // Espera para que el servomotor complete el movimiento
}

void generarPulso(int anchoPulso) {
  digitalWrite(pinServo, HIGH); // Inicia el pulso
  delayMicroseconds(anchoPulso); // Mantiene el pulso por el tiempo especificado
  digitalWrite(pinServo, LOW); // Finaliza el pulso
  delay(20 - (anchoPulso / 1000)); // Espera el resto del ciclo de 20 ms
}
