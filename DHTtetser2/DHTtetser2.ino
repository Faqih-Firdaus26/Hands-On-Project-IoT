#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 13      // Define the GPIO pin connected to the DHT11 data pin
#define DHTTYPE DHT11 // Define the type of DHT sensor

DHT dht(DHTPIN, DHTTYPE);

// Replace with your network credentials
const char* ssid = "Redmi Note 12";
const char* password = "";

// Server URL
const char* serverName = "http://localhost:5000/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  dht.begin();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    String postData = "temperature=" + String(t) + "&humidity=" + String(h);

    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(60000); // Send data every 60 seconds
}