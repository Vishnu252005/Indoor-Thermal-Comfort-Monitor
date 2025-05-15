# """
# Sensor Interface for Thermal Comfort Monitor
# Uses Arduino-compatible sensors to read environmental parameters
# """

# import serial
# import time
# import json
# from typing import Dict, Optional

# class SensorInterface:
#     def __init__(self, port: str = '/dev/ttyUSB0', baud_rate: int = 9600):
#         """
#         Initialize sensor interface
#         port: Serial port (e.g., '/dev/ttyUSB0' for Linux, 'COM3' for Windows)
#         baud_rate: Serial communication speed
#         """
#         self.port = port
#         self.baud_rate = baud_rate
#         self.serial = None
#         self.connected = False

#     def connect(self) -> bool:
#         """Establish connection with Arduino"""
#         try:
#             self.serial = serial.Serial(self.port, self.baud_rate, timeout=1)
#             time.sleep(2)  # Wait for Arduino to reset
#             self.connected = True
#             return True
#         except Exception as e:
#             print(f"Connection error: {str(e)}")
#             self.connected = False
#             return False

#     def disconnect(self):
#         """Close serial connection"""
#         if self.serial and self.serial.is_open:
#             self.serial.close()
#             self.connected = False

#     def read_sensors(self) -> Optional[Dict]:
#         """
#         Read all sensor values
#         Returns dictionary with sensor readings or None if error
#         """
#         if not self.connected:
#             if not self.connect():
#                 return None

#         try:
#             # Request sensor data
#             self.serial.write(b'R')
#             time.sleep(0.1)  # Wait for response

#             # Read response
#             if self.serial.in_waiting:
#                 data = self.serial.readline().decode('utf-8').strip()
#                 try:
#                     sensor_data = json.loads(data)
#                     return {
#                         'air_temperature': sensor_data.get('temp', 0),
#                         'relative_humidity': sensor_data.get('humidity', 0),
#                         'air_velocity': sensor_data.get('air_speed', 0),
#                         'mean_radiant_temp': sensor_data.get('radiant_temp', 0)
#                     }
#                 except json.JSONDecodeError:
#                     print("Error parsing sensor data")
#                     return None
#             return None
#         except Exception as e:
#             print(f"Error reading sensors: {str(e)}")
#             self.connected = False
#             return None

# # Example Arduino code (to be uploaded to Arduino):
# """
# #include <DHT.h>
# #include <Wire.h>
# #include <Adafruit_Sensor.h>
# #include <Adafruit_BME280.h>
# #include <Adafruit_MLX90614.h>

# // Pin definitions
# #define DHT_PIN 2
# #define DHT_TYPE DHT22
# #define ANEMOMETER_PIN A0

# // Initialize sensors
# DHT dht(DHT_PIN, DHT_TYPE);
# Adafruit_BME280 bme;
# Adafruit_MLX90614 mlx = Adafruit_MLX90614();

# void setup() {
#   Serial.begin(9600);
  
#   // Initialize DHT
#   dht.begin();
  
#   // Initialize BME280
#   if (!bme.begin(0x76)) {
#     Serial.println("Could not find BME280 sensor!");
#   }
  
#   // Initialize MLX90614
#   if (!mlx.begin()) {
#     Serial.println("Could not find MLX90614 sensor!");
#   }
# }

# void loop() {
#   if (Serial.available() > 0) {
#     char command = Serial.read();
#     if (command == 'R') {
#       // Read sensors
#       float humidity = dht.readHumidity();
#       float temp = dht.readTemperature();
#       float pressure = bme.readPressure() / 100.0F;
#       float radiant_temp = mlx.readObjectTempC();
      
#       // Read anemometer (air speed)
#       int anemometer_value = analogRead(ANEMOMETER_PIN);
#       float air_speed = map(anemometer_value, 0, 1023, 0, 5.0); // Convert to m/s
      
#       // Create JSON response
#       Serial.print("{");
#       Serial.print("\"temp\":");
#       Serial.print(temp);
#       Serial.print(",\"humidity\":");
#       Serial.print(humidity);
#       Serial.print(",\"air_speed\":");
#       Serial.print(air_speed);
#       Serial.print(",\"radiant_temp\":");
#       Serial.print(radiant_temp);
#       Serial.println("}");
#     }
#   }
#   delay(100);
# }
# """

# # Example usage:
# if __name__ == "__main__":
#     # Create sensor interface
#     sensor = SensorInterface(port='COM3')  # Change port as needed
    
#     # Connect to Arduino
#     if sensor.connect():
#         print("Connected to sensors")
        
#         # Read sensor values
#         while True:
#             data = sensor.read_sensors()
#             if data:
#                 print("Sensor readings:", data)
#             time.sleep(1)  # Read every second
#     else:
#         print("Failed to connect to sensors") 