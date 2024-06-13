const int sensorPin = A0; // Soil moisture sensor connected to A0
const int relayPin = 7;   // Relay module connected to D7
const int threshold = 500; // Moisture level threshold for watering

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Turn off the relay (water pump) initially
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(sensorPin); // Read the sensor value
  Serial.print("Soil Moisture Level: ");
  Serial.println(sensorValue); // Print the sensor value

  if (sensorValue < threshold) {
    digitalWrite(relayPin, LOW); // Turn on the relay (water pump)
    Serial.println("Watering the plant...");
  } else {
    digitalWrite(relayPin, HIGH); // Turn off the relay (water pump)
    Serial.println("Soil moisture is sufficient.");
  }

  delay(1000); // Wait for 1 second before the next reading
}
