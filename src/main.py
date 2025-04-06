import time
import Adafruit_DHT

# Define the sensor type and the GPIO pin
SENSOR = Adafruit_DHT.DHT22  # DHT22 or AM2302
GPIO_PIN = 4  # Replace with your actual pin number

def read_temperature():
    """Read temperature and humidity from DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temp: {temperature:.2f}°C  Humidity: {humidity:.2f}%")
        return temperature, humidity
    else:
        print("Failed to retrieve data from sensor")
        return None, None

if __name__ == "__main__":
    while True:
        read_temperature()
        time.sleep(5)  # Adjust interval as needed
