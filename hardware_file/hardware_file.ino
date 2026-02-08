#include <Servo.h>
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11 // Set to DHT11 for your specific sensor
#define WATER_LEVEL_PIN A1 
#define MQ_PIN A0
#define BUZZER_PIN 8 
#define SERVO_PIN 9

Servo probeServo;
DHT dht(DHTPIN, DHTTYPE);

int levels[] = {0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180};
bool isScanning = false;
int currentStep = 0;
unsigned long lastMoveTime = 0;
unsigned long lastStreamTime = 0;
const int moveDelay = 4000; 
const int streamInterval = 500; 

float lastValidTemp = 25.0; 

// Refined Moisture Logic: Inverting the map
// High raw value (air) = 0%, Low raw value (water) = 100%
float scaleMoisture(float raw) {
  float scaled = map(raw, 700, 0, 0, 100); 
  return constrain(scaled, 0.0, 100.0);
}

void setup() {
  Serial.begin(9600);
  dht.begin();
  probeServo.attach(SERVO_PIN);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); 
  probeServo.write(0); 
  delay(2000); 
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'S') { isScanning = true; currentStep = 0; lastMoveTime = millis(); } 
    else if (command == 'R') { isScanning = false; digitalWrite(BUZZER_PIN, LOW); probeServo.write(0); }
    else if (command == 'B') { digitalWrite(BUZZER_PIN, HIGH); } 
    else if (command == 'N') { digitalWrite(BUZZER_PIN, LOW); }  
  }

  if (isScanning) {
    if (millis() - lastStreamTime >= streamInterval) {
      // Correct Digital Read for Temperature
      float t = dht.readTemperature(); 
      
      if (isnan(t) || t > 100) { 
        t = lastValidTemp; 
      } else {
        lastValidTemp = t;
      }
      
      int rawW = analogRead(WATER_LEVEL_PIN);
      int voc = analogRead(MQ_PIN);
      
      float m = scaleMoisture(rawW); 

      // Send clean data: Depth, Temp(C), Moisture(%), Gas(Raw)
      Serial.print(levels[currentStep]); Serial.print(",");
      Serial.print(t); Serial.print(","); 
      Serial.print(m); Serial.print(",");
      Serial.println(voc);
      
      lastStreamTime = millis();
    }

    if (millis() - lastMoveTime >= moveDelay) {
      if (currentStep < 12) {
        currentStep++;
        probeServo.write(levels[currentStep]);
        lastMoveTime = millis();
      } else { isScanning = false; }
    }
  }
}