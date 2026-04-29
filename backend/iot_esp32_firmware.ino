#include <WiFi.h>
#include <HTTPClient.h>

// 1. WiFi Credentials
const char* ssid = "Techno povo 5 pro 5g";
const char* password = "iccd7065";

// 2. Server Endpoint (Confirmed with 'ipconfig': 172.23.172.249)
const char* serverName = "http://172.23.172.249:8000/sensor-data";

// 3. Pin Definitions for HC-SR04
#define TRIG_PIN 13
#define ECHO_PIN 14

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
}

void loop() {
  long duration;
  float distance;
  float totalDistance = 0;
  int validReadings = 0;

  // --- Dynamic Filtering: Take 5 samples for a stable average ---
  for (int i = 0; i < 5; i++) {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // 30ms timeout prevents out-of-range "ghost" values
    duration = pulseIn(ECHO_PIN, HIGH, 30000); 
    distance = (duration * 0.0343) / 2;

    if (distance > 0 && distance < 400) {
      totalDistance += distance;
      validReadings++;
    }
    delay(50); 
  }

  if (validReadings > 0) {
    float avgDistance = totalDistance / validReadings;

    // --- Dynamic Fill Level Calculation (8cm Bin) ---
    // Empty: 8cm = 0% | Full: 2cm = 100%
    int fillLevel = map(avgDistance, 8, 2, 0, 100);
    fillLevel = constrain(fillLevel, 0, 100);

    // --- Send Data via HTTP POST ---
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      // Updated JSON Structure with bin_id: 20
      String jsonData = "{\"bin_id\": 20, \"fill_level\": " + String(fillLevel) + "}";

      int httpResponseCode = http.POST(jsonData);
      
      Serial.print("Avg Dist: "); Serial.print(avgDistance);
      Serial.print("cm | Fill: "); Serial.print(fillLevel);
      Serial.print("% | Response: "); Serial.println(httpResponseCode);

      http.end();
    }
  } else {
    Serial.println("Error: Failed to get valid sensor reading.");
  }

  delay(2500); 
}
